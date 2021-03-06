from sqlalchemy import Column, Integer, Numeric, String, Table, Text

from app.config.database import metadata

item = Table(
    "core_item",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("name", String),
    Column("brand_name", String),
    Column("regular_price_value", Numeric),
    Column("offer_price_value", Numeric),
    Column("currency", String),
    Column("classification_l1", Text),
    Column("classification_l2", Text),
    Column("classification_l3", Text),
    Column("classification_l4", Text),
    Column("image_url", Text),
)
