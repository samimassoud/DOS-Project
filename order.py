from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Order {self.id}>'

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        orders = Order.query.all()
        result = [{'id': order.id, 'book_id': order.book_id, 'status': order.status} for order in orders]
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        new_order = Order(book_id=data['book_id'], status='Pending')
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order placed successfully'}), 201

@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def single_order(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'GET':
        return jsonify({'id': order.id, 'book_id': order.book_id, 'status': order.status})
    elif request.method == 'PUT':
        data = request.json
        order.status = data.get('status', order.status)
        db.session.commit()
        return jsonify({'message': 'Order updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)
