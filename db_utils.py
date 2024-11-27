import pandas as pd

def get_sale_count(conn):
    """
    Получает данные о количестве продаж по городам
    """
    query = ("""
        SELECT             
            coordinate_latitude,
            coordinate_longitude,
            city_name,
            COUNT(*) AS sale_count
        FROM sales
        GROUP BY coordinate_latitude, coordinate_longitude, city_name
    """)

    sale_count_df = pd.read_sql_query(query, con=conn)
    return sale_count_df
