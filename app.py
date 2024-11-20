from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from map_utils import create_map

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'  # Измените на вашу базу данных
db = SQLAlchemy(app)


class Sale(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    sale_status = db.Column(db.String)
    sale_date = db.Column(db.Date)
    sales_value_rub = db.Column(db.Numeric)
    sales_value_usd = db.Column(db.Numeric)
    created_at = db.Column(db.DateTime)


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    customer_legal_name = db.Column(db.String)
    customer_inn = db.Column(db.Integer)
    customer_mail = db.Column(db.String)
    customer_phone = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)


class Region(db.Model):
    region_id = db.Column(db.Integer, primary_key=True)
    continent_name = db.Column(db.String)
    country_name = db.Column(db.String)
    region_name = db.Column(db.String)
    city_name = db.Column(db.String)
    created_at = db.Column(db.DateTime)


class Machine(db.Model):
    machine_article_id = db.Column(db.Integer)
    machine_id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String)
    manufacturer_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)


@app.route('/')
def index():
    # Загрузка карты
    # attr = (
    #     '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    #     'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    # )
    # tiles = 'https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.png'
    # Создаем карту
    map_obj = create_map()

    # Генерируем HTML карты
    map_html = map_obj._repr_html_()

    # Возвращаем шаблон с картой
    return render_template('index.html', map=map_html)


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        # Получаем данные о продаже и сохраняем их в БД
        data = request.get_json()
        new_sale = Sale(**data)
        db.session.add(new_sale)
        db.session.commit()
        return jsonify({'status': 'success'})

    # Если GET, возвращаем все продажи
    sales_data = Sale.query.all()
    return jsonify([{
        'sale_id': sale.sale_id,
        'machine_id': sale.machine_id,
        'customer_id': sale.customer_id,
        'region_id': sale.region_id,
        'sale_status': sale.sale_status,
        'sale_date': sale.sale_date,
        'sales_value_rub': sale.sales_value_rub,
        'sales_value_usd': sale.sales_value_usd,
        'created_at': sale.created_at
    } for sale in sales_data])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)