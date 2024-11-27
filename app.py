import psycopg2
import pandas as pd
from flask import Flask, render_template, request, jsonify, g
from map_utils import create_map
from db_utils import get_sale_count

# Приложение интерактивной карты на Flask
app = Flask(__name__)

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
    dbname="test1",  # TODO изменить наименование бд
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
cur = conn.cursor()
# cur.execute("SELECT * FROM sales;")
# sales_df = pd.DataFrame(cur.fetchall(), columns=['country_name', 'region_name', 'city_name',
#                                                  'coordinate_longitude', 'coordinate_latitude',
#                                                  'customer_name', 'machine_num', 'sale_date'])
sales_df = pd.read_sql_query("SELECT * FROM sales;", con=conn)
#sales_df.drop(index=0, inplace=True)
sales_df[['coordinate_longitude', 'coordinate_latitude']] = sales_df[['coordinate_longitude', 'coordinate_latitude']].astype(float)

# Получаем данные о количестве продаж
test_count_df = get_sale_count(conn)

cur.close()
conn.close()

@app.route('/')
def index():
    # Создаем карту
    map_obj = create_map(sales_df.drop_duplicates(['coordinate_longitude']),
                         test_count_df)

    # Генерируем HTML карты
    map_html = map_obj._repr_html_()

    # Возвращаем шаблон с картой
    return render_template('index.html', map=map_html)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        conn.close()  # Закрываем подключение к БД при завершении приложения