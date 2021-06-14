import pandas as pd

from sqlalchemy import Table, Column, Integer, String, MetaData, desc
from sqlalchemy.sql import select

from csv_manager.csv_data_db import db


def create_table(df_csv: pd.DataFrame):
    meta = MetaData()
    table_data = [
        df_csv.index.name,
        meta,
        Column("id", Integer, primary_key=True),
    ]
    for column_name in df_csv.columns:
        table_data.append(Column(column_name, String))
    csv_data_table = Table(*table_data)
    meta.create_all(db.engine, tables=[csv_data_table])

    with db.engine.connect() as conn:
        conn.execute(csv_data_table.insert(), df_csv.to_dict("records"))


def retrieve_data(table_name: str, order_by: str = "id", filters: dict = {}):
    meta = MetaData()
    table = Table(table_name, meta, autoload=True, autoload_with=db.engine)
    filters_set = []
    result = []
    
    for column_name, value in filters.items():
        filters_set.append(getattr(table.columns, column_name) == value)
    
    with db.engine.connect() as conn:
        result = conn.execute(
            select(table)
            .filter(*filters_set)
            .order_by(desc(order_by[1:]) if order_by[0] == "-" else order_by)
        ).fetchall()
    return result
