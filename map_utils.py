import folium

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


def create_map(sales_df, sale_count_df):
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
            font-size: 14px; font-weight: bold; border: 2px solid black;">
            {number}
        </div>
        """

    # Создаем FeatureGroup для меток
    marker_group = folium.FeatureGroup(name="Метки", overlay=True, control=True)
    sale_marker_group = folium.FeatureGroup(name="Продажи", overlay=True, control=True)

    # Добавляем маркеры в FeatureGroup
    # folium.Marker(
    #     location=[55.7558, 37.6176],  # Москва
    #     tooltip="Продажа товаров",
    #     popup="Город: Москва",
    #     icon=folium.DivIcon(html=create_label_html(5))  # Используем функцию для создания метки
    # ).add_to(marker_group)

    folium.Marker(
        location=[59.9343, 30.3351],  # Санкт-Петербург
        tooltip="Конкурент",
        popup="Город: Санкт-Петербург",
        icon=folium.Icon(color="red", prefix='fa')
    ).add_to(marker_group)

    folium.Marker(
        location=[40.3680, 49.8770],  # Баку
        tooltip="Конкурент",
        popup="Город: Баку",
        icon=folium.Icon(color="red", icon="briefcase", prefix='fa')
    ).add_to(marker_group)

    folium.Marker(
        location=[61.5240, 105.3188],  # Пример месторождения в Сибири
        tooltip="Месторождение камня",
        popup="Месторождение: Сибирь",
        icon=folium.Icon(color="darkred", icon="gem", prefix='fa')
    ).add_to(marker_group)

    # отображение всех продаж на карте
    for sale_index in sales_df.index:
        folium.Marker(
            # !!!! нужно поменять местами: сначала широта(lat), потом долгота (lon)
            location=[sales_df['coordinate_longitude'][sale_index], sales_df['coordinate_latitude'][sale_index]],
            tooltip=sales_df['customer_name'][sale_index],
            popup=sales_df['machine_num'][sale_index],
            icon=folium.Icon(color="red", icon="circle", prefix='fa')
        ).add_to(marker_group)

    # Отображаем города с количеством продаж
    for _, row in sale_count_df.iterrows():
        lat = row['coordinate_latitude']
        lon = row['coordinate_longitude']
        city_name = row['city_name']
        sale_count = row['sale_count']
        
        # # Получаем координаты для города (сначала ищем координаты по имени города в sales_df)
        # city_sales = sales_df[sales_df['city_name'] == city_name]
        # if not city_sales.empty:
        #     lat, lon = city_sales.iloc[0][['coordinate_latitude', 'coordinate_longitude']]
            
        # Создаем метку с количеством продаж
        folium.Marker(
            location=[lat, lon],
            popup=f"Город: {city_name}<br>Количество продаж: {sale_count}",
            icon=folium.DivIcon(
                html=create_label_html(sale_count, color="blue", text_color="white")
            )
        ).add_to(sale_marker_group)

    # Добавляем FeatureGroup на карту
    marker_group.add_to(m)
    sale_marker_group.add_to(m)

    # Добавляем управление слоями
    folium.LayerControl().add_to(m)

    # Применяем кастомный CSS стиль
    m = add_custom_css_to_folium_map(m)

    return m
