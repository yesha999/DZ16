import json
from datetime import datetime

from flask import render_template, request

from create_models import User, Offer, Order

from settings import app, db


@app.route("/")
def main_page():
    """ Ссылки на значимые страницы для удобства"""
    return render_template('index.html')


@app.route("/users", methods=["GET"])
def get_users():
    """Список пользователей"""
    users = User.query.all()
    return render_template('all_users.html', users=users)


@app.route("/users", methods=["POST"])
def load_user():
    """Пост запрос добавления пользователя"""
    first_name = request.values.get("first_name")
    last_name = request.values.get("last_name")
    age = request.values.get("age")
    email = request.values.get("email")
    role = request.values.get("role")
    phone = request.values.get("phone")
    user = User(first_name=first_name,
                last_name=last_name, age=age,
                email=email, role=role, phone=phone)
    db.session.add(user)
    db.session.commit()

    return render_template('user_added.html')


@app.route("/users/<int:id>")
def get_user(id):
    """Страница пользователя"""
    user = User.query.get(id)
    return render_template('user.html', user=user)


# Увы, мой метод решения идет через HTML, и использовать PUT невозможно (наверное).
@app.route("/users/<int:id>", methods=["POST"])
def put_user(id):
    """ПУТ (ПОСТ) запрос изменения пользователя"""
    user = User.query.get(id)
    user.first_name = request.values.get("first_name")
    user.last_name = request.values.get("last_name")
    user.age = request.values.get("age")
    user.email = request.values.get("email")
    user.role = request.values.get("role")
    user.phone = request.values.get("phone")

    db.session.add(user)
    db.session.commit()

    return render_template('user_added.html')


# Аналогично PUT, метод DELETE реализован через POST,
# т.к. мне пока что не очень понятно как отправлять json запрос методом DELETE как в разборе ДЗ
# было бы здорово, если бы хотя бы в шпаргалке, не говоря о видеоуроке,
# было упоминание этих методов: как, зачем, почему!)
@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """Удаление пользователя"""
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    return render_template('all_users.html', users=users)


# Представления для заказов
@app.route("/orders")
def get_orders():
    """Список всех заказов"""
    orders = Order.query.all()
    users = User.query.all()
    return render_template('all_orders.html', orders=orders, users=users)


@app.route("/orders", methods=["POST"])
def load_order():
    """Пост запрос добавления заказа"""
    name = request.values.get("name")
    description = request.values.get("description")
    start_date = datetime.strptime(request.values.get("start_date"), '%Y-%m-%d').date()
    end_date = datetime.strptime(request.values.get("end_date"), '%Y-%m-%d').date()
    address = request.values.get("address")
    price = request.values.get("price")
    customer_id = request.values.get("customer_id")
    executor_id = request.values.get("executor_id")
    order = Order(name=name,
                  description=description, start_date=start_date,
                  end_date=end_date, address=address, price=price, customer_id=customer_id, executor_id=executor_id)

    db.session.add(order)
    db.session.commit()

    return render_template('user_added.html')


@app.route("/orders/<int:id>")
def get_order(id):
    """Страница заказа"""
    order = Order.query.get(id)
    customer = User.query.get(order.customer_id)
    executor = User.query.get(order.executor_id)
    users = User.query.all()
    return render_template('order.html', order=order, users=users, customer=customer, executor=executor)


@app.route("/orders/<int:id>", methods=["POST"])
def put_order(id):
    """ПОСТ (ПУТ) запрос изменения заказа"""
    order = Order.query.get(id)

    order.name = request.values.get("name")
    order.description = request.values.get("description")
    order.start_date = datetime.strptime(request.values.get("start_date"), '%Y-%m-%d').date()
    order.end_date = datetime.strptime(request.values.get("end_date"), '%Y-%m-%d').date()
    order.address = request.values.get("address")
    order.price = request.values.get("price")
    order.customer_id = request.values.get("customer_id")
    order.executor_id = request.values.get("executor_id")

    db.session.add(order)
    db.session.commit()

    return render_template('user_added.html')


@app.route("/orders/<int:id>/delete", methods=["POST"])
def delete_order(id):
    """Удаление заказа"""
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return render_template('user_added.html')


# Представления для предложений
@app.route("/offers")
def get_offers():
    """Список всех предложений"""
    offers = Offer.query.all()
    users = User.query.all()
    orders = Order.query.all()
    return render_template('all_offers.html', offers=offers, orders=orders, users=users)


@app.route("/offers", methods=["POST"])
def load_offer():
    """Пост запрос добавления предложения"""
    order_id = request.values.get("order_id")
    executor_id = request.values.get("executor_id")
    offer = Offer(order_id=order_id, executor_id=executor_id)

    db.session.add(offer)
    db.session.commit()

    return render_template('user_added.html')


@app.route("/offers/<int:id>")
def get_offer(id):
    """Представление одного предложения"""
    users = User.query.all()
    orders = Order.query.all()
    offer = Offer.query.get(id)
    order = Order.query.get(offer.order_id)
    executor = User.query.get(offer.executor_id)

    return render_template('offer.html', offer=offer, orders=orders, users=users, order=order, executor=executor)


@app.route("/offers/<int:id>", methods=["POST"])
def put_offer(id):
    """ПОСТ (ПУТ) запрос изменения предложения"""
    offer = Offer.query.get(id)

    offer.order_id = request.values.get("order_id")
    offer.executor_id = request.values.get("executor_id")

    db.session.add(offer)
    db.session.commit()

    return render_template('user_added.html')


@app.route("/offers/<int:id>/delete", methods=["POST"])
def delete_offer(id):
    """Удаление предложения"""
    offer = Offer.query.get(id)
    db.session.delete(offer)
    db.session.commit()
    return render_template('user_added.html')


if __name__ == '__main__':
    app.run()
