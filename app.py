import psycopg2
import pandas as pd
from map_utils import create_map
from flask import Flask, render_template, request, jsonify

# Забираем данные о продажах из БД и сохраняем в pd.DataFrame
conn = psycopg2.connect(
    dbname="test1",  # TODO изменить наименование бд
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
cur = conn.cursor()
cur.execute("SELECT * FROM sales;")
sales_df = pd.DataFrame(cur.fetchall(), columns=['country_name', 'region_name', 'city_name',
                                                 'coordinate_longitude', 'coordinate_latitude',
                                                 'customer_name', 'machine_num', 'sale_date'])
sales_df.drop(index=0, inplace=True)
sales_df[['coordinate_longitude', 'coordinate_latitude']] = sales_df[['coordinate_longitude', 'coordinate_latitude']].astype(float)
cur.close()
conn.close()


# Приложение интерактивной карты на Flask
app = Flask(__name__)


@app.route('/')
def index():
    # Создаем карту
    map_obj = create_map(sales_df.drop_duplicates(['coordinate_longitude']))

    # Генерируем HTML карты
    map_html = map_obj._repr_html_()

    # Возвращаем шаблон с картой
    return render_template('index.html', map=map_html)


if __name__ == '__main__':
    app.run(debug=True)