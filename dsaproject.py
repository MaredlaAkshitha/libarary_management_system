import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import font


class Library:
    def __init__(self, book_name, author, pages, price, borrower=None):
        self.book_name = book_name
        self.author = author
        self.pages = pages
        self.price = price
        self.borrower = borrower


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x500")
        self.root.title("Library Management System")

        self.default_font = font.Font(size=15)

        self.lib = []
        self.count = 0

        self.initialize_sample_books()

        self.add_button = tk.Button(root, text="Add Book", command=self.add_book, font=self.default_font)
        self.add_button.pack(pady=10)

        self.display_button = tk.Button(root, text="Display Books", command=self.display_books, font=self.default_font)
        self.display_button.pack(pady=10)

        self.author_button = tk.Button(root, text="List Books by Author", command=self.list_books_by_author, font=self.default_font)
        self.author_button.pack(pady=10)

        self.borrow_button = tk.Button(root, text="Borrow Book", command=self.borrow_book, font=self.default_font)
        self.borrow_button.pack(pady=10)

        self.return_button = tk.Button(root, text="Return Book", command=self.return_book, font=self.default_font)
        self.return_button.pack(pady=10)

        self.count_button = tk.Button(root, text="Count Books", command=self.count_books, font=self.default_font)
        self.count_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit, font=self.default_font)
        self.exit_button.pack(pady=10)

    def initialize_sample_books(self):
        sample_books = [
            Library("The Great Gatsby", "F. Scott Fitzgerald", 180, 10.99),
            Library("1984", "George Orwell", 328, 8.99),
            Library("To Kill a Mockingbird", "Harper Lee", 281, 7.99),
            Library("Pride and Prejudice", "Jane Austen", 279, 6.99),
            Library("The Catcher in the Rye", "J.D. Salinger", 277, 9.99)
        ]
        self.lib.extend(sample_books)
        self.count += len(sample_books)

    def add_book(self):
        book_name = simpledialog.askstring("Input", "Enter book name:", parent=self.root)
        author = simpledialog.askstring("Input", "Enter author name:", parent=self.root)
        pages = simpledialog.askinteger("Input", "Enter number of pages:", parent=self.root)
        price = simpledialog.askfloat("Input", "Enter price:", parent=self.root)

        if book_name and author and pages is not None and price is not None:
            self.lib.append(Library(book_name, author, pages, price))
            self.count += 1
            messagebox.showinfo("Success", "Book added successfully!", parent=self.root)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.", parent=self.root)

    def display_books(self):
        if not self.lib:
            messagebox.showinfo("Info", "No books available.", parent=self.root)
            return

        table_window = tk.Toplevel(self.root)
        table_window.title("Books List")
        table_window.geometry("700x400")

        columns = ("Book Name", "Author", "Pages", "Price", "Borrower")
        tree = ttk.Treeview(table_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for book in self.lib:
            tree.insert("", "end", values=(
                book.book_name, book.author, book.pages, book.price, book.borrower or "Available"
            ))

        tree.pack(fill="both", expand=True)

    def list_books_by_author(self):
        author = simpledialog.askstring("Input", "Enter author name:", parent=self.root)
        if author:
            books_by_author = [book for book in self.lib if book.author == author]
            if books_by_author:
                self.display_books_in_table(f"Books by {author}", books_by_author)
            else:
                messagebox.showinfo("Info", "No books found by this author.", parent=self.root)
        else:
            messagebox.showwarning("Input Error", "Please enter an author name.", parent=self.root)

    def display_books_in_table(self, title, books):
        table_window = tk.Toplevel(self.root)
        table_window.title(title)
        table_window.geometry("700x400")

        columns = ("Book Name", "Author", "Pages", "Price", "Borrower")
        tree = ttk.Treeview(table_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for book in books:
            tree.insert("", "end", values=(
                book.book_name, book.author, book.pages, book.price, book.borrower or "Available"
            ))

        tree.pack(fill="both", expand=True)

    def borrow_book(self):
        book_name = simpledialog.askstring("Input", "Enter book name to borrow:", parent=self.root)
        borrower = simpledialog.askstring("Input", "Enter your name:", parent=self.root)

        if book_name and borrower:
            for book in self.lib:
                if book.book_name == book_name:
                    if book.borrower is None:
                        book.borrower = borrower
                        messagebox.showinfo("Success", f"Book '{book_name}' borrowed successfully by {borrower}.", parent=self.root)
                        return
                    else:
                        messagebox.showinfo("Info", f"Book '{book_name}' is already borrowed by {book.borrower}.", parent=self.root)
                        return
            messagebox.showinfo("Info", f"Book '{book_name}' not found.", parent=self.root)
        else:
            messagebox.showwarning("Input Error", "Please enter both book name and borrower name.", parent=self.root)

    def return_book(self):
        book_name = simpledialog.askstring("Input", "Enter book name to return:", parent=self.root)

        if book_name:
            for book in self.lib:
                if book.book_name == book_name:
                    if book.borrower is not None:
                        book.borrower = None
                        messagebox.showinfo("Success", f"Book '{book_name}' returned successfully.", parent=self.root)
                        return
                    else:
                        messagebox.showinfo("Info", f"Book '{book_name}' is not currently borrowed.", parent=self.root)
                        return
            messagebox.showinfo("Info", f"Book '{book_name}' not found.", parent=self.root)
        else:
            messagebox.showwarning("Input Error", "Please enter the book name.", parent=self.root)

    def count_books(self):
        messagebox.showinfo("Count", f"No of books in library: {self.count}", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
