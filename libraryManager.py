#JAM
#6/25/2025
#Stores several books properties and provides other useful methods

from dotenv import load_dotenv
import os
from book import Book

load_dotenv()

SUPABASE_URL = "https://your_supbase_reference_id.supabase.co"
SUPABASE_KEY = "your_supabase_anon_key"

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class LibraryManager:
    def __init__(self, books=None):
        self.books = []
        
        if books is not None:
            for curBook in books:
                self.books.append(curBook)
    
    #Displays all books' information in the library
    def displayAll(self):
        if len(self.books) == 0:
            print("No book(s) to display\n")
        
        for book in self.books:
            print(book.toString())
    
    #Adds the book parameter at the end of the list  
    def addBook(self,book):
        response = supabase.table("books").insert({
            "title": book.getTitle(),
            "author": book.getAuthor(),
            "year": book.getYear(),
            "didRead": book.getRead()
        }).execute()
        
        if response.data and len(response.data) > 0:
            book.id = response.data[0].get("id")
        
        self.books.append(book)
        print("Successfully Added your Book!\n")
    
    #Removes a book from the library by id
    def removeBookById(self, bookID):
        response = supabase.table("books").delete().eq("id", bookID).execute()
        
        if response.data and len(response.data)>0:
            self.books = [b for b in self.books if b.id != bookID]
            print(f"Successfully removed book with ID: {bookID}!\n")
        else:
            print(f"Book with ID: {bookID} not found.\n")
            
    #Sorts the books in the library by year and title
    def sortBooks(self):
        self.books.sort(key=lambda book: (-book.getYear(), book.getTitle()))
        print("Successfully Sorted your Library!\n")
    
    #Finds if the book parameter exists, returns if does
    def findBook(self, targetTitle):
        for book in self.books:
            if book.getTitle() == targetTitle:
                return (f"{book.getTitle()} is in the Library!\n")
        
        return (f"{targetTitle} not Found\n")
        
    #Loads data from SupaBase, storing several books' information
    def loadLibrary(self):
        response = supabase.table("books").select("*").execute()
        self.books = []
        
        for record in response.data:
            book = Book.from_dict(record)
            self.books.append(book)
        
        self.sortBooks()
        print("Successfully loaded library from database!\n")
        
    #Removes all the books in the library
    def clearAllBooks(self):
        response = supabase.table('books').delete().neq("id",0).execute()
        
        if response.data is not None:
            self.books=[]
            print("All books cleared successfully!\n")
        else:
            print("Failed to clear books.\n")
