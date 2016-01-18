import json
class User(object):
  uid = 1
  def __init__(self, name = ""):
    # self.uid is set to autoincrement
    self.uid = User.uid
    User.uid += 1

    self.name = name
    self.books = []

  def has_book(self, book_id):
    return (book_id in [book.uid for book in self.books])

  def remove_book(self, book_uid):
    self.books = filter(lambda book: book.uid != book_uid, self.books)

  def add_book(self, book):
    self.books.append(book)

class Book(object):
  uid = 1
  def __init__(self, title = "", author = ""):
    # self.uid is set to autoincrement
    self.uid = Book.uid
    Book.uid += 1

    self.title = title
    self.author = author
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
import re
def get_status(library, cmd):
  verb, url_package = cmd.split(' ', 1)
  if ' ' in url_package:
    url, package = url_package.split(' ', 1)
  else:
    url = url_package
    package = ''

  # --- Helper functions start --- #
  def _library_book_ids(library):
    return [book.uid for book in library.books]

  def _library_user_ids(library):
    return [user.uid for user in library.users]

  def _library_book(library, book_id):
    return [book for book in library.books if book.uid == book_id][0]

  def _library_user(library, user_id):
    return [user for user in library.users if user.uid == user_id][0]

  def _user_book_ids(user):
    return [book.uid for book in user.books]

  def _user_book(user, book_id):
    return [book for book in user.books if book.uid == book_id][0]
  # ---  Helper functions end  --- #

  def get_books(verb, package):
    if verb == 'GET':
      return 200
    elif verb == 'POST':
      if not package: return 400
      try:
        attrs = package.split('&')
        args = {attr.split('=')[0]:attr.split('=')[1] for attr in attrs}
        # TODO: Validation
        book = Book(**args)
        library.add_book(book)
      except ValueError:
        return 400
      return 200
    else:
      return 405

  def get_book(verb, package, book_id):
    if verb == 'GET':
      if book_id not in _library_book_ids(library):
        return 404
      else:
        return 200
    elif verb == 'PUT':
      if not package:
        return 400
      if book_id not in _library_book_ids(library):
        return 404
      else:
        book = _library_book(library, book_id)
        try:
          attrs = package.split('&')
          args = {attr.split('=')[0]:attr.split('=')[1] for attr in attrs}
          for arg in args:
            setattr(book, arg, args[arg])
        except ValueError:
          return 400
        return 200
    else:
      return 405

  def get_users(verb, package):
    if verb == 'GET':
      return 200
    elif verb == 'POST':
      if not package: return 400
      try:
        attrs = package.split('&')
        args = {attr.split('=')[0]:attr.split('=')[1] for attr in attrs}
        # TODO: Validation
        user = User(**args)
        library.add_user(user)
      except ValueError:
        return 400
      return 200
    else:
      return 405

  def get_user(verb, package, user_id):
    if verb == 'GET':
      if user_id not in _library_user_ids(library):
        return 404
      else:
        return 200
    elif verb == 'PUT':
      if not package:
        return 400
      if user_id not in _library_user_ids(library):
        return 404
      else:
        user = _library_user(library, user_id)
        try:
          attrs = package.split('&')
          args = {attr.split('=')[0]:attr.split('=')[1] for attr in attrs}
          # TODO: Validation
          for arg in args:
            setattr(user, arg, args[arg])
        except ValueError:
          return 400
        return 200
    else:
      return 405

  def get_user_books(verb, package, user_id):
    if verb == 'GET':
      if user_id not in _library_user_ids(library):
        return 404
      else:
        return 200
    else:
      return 405

  def get_user_book(verb, package, user_id, book_id):
    if verb == 'GET':
      if user_id not in _library_user_ids(library):
        return 404
      if book_id not in _library_book_ids(library):
        return 404
      user = _library_user(library, user_id)
      if book_id not in _user_book_ids(user):
        return 404
      return 200
    else:
      return 405

  def user_checkout(verb, package, user_id, book_id):
    if verb == 'POST':
      if user_id not in _library_user_ids(library):
        return 404
      if book_id not in _library_book_ids(library):
        return 404
      user = _library_user(library, user_id)
      book = _library_book(library, book_id)
      if book.checkedout == True:
        return 409
      book.checkedout = True
      user.add_book(book)
      return 200
    else:
      return 405

  def user_return(verb, package, user_id, book_id):
    if verb == 'POST':
      if user_id not in _library_user_ids(library):
        return 404
      if book_id not in _library_book_ids(library):
        return 404
      user = _library_user(library, user_id)
      book = _library_book(library, book_id)

      if book_id not in _user_book_ids(user):
        return 404

      book.checkedout = False
      user.remove_book(book)
      return 200
    else:
      return 405


  patterns = {
    r'^/books/?$': get_books,
    r'^/books/(\d+)/?$': get_book,
    r'^/users/?$': get_users,
    r'^/users/(\d+)/?$': get_user,
    r'^/users/(\d+)/books/?$': get_user_books,
    r'^/users/(\d+)/books/(\d+)/?$': get_user_book,
    r'^/users/(\d+)/checkout/(\d+)/?$': user_checkout,
    r'^/users/(\d+)/return/(\d+)/?$': user_return
  }

  for pattern in patterns:
    match = re.match(pattern, url)
    if match:
      params = map(int, match.groups())
      fn = patterns[pattern]
      return fn(verb, package, *params)
      break

  return 200

library = Library()
while True:
  cmd = raw_input()

  if cmd.rstrip() == 'quit': break

  status = get_status(library, cmd)

  print status
  # print library


