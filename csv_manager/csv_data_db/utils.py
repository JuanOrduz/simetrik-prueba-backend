import pandas as pd

from sqlalchemy import Table, Column, Integer, String, MetaData

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
