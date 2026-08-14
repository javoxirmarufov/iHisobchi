# coding: utf-8
"""217 — кадровое делопроизводство: события, приказы, документы, серии номеров.

Фаза 1 плана `docs/hr-personnel-records-plan.md`.

Зачем четыре таблицы, а не поля на `employees`
----------------------------------------------
Карточка сотрудника перестаёт быть формой, которую кто-то заполнил, и
становится **свёрткой ленты кадровых событий** — как `attendance_days`
производна от событий отметки. Отсюда `hr_events` как источник правды: «кем
работает» и «сколько получает» нельзя поменять мимо приказа, а состояние на
любую дату в прошлом восстанавливается перечитыванием ленты.

`payload` и `prev_snapshot` — JSONB намеренно: набор изменяемых условий растёт
(доля ставки, надбавки, график, место работы), и колонка под каждое означала бы
миграцию на каждую кадровую новацию.

Нумерация приказов (решение владельца 2026-08-10)
-------------------------------------------------
**Отдельная серия и свой префикс на каждый тип**: П — приём, У — увольнение,
ПВ — перевод, ПО — изменение оклада, О — отпуск, К — командировка, ШР —
штатное расписание. Общий префикс на все типы при отдельных счётчиках дал бы
два разных документа с номером «П-1» в одном году — дефект реестра, а не
стилистика.

Счётчик живёт в `hr_order_series` с ключом (бизнес, тип, **год**): сброс
1 января получается сам собой, новой строкой на новый год, без крона.

`number` у приказа **nullable**, и это не забывчивость: номер выдаётся при
ИЗДАНИИ (`status='issued'`), а не при создании черновика. Иначе брошенные
черновики выжигают номера и в реестре появляются дыры, которые придётся
объяснять проверяющему. Тот же дефект уже ловили в voice-контуре — экран
review жёг номер до подтверждения.

`number_year` хранится явной колонкой, а не вычисляется из `order_date` в
выражении индекса: уникальность номера обязана держаться на том же значении
года, на котором крутился счётчик, а не на функции от даты, которую можно
отредактировать после выдачи номера.

ЭЦП (решение владельца 2026-08-10)
----------------------------------
Приказы подписываются ЭЦП, поэтому колонки подписи заводятся сразу — но
только как хранилище. Сам контур подписания (E-IMZO) в эту фазу НЕ входит:
он трогает `services/signing_*` и admin-agent, а это отдельный blast radius.
Пустые колонки сегодня дешевле, чем миграция по живой таблице завтра.

Аддитивно: только `CREATE TABLE` и индексы. Ни `DROP`, ни `UPDATE`, ни
backfill. `downgrade` симметричен.

Revision ID: 217
Revises: 216
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "217"
down_revision: Union[str, None] = "216"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Зеркалит services/hr_records_db.EVENT_KINDS. Расхождение = 23514 из PG на
# ровном месте, поэтому оба списка правятся одной правкой.
_EVENT_KINDS = (
    "hire",
    "probation_end",
    "transfer",
    "rate_change",
    "leave",
    "sick",
    "trip",
    "dismiss",
)
_ORDER_KINDS = _EVENT_KINDS + ("staffing",)
_DOC_KINDS = (
    "contract",
    "addendum",
    "order",
    "t2_card",
    "notice",
    "consent",
    "statement",
    "ensst_extract",
    "income_ref",
    "settlement_note",
)


def _in_list(column: str, values: Sequence[str]) -> str:
    joined = ", ".join(f"'{v}'" for v in values)
    return f"{column} IN ({joined})"


def upgrade() -> None:
    # --- 1. Лента кадровых событий — источник правды -----------------------
    op.create_table(
        "hr_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "business_id",
            sa.Integer(),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            sa.BigInteger(),
            sa.ForeignKey("employees.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=24), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column(
            "payload",
            sa.JSON().with_variant(postgresql.JSONB(), "postgresql"),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("prev_snapshot", sa.JSON().with_variant(postgresql.JSONB(), "postgresql"), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="active"),
        # Отмена — компенсирующее событие со ссылкой, а не DELETE: кадровая
        # история не переписывается задним числом.
        sa.Column(
            "cancels_event_id",
            sa.BigInteger(),
            sa.ForeignKey("hr_events.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(_in_list("kind", _EVENT_KINDS), name="ck_hr_events_kind"),
        sa.CheckConstraint(_in_list("status", ("active", "cancelled")), name="ck_hr_events_status"),
    )
    op.create_index(
        "ix_hr_events_employee",
        "hr_events",
        ["business_id", "employee_id", "effective_from"],
    )

    # --- 2. Серии номеров приказов ----------------------------------------
    op.create_table(
        "hr_order_series",
        sa.Column(
            "business_id",
            sa.Integer(),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=24), nullable=False),
        sa.Column("year", sa.SmallInteger(), nullable=False),
        sa.Column("prefix", sa.String(length=8), nullable=False),
        sa.Column("separator", sa.String(length=4), nullable=False, server_default="-"),
        sa.Column("next_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("business_id", "kind", "year"),
        sa.CheckConstraint(_in_list("kind", _ORDER_KINDS), name="ck_hr_order_series_kind"),
        sa.CheckConstraint("next_number >= 1", name="ck_hr_order_series_next_positive"),
    )

    # --- 3. Приказы --------------------------------------------------------
    op.create_table(
        "hr_orders",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "business_id",
            sa.Integer(),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        # NULL — приказ не про человека (утверждение штатного расписания).
        sa.Column(
            "employee_id",
            sa.BigInteger(),
            sa.ForeignKey("employees.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "event_id",
            sa.BigInteger(),
            sa.ForeignKey("hr_events.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("kind", sa.String(length=24), nullable=False),
        sa.Column("number", sa.String(length=64), nullable=True),
        sa.Column("number_year", sa.SmallInteger(), nullable=True),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("basis", sa.Text(), nullable=True),
        # Точная формулировка статьи ТК РУз для увольнения: вольный пересказ
        # делает приказ оспоримым, поэтому хранится код из справочника.
        sa.Column("tk_article", sa.String(length=32), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        sa.Column("file_id", sa.Text(), nullable=True),
        # ЭЦП — хранилище готово, контур подписания придёт отдельной фазой.
        sa.Column("signature_pkcs7", sa.Text(), nullable=True),
        sa.Column("signer_cert_cn", sa.Text(), nullable=True),
        sa.Column("signer_tin", sa.String(length=16), nullable=True),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(_in_list("kind", _ORDER_KINDS), name="ck_hr_orders_kind"),
        sa.CheckConstraint(
            _in_list("status", ("draft", "issued", "signed", "cancelled")),
            name="ck_hr_orders_status",
        ),
        # Номер и его год появляются вместе или не появляются вовсе: без этого
        # строка с номером и пустым годом обошла бы уникальный индекс ниже.
        sa.CheckConstraint(
            "(number IS NULL AND number_year IS NULL) OR (number IS NOT NULL AND number_year IS NOT NULL)",
            name="ck_hr_orders_number_pair",
        ),
    )
    # Два приказа одного года с одним номером — дефект реестра. Частичный,
    # потому что у черновиков номера ещё нет и они не должны конфликтовать.
    op.create_index(
        "uq_hr_orders_number",
        "hr_orders",
        ["business_id", "number_year", "number"],
        unique=True,
        postgresql_where=sa.text("number IS NOT NULL"),
    )
    op.create_index(
        "ix_hr_orders_employee",
        "hr_orders",
        ["business_id", "employee_id", "order_date"],
    )

    # --- 4. Документы пакета ----------------------------------------------
    op.create_table(
        "hr_documents",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "business_id",
            sa.Integer(),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            sa.BigInteger(),
            sa.ForeignKey("employees.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "event_id",
            sa.BigInteger(),
            sa.ForeignKey("hr_events.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "order_id",
            sa.BigInteger(),
            sa.ForeignKey("hr_orders.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("number", sa.String(length=64), nullable=True),
        sa.Column("doc_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        sa.Column("file_id", sa.Text(), nullable=True),
        sa.Column("template_id", sa.String(length=64), nullable=True),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("handed_over_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(_in_list("kind", _DOC_KINDS), name="ck_hr_documents_kind"),
        sa.CheckConstraint(
            _in_list("status", ("draft", "generated", "signed", "handed")),
            name="ck_hr_documents_status",
        ),
    )
    op.create_index(
        "ix_hr_documents_event",
        "hr_documents",
        ["business_id", "event_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_hr_documents_event", table_name="hr_documents")
    op.drop_table("hr_documents")
    op.drop_index("ix_hr_orders_employee", table_name="hr_orders")
    op.drop_index("uq_hr_orders_number", table_name="hr_orders")
    op.drop_table("hr_orders")
    op.drop_table("hr_order_series")
    op.drop_index("ix_hr_events_employee", table_name="hr_events")
    op.drop_table("hr_events")
