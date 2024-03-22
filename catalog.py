from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

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
    books = [
        {'title': 'How to get a good grade in DOS in 40 minutes a day.', 'author': 'Sami', 'topic': 'distributed systems', 'stock': 10, 'cost': 25.0},
        {'title': 'RPCs for Noobs.', 'author': 'Sami', 'topic': 'distributed systems', 'stock': 15, 'cost': 20.0},
        {'title': 'Xen and the Art of Surviving Undergraduate School.', 'author': 'Sami', 'topic': 'undergraduate school', 'stock': 8, 'cost': 30.0},
        {'title': 'Cooking for the Impatient Undergrad.', 'author': 'Sami', 'topic': 'undergraduate school', 'stock': 12, 'cost': 18.0}
    ]
    for book_data in books:
        existing_book = Catalog.query.filter_by(title=book_data['title']).first()
        if not existing_book:
            new_book = Catalog(title=book_data['title'], author=book_data['author'], topic=book_data['topic'], stock=book_data['stock'], cost=book_data['cost'])
            db.session.add(new_book)
    db.session.commit()

def cleanup_database():
    try:
        # Delete all records from the Catalog table
        db.session.query(Catalog).delete()
        db.session.commit()
        print("Database cleanup successful.")
    except Exception as e:
        db.session.rollback()
        print("Database cleanup failed:", str(e))

# Create database tables
with app.app_context():
    db.create_all()

# Add initial books to the catalog
add_bazar_books()

@app.route('/catalog', methods=['GET'])
def get_catalog():
    books = Catalog.query.all()
    result = [{'id': book.id, 'title': book.title, 'author': book.author, 'topic': book.topic,
               'stock': book.stock, 'cost': book.cost} for book in books]
    return jsonify(result)

def search_catalog():
    query_param = request.args.get('query')
    if query_param:
        if query_param.isdigit():
            book = Catalog.query.filter_by(id=query_param).first()
            if book:
                result = {'id': book.id, 'title': book.title, 'author': book.author, 'topic': book.topic,
                          'stock': book.stock, 'cost': book.cost}
                return jsonify(result)
            else:
                return jsonify({'error': 'Book not found for the given item ID'}), 404
        else:
            books = Catalog.query.filter_by(topic=query_param).all()
            result = [{'id': book.id, 'title': book.title, 'author': book.author, 'topic': book.topic,
                       'stock': book.stock, 'cost': book.cost} for book in books]
            return jsonify(result)
    else:
        return jsonify({'error': 'Query parameter is required for search'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)