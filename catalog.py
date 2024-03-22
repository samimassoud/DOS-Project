from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.id}>'

def add_bazar_books():
    with app.app_context():
        books = [
        {'id': 1, 'title': 'How to get a good grade in DOS in 40 minutes a day.', 'author': 'Sami', 'topic': 'distributed systems', 'stock': 10, 'cost': 25.0},
        {'id': 2, 'title': 'RPCs for Noobs.', 'author': 'Sami', 'topic': 'distributed systems', 'stock': 1, 'cost': 20.0},
        {'id': 3, 'title': 'Xen and the Art of Surviving Undergraduate School.', 'author': 'Sami', 'topic': 'undergraduate school', 'stock': 8, 'cost': 30.0},
        {'id': 4, 'title': 'Cooking for the Impatient Undergrad.', 'author': 'Sami', 'topic': 'undergraduate school', 'stock': 12, 'cost': 18.0}
        ]
        for book_data in books:
            existing_book = Catalog.query.filter_by(title=book_data['title']).first()
            if not existing_book:
                new_book = Catalog(title=book_data['title'], author=book_data['author'], topic=book_data['topic'], stock=book_data['stock'], cost=book_data['cost'])
                db.session.add(new_book)
        db.session.commit()

def cleanup_database():
    with app.app_context():
        try:
            # Delete all records from the Catalog table
            db.session.query(Catalog).delete()
            db.session.commit()
            print("Database cleanup successful.")
        except Exception as e:
            db.session.rollback()
            print("Database cleanup failed:", str(e))



@app.route('/catalog', methods=['GET'])
# def get_catalog():
#     books = Catalog.query.all()
#     result = [{'id': book.id, 'title': book.title, 'author': book.author, 'topic': book.topic,
#                'stock': book.stock, 'cost': book.cost} for book in books]
#     return jsonify(result)

def search_catalog():
    query_param = request.args.get('query')
    if query_param:
        print (f"%{query_param}%")
        books = Catalog.query.filter(or_(Catalog.topic.like(f"%{query_param}%"))).all()
        if books:
            result = {book.title: book.id for book in books}
            return jsonify({'items': result})
        else:
            return jsonify({'error': 'Book not found for the given item ID'}), 404
    else:
        return jsonify({'error': 'Query parameter is required for search'}), 400

@app.route('/info', methods=['GET'])
def get_book_info():
    book_id = request.args.get('id')
    if book_id:
        book = Catalog.query.filter_by(id=book_id).first()
        if book:
            result = {'id': book.id, 'title': book.title, 'author': book.author, 'topic': book.topic,
                      'stock': book.stock, 'cost': book.cost}
            return jsonify(result)
        else:
            return jsonify({'error': 'Book not found for the given item ID'}), 404
    else:
        return jsonify({'error': 'Book ID parameter is required for info'}), 400


@app.route('/update', methods=['POST'])
def update_stock():
    data = request.get_json()
    book_id = data.get('id')
    updated_stock = data.get('stock')

    if book_id is None or updated_stock is None:
        return jsonify({'error': 'Missing book ID or stock information'}), 400

    book = Catalog.query.filter_by(id=book_id).first()
    if book:
        book.stock = updated_stock
        db.session.commit()
        return jsonify({'message': 'Stock updated successfully'}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404
if __name__ == "__main__":
    cleanup_database()
    add_bazar_books()
    app.run(debug=True, host='0.0.0.0', port=5001)