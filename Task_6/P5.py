class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def borrow_book(self):
        if self.is_available:
            self.is_available = False
            print("Book borrowed successfully.")
        else:
            print("This book is out.")


book1 = Book("Murder at the oriental express", "Agatha Christie")
book1.borrow_book()