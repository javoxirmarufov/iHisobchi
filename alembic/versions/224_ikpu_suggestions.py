# coding: utf-8
"""224 — очередь предложений ИКПУ для каталога продавца (UmagShop).

Почему таблица, а не колонки в ``products_catalog``. Предложение — событие с
автором, временем и решением, а не свойство товара. Колонка
``ikpu_suggested_*`` неизбежно стала бы «почти настоящим кодом», и первый же
код-путь начал бы читать её как истину. Отдельная таблица делает границу
физической: ``products_catalog.ikpu_code`` остаётся **единственным** источником
истины о коде, а предложение живёт рядом и до подтверждения человеком не значит
ничего.

Массовый backfill ИКПУ запрещён (ст. 223 НК РУз): конвейер пишет только строки
в эту таблицу; перенос в ``products_catalog`` — отдельной ручкой с явным списком
id. Частичный UNIQUE ``product_id WHERE status='pending'`` гасит двойные
предложения при параллельных прогонах.

Ревизия строго аддитивна: одна ``CREATE TABLE`` + два индекса, без backfill и
без мутации существующих данных. Downgrade симметричен.

Revision ID: 224
Revises: 223
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "224"
down_revision: Union[str, None] = "223"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ikpu_suggestions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "business_id",
            sa.Integer(),
            sa.ForeignKey("businesses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer(),
            sa.ForeignKey("products_catalog.id", ondelete="CASCADE"),
            nullable=False,
        ),
        # NULL = requires_manual (конвейер не уверен / Tasnif не ответил)
        sa.Column("code", sa.String(17), nullable=True),
        # Каноническое имя Tasnif — то, что продавец видит рядом с кодом
        sa.Column("catalog_name", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=True),
        # profile|whitelist|cache|tasnif_rag|requires_manual|pending_import
        sa.Column("source", sa.String(30), nullable=False),
        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        # users.id, без FK — межмодульная ссылка, users может жить иначе
        sa.Column("decided_by", sa.Integer(), nullable=True),
    )
    # Один pending на товар — фенс от двойного предложения при параллельных
    # прогонах suggest_batch / import-enqueue.
    op.create_index(
        "uq_ikpu_suggestions_pending",
        "ikpu_suggestions",
        ["product_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )
    op.create_index(
        "ix_ikpu_suggestions_business_status",
        "ikpu_suggestions",
        ["business_id", "status"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ikpu_suggestions_business_status",
        table_name="ikpu_suggestions",
    )
    op.drop_index(
        "uq_ikpu_suggestions_pending",
        table_name="ikpu_suggestions",
    )
    op.drop_table("ikpu_suggestions")
