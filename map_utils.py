import folium
import db_utils as db

def add_custom_css_to_folium_map(folium_map):
    """
    Функция для добавления кастомного CSS стиля в карту. 
    """
    custom_css = """
    .leaflet-top.leaflet-right {
        position: absolute;
        right: 5%;
        width: 200px;
    }
    
    # .leaflet-top.leaflet-right .leaflet-control {
    #     white-space: nowrap; /* Чтобы текст не переносился */

    """

    folium_map.get_root().header.add_child(folium.Element(f'<style>{custom_css}</style>'))
    return folium_map

def create_map():
    # Создаем карту
    m = folium.Map(location=[55, 40], zoom_start=4)

    # Добавляем базовые слои
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='© OpenStreetMap contributors',
        name='Географическая карта'
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='© OpenTopoMap contributors',
        name='Топографическая карта'
    ).add_to(m)

    return m

def search_map_markers(folium_map, sales_data):
    """
    Обновляет метки на существующей карте.
    """
    search_marker_group = folium.FeatureGroup(name="Результаты поиска", overlay=True, control=True)
    for _, row in sales_data.iterrows():
        lat = row['coordinate_latitude']
        lon = row['coordinate_longitude']
        city_name = row['city_name']
        folium.Marker(
            location=[lat, lon],
            popup=f"Город: {city_name}",
            icon=folium.Icon(color="Crimson", icon="circle", prefix='fa')
        ).add_to(search_marker_group)

    # Обновляем параметры location
    folium_map.location = [lat, lon]  # Новый центр карты
    search_marker_group.add_to(folium_map)

    # Добавляем управление слоями
    folium.LayerControl().add_to(folium_map)
    return folium_map


def all_markers_map(folium_map, sale_df, region_df, machine_df, customer_df, manufacturer_df):
    """
    Функция для добавления основных меток.
    """   

    # Функция для создания кастомного HTML с цифрой в кружочке
    def create_label_html(number, color="white", text_color="black"):
        return f"""
        <div style="
            display: flex; align-items: center; justify-content: center; 
            width: 30px; height: 30px; border-radius: 50%; 
            background-color: {color}; color: {text_color}; 
            font-size: 14px; font-weight: bold; border: 1px solid black;">
            {number}
        </div>
        """

    # Создаем FeatureGroup для меток
    # marker_group = folium.FeatureGroup(name="Метки", overlay=True, control=True)
    sale_marker_group = folium.FeatureGroup(name="Продажи", overlay=True, control=True)
    manufacturer_marker_group = folium.FeatureGroup(name="Конкуренты", overlay=True, control=True)

    # Отображаем города с количеством продаж
    sale_count_df = db.get_sale_count(sale_df, region_df)
    for _, row in sale_count_df.iterrows():
        lat = row['coordinate_latitude']
        lon = row['coordinate_longitude']
        city_name = row['city_name']
        sale_count = row['sale_count']
        
        # Создаем метку с количеством продаж
        if sale_count == 1:
            icon_custom = folium.Icon(color="Crimson", icon="circle", prefix='fa') # Иконка для sale_count = 1
        else:
            icon_custom = folium.DivIcon(
                html=create_label_html(sale_count, color="Crimson", text_color="white")
            )   # Иконка для sale_count > 1
        folium.Marker(
            location=[lat, lon],
            popup=f"Город: {city_name}<br>Количество продаж: {sale_count}",
            icon=icon_custom
        ).add_to(sale_marker_group)

    # Отображаем конкурентов
    sale_count_df = db.get_competitors(manufacturer_df, region_df)
    for _, row in sale_count_df.iterrows():
        lat = row['coordinate_latitude']
        lon = row['coordinate_longitude']
        name = row['manufacturer_name']
        city_name = row['city_name']
        # Создаем метку с конкурентом
        folium.Marker(
            location=[lat, lon],
            tooltip=name,
            popup=f"Город: {city_name}",
            icon=folium.Icon(color="black", icon="briefcase", prefix='fa')
        ).add_to(manufacturer_marker_group)

    # Добавляем FeatureGroup на карту
    sale_marker_group.add_to(folium_map)
    manufacturer_marker_group.add_to(folium_map)

    # Применяем кастомный CSS стиль
    folium_map = add_custom_css_to_folium_map(folium_map)

    # Добавляем управление слоями
    folium.LayerControl().add_to(folium_map)

    return folium_map