import psycopg2
import pandas as pd
from flask import Flask, render_template, request, jsonify, g
from map_utils import create_map
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
# cur.execute("SELECT * FROM sales;")
# sales_df = pd.DataFrame(cur.fetchall(), columns=['country_name', 'region_name', 'city_name',
#                                                  'coordinate_longitude', 'coordinate_latitude',
#                                                  'customer_name', 'machine_num', 'sale_date'])
#sales_df = pd.read_sql_query("SELECT * FROM ez_sale;", con=conn)
#sales_df.drop(index=0, inplace=True)
#sales_df[['coordinate_longitude', 'coordinate_latitude']] = sales_df[['coordinate_longitude', 'coordinate_latitude']].astype(float)

sale_df = pd.read_sql_query("SELECT * FROM ez_sale;", con=conn)
region_df = pd.read_sql_query("SELECT * FROM ez_region;", con=conn)
machine_df = pd.read_sql_query("SELECT * FROM ez_machine;", con=conn)
manufacturer_df = pd.read_sql_query("SELECT * FROM ez_manufacturer;", con=conn)
customer_df = pd.read_sql_query("SELECT * FROM ez_customer;", con=conn)
# Получаем данные о количестве продаж
# test_count_df = get_sale_count(conn)

cur.close()
conn.close()

@app.route('/')
def index():
    # Создаем карту
    map_obj = create_map(sale_df, region_df, machine_df, customer_df, manufacturer_df)

    # Генерируем HTML карты
    map_html = map_obj._repr_html_()

    # Возвращаем шаблон с картой
    return render_template('index.html', map=map_html)


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