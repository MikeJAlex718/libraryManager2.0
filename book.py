#JAM
#6/25/2025
#Stores a book and its information

class Book:
    def __init__(self,title, author, year, didRead, id=None):
        self.title = title
        self.author = author
        self.year = year
        self.didRead = didRead
        self.id=id
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "didRead": self.didRead
        }
        
    #Retrieves the book's information from SupaBase
    @staticmethod
    def from_dict(data):
        return Book(
            title=data["title"],
            author=data["author"],
            year=data["year"],
            didRead=data["didRead"],
            id=data.get("id")
        )
    
    def toString(self):
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, Read: {self.didRead}\n")
    
    def getTitle(self):
        return self.title
    
    def getAuthor(self):
        return self.author
    
    def getYear(self):
        return self.year
    
    def getRead(self):
        return self.didRead
    
    #Marks the book read
    def markRead(self):
        self.didRead = True
    
    #Marks the book unread
    def markUnread(self):
        self.didRead = False