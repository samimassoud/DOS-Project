from flask import Flask, render_template, url_for,request , redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
db= SQLAlchemy(app)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id

def add_bazar_books():
    books = [
        {'title': 'How to get a good grade in DOS in 40 minutes a day.', 'author': 'Sami', 'topic': 'distributed systems', 'stock': 10, 'cost': 25.0},
        {'title': 'RPCs for Noobs.', 'author': 'Sami', 'topic': 'distributed systems', 'stock': 15, 'cost': 20.0},
        {'title': 'Xen and the Art of Surviving Undergraduate School.', 'author': 'Sami', 'topic': 'undergraduate school', 'stock': 8, 'cost': 30.0},
        {'title': 'Cooking for the Impatient Undergrad.', 'author': 'Sami', 'topic': 'undergraduate school', 'stock': 12, 'cost': 18.0}
    ]
    for book_data in books:
        new_book = Book(title=book_data['title'], author=book_data['author'], topic=book_data['topic'], stock=book_data['stock'], cost=book_data['cost'])
        db.session.add(new_book)
    db.session.commit()
#----------------------------
@app.route('/search',methods=['GET']) # Search
def search_books():
    topic = request.args.get('topic')
    if topic:
        books = Book.query.filter_by(topic=topic).all()
        response = {'items': {book.title: book.stock for book in books}}
    else:
        response = {'error': 'Topic parameter is required for search'}
    return jsonify(response)
# and route for getting info by number of item
@app.route('/info/<int:item_number>', methods=['GET'])
def get_book_info(item_number):
    # First we need to find the book, it's by default not found
    book = Book.query.filter_by(id=item_number).first()
    if book:
       return jsonify({book.title: book.stock})
    else:
        return jsonify({'error': 'Book not found'}), 404
#Purcahse 
@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase_book(item_number):
    # First we find the book specified with number
    book = Book.query.get(item_number)

    # if book found we check if it's in the stock
    if book:
        if book.stock > 0:
            book.stock -= 1
            db.session.commit()
            return jsonify({'title': book.title, 'stock': book.stock})
        else:
            return jsonify({'error': 'Book out of stock'}),400
    # if not found
    else:
        return jsonify({'error': 'Book was not found'}), 404
#Updae
@app.route('/update/<int:item_number>', methods=['PUT'])
def update_book(item_number):
    book = Book.query.get(item_number)
    if book:
        data = request.json
        if 'cost' in data:
            book.cost = data['cost']
        if 'stock' in data:
            book.stock = data['stock']
        db.session.commit()
        return jsonify({'message': 'Book updated!!!'})
    else:
        return jsonify({'error': 'Book not found'})
# ----------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        add_bazar_books()
    app.run(debug=True)

