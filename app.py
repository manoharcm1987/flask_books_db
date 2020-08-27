from flask import Flask, jsonify, request
from db_utils.db import DBHandler

app = Flask(__name__)
db = DBHandler()


@app.route("/books", methods=['GET', 'POST'])
def books():
    db_conn = db.create_connection()
    cur = db_conn.cursor()
    try:
        if request.method == 'GET':
            print("Get Request: ")
            cursor = cur.execute("SELECT * FROM books")
            if cursor is not None:
                list_of_books = [dict(id=row[0], author=row[1], language=row[2], title=row[3], price=row[4],
                                      published_year=row[5]) for row in cursor.fetchall()]
                return jsonify(list_of_books), 200
            else:
                return "No records found", 404
    except Exception as e:
        return jsonify({"error": str(e)})

    if request.method == 'POST':
        print("Post Request: ")
        try:
            author = request.form['author']
            language = request.form['language']
            title = request.form['title']
            price = request.form['price']
            published_year = request.form['published_year']
            query = """INSERT INTO books (author, language, title, price, published_year) VALUES (?,?,?,?,?)"""
            cur.execute(query, (author, title, language, price, published_year))
            db_conn.commit()
            return f"Book with the id: {cur.lastrowid} created successfully", 201
        except Exception as e:
            return jsonify({"error": str(e)})


@app.route("/book/<int:book_id>", methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    db_conn = db.create_connection()
    cur = db_conn.cursor()
    if request.method == 'GET':
        print("Get Request: ")
        try:
            sql = "SELECT * FROM books WHERE id=?"
            cursor = cur.execute(sql, (book_id,))
            book_row = cursor.fetchone()
            if book_row is not None:
                book = dict(id=book_row[0], author=book_row[1], language=book_row[2], title=book_row[3], price=book_row[4],
                            published_year=book_row[5])
                return jsonify(book), 200
            else:
                return f"Book with id {book_id} not found !!", 404
        except Exception as e:
            return jsonify({"error": str(e)})

    if request.method == 'PUT':
        print("Put Request: ")
        try:
            author = request.form['author']
            title = request.form['title']
            language = request.form['language']
            price = request.form['price']
            published_year = request.form['published_year']
            updated_book = {"id": book_id, "author": author, "language": language, "title": title, "price": price,
                            "published_year": published_year}
            sql = "UPDATE books SET author=?,language=?, title=?, price=?,published_year=? WHERE id=?"
            cur.execute(sql,(author, language, title, price, published_year, book_id))
            db_conn.commit()
            return jsonify(updated_book)
        except Exception as e:
            return jsonify({"error": str(e)})

    if request.method == 'DELETE':
        print("Delete Request: ")
        try:
            sql = "DELETE FROM books where id=?"
            res = cur.execute(sql, (book_id,))
            db_conn.commit()
            if res.rowcount:
                return f"The book with id: {id} has been deleted.", 200

            return f"Failed to delete!!.The book with id: {book_id} is not found.", 404

        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == '__main__':
    db = DBHandler()
    db.create_connection()
    db.create_table('books')
    db.close_connection()
    app.run(debug=True)