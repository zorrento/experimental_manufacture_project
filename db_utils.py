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

    # Фильтруем данные 
    competitor_df = merged_df[merged_df['manufacturer_name'] != 'НПО "ЭЗ"']
    return competitor_df


def get_sales_by_machine_id(machine_id, machine_df, sale_df, region_df):

    # Находим machine_id по machine_name
    # machine_id = machine_df[machine_df['machine_name'] == machine_name]['machine_id'].iloc[0]

    try:
        # Фильтруем sale_df по machine_id
        machine_id_int = int(machine_id)
        sales_by_machine_df = sale_df[sale_df['machine_id'] == machine_id_int]

        # Объединяем DataFrame по 'region_id' 
        search_result_df = pd.merge(sales_by_machine_df, region_df, on='region_id', how='inner')

        return search_result_df  # Возвращаем результат с регионами, если merge выполнился успешно.
    
    except IndexError:
        print(f"Машина '{machine_id}' не найдена.")
        return None


def get_sales_by_city_name(city_name, sale_df, region_df):

    # Находим region_id по city_name, который содержит подстроку
    region_id = region_df[region_df['city_name'].str.contains(city_name, case=False, na=False)]['region_id'].iloc[0]

    try:
        # Объединяем DataFrame по 'region_id' 
        sale_with_region_df = pd.merge(sale_df, region_df, on='region_id', how='inner')

        # Фильтруем sale_df по city_name
        region_id_int = int(region_id)
        search_result_df = sale_with_region_df[sale_with_region_df['region_id'] == region_id_int]

        return search_result_df  # Возвращаем результат с регионами, если merge выполнился успешно.
    
    except IndexError:
        print(f"Город '{city_name}' не найден в продажах.")
        return None
    

