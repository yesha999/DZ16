import json

from datetime import datetime

from sqlalchemy.orm import relationship

from settings import db


# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///UOO.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    phone = db.Column(db.String(16))


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    orders = relationship("Order")
    users = relationship("User")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"), )
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    customers = relationship("User", foreign_keys='Order.customer_id', cascade="all,delete")
    executors = relationship("User", foreign_keys='Order.executor_id')


if __name__ == '__main__':
    db.create_all()

    ##########################################################
    with open('jsons/users.json', encoding='utf-8') as file:
        users_list_json = json.load(file)

    users_list = []
    for i in users_list_json:
        user_i = User(id=i['id'], first_name=i['first_name'],
                      last_name=i['last_name'], age=i['age'],
                      email=i['email'], role=i['role'], phone=i['phone'])
        users_list.append(user_i)

    ##########################################################
    with open('jsons/offers.json', encoding='utf-8') as file:
        offers_list_json = json.load(file)

    offers_list = []
    for i in offers_list_json:
        offer_i = Offer(id=i['id'], order_id=i['order_id'], executor_id=i['executor_id'])
        offers_list.append(offer_i)

    ##########################################################
    with open('jsons/orders.json', encoding='utf-8') as file:
        orders_list_json = json.load(file)

    orders_list = []
    for i in orders_list_json:
        order_i = Order(id=i['id'], name=i['name'],
                        description=i['description'], start_date=datetime.strptime(i['start_date'], '%m/%d/%Y').date(),
                        end_date=datetime.strptime(i['end_date'], '%m/%d/%Y').date(), address=i['address'],
                        price=i['price'], customer_id=i['customer_id'],
                        executor_id=i['executor_id'])
        orders_list.append(order_i)

    with db.session.begin():
        db.session.add_all(users_list)
        db.session.add_all(offers_list)
        db.session.add_all(orders_list)
        db.session.commit
