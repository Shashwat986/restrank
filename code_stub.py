import json
class User(object):
  uid = 1
  def __init__(self):
    # self.uid is set to autoincrement
    self.uid = User.uid
    User.uid += 1

    self.name = ""
    self.books = []

  def has_book(self, book_id):
    return (book_id in [book.uid for book in self.books])

  def remove_book(self, book_uid):
    self.books = filter(lambda book: book.uid != book_uid, self.books)

  def add_book(self, book):
    self.books.append(book)

class Book(object):
  uid = 1
  def __init__(self):
    # self.uid is set to autoincrement
    self.uid = Book.uid
    Book.uid += 1

    self.title = ""
    self.author = ""
    self.checkedout = False

class Library(object):
  uid = 1
  def __init__(self):
    # self.uid is set to autoincrement
    self.uid = Library.uid
    Library.uid += 1

    self.users = []
    self.books = []

  def add_user(self, user):
    self.users.append(user)

  def add_book(self, book):
    self.books.append(book)

  def remove_user(self, user_uid):
    self.users = filter(lambda user: user.uid != user_uid, self.users)

  def remove_book(self, book_uid):
    self.books = filter(lambda book: book.uid != book_uid, self.books)

  def __repr__(self):
    obj = {}
    obj['uid'] = self.uid
    obj['books'] = []
    for book in self.books:
      obj['books'].append({
        'uid': book.uid,
        'title': book.title,
        'author': book.author
      })
    obj['users'] = []
    for user in self.users:
      obj['users'].append({
        'uid': user.uid,
        'name': user.name,
        'books': [book.__dict__ for book in user.books]
      })
    return json.dumps(obj)

'''
  Possible Inputs:
  GET /books
  GET /books/1
  DELETE /books/1
  PUT /books/1
  POST /books/
  GET /users
  GET /users/1
  DELETE /users/1
  PUT /users/1
  POST /users
  POST /users/1/checkout/1
  POST /users/1/return/1
  GET /users/1/books
  GET /users/1/books/1


  Response Status Codes:
  200
  400
  403
  404
  405
  409
'''

def get_status(library, cmd):
  return 200

library = Library()
while True:
  cmd = raw_input()

  if cmd.rstrip() == 'quit': break

  status = get_status(library, cmd)

  print status
  # print library


