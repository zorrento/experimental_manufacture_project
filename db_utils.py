import pandas as pd

def get_sale_count(sale_df, region_df):
    """
    Получает данные о количестве продаж по городам
    
    query = ('''
        SELECT             
            r.coordinate_latitude,
            r.coordinate_longitude,
            city_name,
            COUNT(s.sale_id) AS sale_count
        FROM ez_sale s
        inner join ez_region r ON s.region_id = r.region_id 
        GROUP BY coordinate_latitude, coordinate_longitude, city_name
    ''')

    sale_count_df = pd.read_sql_query(query, con=conn)
    """

    # Объединяем DataFrame по 'region_id'
    merged_df = pd.merge(sale_df, region_df, on='region_id', how='inner')

    # Группируем данные и считаем количество продаж
    sale_count_df = merged_df.groupby(['coordinate_latitude', 'coordinate_longitude', 'city_name'])\
                            .agg(sale_count=('sale_id', 'count')).reset_index()
    return sale_count_df

def get_competitors(manufacturer_df, region_df):
    """
    Получает данные о конкурентах
    """

    # Объединяем DataFrame по 'region_id'
    merged_df = pd.merge(manufacturer_df, region_df, on='region_id', how='inner')

    # Группируем данные и считаем количество продаж
    competitor_df = merged_df[merged_df['manufacturer_name'] != 'НПО "ЭЗ"']
    return competitor_df

