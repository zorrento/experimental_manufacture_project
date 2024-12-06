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


def create_map(sale_df, region_df, machine_df, customer_df, manufacturer_df):
    """
    Функция для создания карты с двумя базовыми слоями и слоем меток.
    """
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
    marker_group = folium.FeatureGroup(name="Метки", overlay=True, control=True)
    sale_marker_group = folium.FeatureGroup(name="Продажи", overlay=True, control=True)
    manufacturer_marker_group = folium.FeatureGroup(name="Конкуренты", overlay=True, control=True)

    # Добавляем маркеры в FeatureGroup
    # folium.Marker(
    #     location=[55.7558, 37.6176],  # Москва
    #     tooltip="Продажа товаров",
    #     popup="Город: Москва",
    #     icon=folium.DivIcon(html=create_label_html(5))  # Используем функцию для создания метки
    # ).add_to(marker_group)

    # folium.Marker(
    #     location=[59.9343, 30.3351],  # Санкт-Петербург
    #     tooltip="Конкурент",
    #     popup="Город: Санкт-Петербург",
    #     icon=folium.Icon(color="red", prefix='fa')
    # ).add_to(marker_group)

    # folium.Marker(
    #     location=[40.3680, 49.8770],  # Пример метки Конкурент
    #     tooltip="Конкурент",
    #     popup="Город: ",
    #     icon=folium.Icon(color="red", icon="briefcase", prefix='fa')
    # ).add_to(marker_group)

    # folium.Marker(
    #     location=[61.5240, 105.3188],  # Пример месторождения в Сибири
    #     tooltip="Месторождение камня",
    #     popup="Месторождение: Сибирь",
    #     icon=folium.Icon(color="darkred", icon="gem", prefix='fa')
    # ).add_to(marker_group)

    # отображение всех продаж на карте
    # for sale_index in sales_df.index:
    #     folium.Marker(
    #         # !!!! нужно поменять местами: сначала широта(lat), потом долгота (lon)
    #         location=[sales_df['coordinate_longitude'][sale_index], sales_df['coordinate_latitude'][sale_index]],
    #         tooltip=sales_df['customer_name'][sale_index],
    #         popup=sales_df['machine_num'][sale_index],
    #         icon=folium.Icon(color="red", icon="circle", prefix='fa')
    #     ).add_to(marker_group)

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
    sale_marker_group.add_to(m)
    manufacturer_marker_group.add_to(m)

    # Добавляем управление слоями
    folium.LayerControl().add_to(m)

    # Применяем кастомный CSS стиль
    m = add_custom_css_to_folium_map(m)

    return m
