from flask import Flask, jsonify, request, Response, json
from settings import *
from BookModel import *

# app = Flask(__name__)


print(__name__)


# books = [
#     {
#         "name": "Green Egg",
#         "price": 256.99,
#         "isbn": 1235339935
#     },
#     {
#         "name": "Red Egg",
#         "price": 125.99,
#         "isbn": 3235339935
#     }
# ]

@app.route('/')
def hello_world():
    return 'Book Store'


@app.route('/books', methods=['GET'])
def get_books():
    # return jsonify({"books": books})
    return jsonify({"books": Book.get_all_books()})



@app.route('/books/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    # return_value = {}
    # for book in books:
    #     if (book["isbn"] == isbn):
    #         return_value = {
    #             "name": book["name"],
    #             "price": book["price"],
    #             "isbn": book["isbn"],
    #         }
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()

    if validBookObject(request_data):
        # new_book = {
        #     "name": request_data["name"],
        #     "price": request_data["price"],
        #     "isbn": request_data["isbn"],
        # }
        # books.insert(0,new_book)
        Book.add_book(request_data["name"],request_data["price"],request_data["isbn"])
        response = Response("", 201, mimetype='application/json')
        response.headers["Location"] = "/books/"+ str(request_data["isbn"])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this..."
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


def valid_put_request_data(request_data):
    if ("name" in request_data and "price" in request_data):
        return True
    else:
        return False

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()

    # if (not valid_put_request_data(request_data)):
    #     invalidBookObjectErrorMsg = {
    #         "error": "Valid book object must be passed in the request",
    #         "helpString": "Data passed is similar to this..."
    #     }
    #     response = Response(json.dump(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
    #     return response
    #
    # new_book = {
    #     "name": request_data["name"],
    #     "price": request_data["price"],
    #     "isbn": isbn
    # }
    #
    # i = 0
    # for book in books:
    #     currentIsbn = book["isbn"]
    #     if(currentIsbn == isbn):
    #         books[i] = new_book
    #     i += 1
    Book.replace_book(isbn, request_data["name"], request_data["price"])
    response = Response("", status = 204)

    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()

    if ("name" in request_data):
        Book.update_book_name(isbn, request_data["name"])
    if ("price" in request_data):
        Book.update_book_price(isbn, request_data["price"])

    response = Response("", status=204)
    response.headers["Location"] = "/books/"+str("isbn")

    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    Book.delete_book(isbn)
    invalidbookObjectErrorMsg = {
        "error": "Book with this ISBN was not found"
    }
    response = Response(json.dump(invalidbookObjectErrorMsg), status=401, mimetype="application/jon")
    return response


# ----------------------------------------------------------
if __name__ == '__main__':
    app.run()
