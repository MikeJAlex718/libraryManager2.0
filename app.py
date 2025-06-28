#JAM
#6/25/2025
#Provides the app/website functionality

from flask import Flask, render_template, request, redirect, url_for
from libraryManager import LibraryManager
from dotenv import load_dotenv
from book import Book
import os

SUPABASE_URL = "https://yhpuxmffbbnwmojhuaky.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlocHV4bWZmYmJud21vamh1YWt5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5NTQ3NzMsImV4cCI6MjA2NjUzMDc3M30.OvzWIPNfbj4AcuKT0f8P7fTJZXdYdStnE9xz71je8LE"

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
library = LibraryManager()

@app.route('/')
def index():
    library.loadLibrary()
    print("Books and their IDs:")
    return render_template('index.html', books=library.books)

#Adds book into the library
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        try:
            year = int(request.form['year'])
        except ValueError:
            return "Invalid year. Please enter a number.", 400
        
        if year<0 or year>2025:
            return "year must be between 0 and 2025.", 400
        
        didRead = request.form['didRead'].lower()=='true'
        book = Book(title, author, year, didRead)
        library.addBook(book)
        return redirect(url_for("index"))
    
    return render_template('add.html')

#Removes book by ID
@app.route("/delete/<int:bookID>", methods=["POST"])
def delete_book(bookID):
    library.removeBookById(bookID)
    return redirect(url_for("index"))

#Marks the book either unread or read depending on the current read status
@app.route('/toggle-read/<int:bookID>', methods=['POST'])
def toggleRead(bookID):
    for book in library.books:
        if book.id == bookID:
            newStatus = not book.didRead
            response = supabase.table("books").update({"didRead":newStatus}).eq("id", bookID).execute()
            
            if response.data and len(response.data)>0:
                book.didRead = newStatus
            break
    return redirect(url_for('index'))

#Searches for the book
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_result = None
    if request.method == 'POST':
        title = request.form['title']
        search_result = library.findBook(title)
    
    return render_template('search.html', search_result=search_result)

#Removes all the books in library
@app.route("/clear", methods=["POST"])
def clear():
    library.clearAllBooks()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)