import psycopg2
import pandas as pd
from flask import Flask, render_template, request, jsonify, g
import map_utils as map_func
import db_utils as db
import geopy

# Приложение интерактивной карты на Flask
app = Flask(__name__)

geolocator = geopy.Nominatim(user_agent="http")

# Настройки подключения
DB_CONFIG = {
    'dbname': 'test1',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

# Функция для установки подключения
def get_db_connection():
    if 'conn' not in g:
        g.conn = psycopg2.connect(**DB_CONFIG)
    if 'cur' not in g:
        g.cur = g.conn.cursor()
    return g.cur

# Создаем соединение перед запросом
@app.before_request
def before_request():
    get_db_connection()

# Закрываем соединение после запроса
@app.teardown_request
def close_db_connection(exception):
    conn = g.pop('conn', None)
    cur = g.pop('cur', None)
    if conn:
        cur.close()
        conn.close()


# Забираем данные о продажах из БД и сохраняем в pd.DataFrame
conn = psycopg2.connect(
    dbname="interactive_map",
    user="postgres",
    password="estetka2024!",
    host="db.nerq.ru",
    port=2410
)
cur = conn.cursor()


sale_df = pd.read_sql_query("SELECT * FROM ez_sale;", con=conn)
region_df = pd.read_sql_query("SELECT * FROM ez_region;", con=conn)
machine_df = pd.read_sql_query("SELECT * FROM ez_machine;", con=conn)
manufacturer_df = pd.read_sql_query("SELECT * FROM ez_manufacturer;", con=conn)
customer_df = pd.read_sql_query("SELECT * FROM ez_customer;", con=conn)

cur.close()
conn.close()

@app.route('/')
def index():

    # Создаём базовую карту
    base_map = map_func.create_map()

    # Добавляем маркеры
    all_markers_map = map_func.all_markers_map(base_map, sale_df, region_df, machine_df, customer_df, manufacturer_df)

    # Генерируем HTML карты
    map_html = all_markers_map._repr_html_()

    # Возвращаем шаблон с картой
    return render_template('index.html', map=map_html)


@app.route('/search_by_machine', methods=['GET'])
def search_by_machine():
    machine_id = request.args.get('machine_id')
    if machine_id:
        sales_data = db.get_sales_by_machine_id(machine_id, machine_df, sale_df, region_df)
        if not sales_data.empty:
            search_map = map_func.create_map()  # Создаём новую карту
            updated_map = map_func.search_map_markers(search_map, sales_data)
            search_map_html = updated_map._repr_html_()

            # Возвращаем HTML карты в формате JSON
            return jsonify({'map': search_map_html})
        else:
            return jsonify({"error": "Номер машины не найден в продажах"}), 404  # Код 404 - Not Found
    else:
        return jsonify({"error": "Machine name is missing"}), 400 # Код 400 - Bad Request
    
@app.route('/search_by_city', methods=['GET'])
def search_by_city():
    city_name = request.args.get('city_name')
    if city_name:
        sales_data = db.get_sales_by_city_name(city_name, sale_df, region_df)
        if not sales_data.empty:
            search_map = map_func.create_map()  # Создаём новую карту
            updated_map = map_func.search_map_markers(search_map, sales_data)
            search_map_html = updated_map._repr_html_()

            # Возвращаем HTML карты в формате JSON
            return jsonify({'map': search_map_html})
        else:
            return jsonify({"error": "Город не найден в продажах"}), 404  # Код 404 - Not Found
    else:
        return jsonify({"error": "City name is missing"}), 400 # Код 400 - Bad Request

@app.route('/reset_map', methods=['GET'])
def reset_map():
    base_map = map_func.create_map()  # Создаём базовую карту
    all_markers_map = map_func.all_markers_map(base_map, sale_df, region_df, machine_df, customer_df, manufacturer_df)
    map_html = all_markers_map._repr_html_()

    return jsonify({'map': map_html})


@app.route('/get_url_root')
def get_url():
    return jsonify({'base_url': request.url_root})


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        # Обработка формы
        date_of_sale = request.form['date_of_sale']
        supplier_name = request.form['supplier_name']
        car_id = request.form['car_id']
        city_of_sale = request.form['city_of_sale']

        print("Получены данные:")
        print(date_of_sale)
        print(supplier_name)
        print(car_id)
        print(city_of_sale)

        city_location = None
        try:
            city_location = geolocator.geocode(city_of_sale, language="ru")
            lat = city_location.latitude
            lng = city_location.longitude
            print(f"Получены координаты: {lat} {lng}")
        except Exception as e:
            print(f"Ошибка при получении координат города {city_of_sale}. {e}")
        if city_location is None:
            return render_template('add_record.html', error="Ошибка при получении координат введенного города")

        return '''<script>
                   window.close();
                   alert("Новая запись о продаже успешно добавлена");
                  </script>'''

    return render_template('add_record.html')


@app.route('/autocomplete_cities')
def autocomplete_cities():
    query = request.args.get('query')
    locations = geolocator.geocode(query, exactly_one=False, language="ru")
    hints = []
    if locations:
        hints = [location.address for location in locations]
    return jsonify(cities=hints)


@app.route('/delete_record', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        # Обработка формы
        sale_id = request.form['sale_id']

        print("Получены данные:")
        print(sale_id)

        return '''<script>
                   window.close();
                   alert("Запись о продаже успешно удалена");
                  </script>'''

    return render_template('delete_record.html')


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        conn.close()  # Закрываем подключение к БД при завершении приложения