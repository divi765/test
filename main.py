

import mysql.connector as sql
from datetime import date
conn = sql.connect(
    host="localhost", 
    user="root", 
    password="", 
    database="library")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS books(
book_id INT PRIMARY KEY,
title VARCHAR(100),
author VARCHAR(100),
status VARCHAR(20))
"""
               )

cursor.execute("""CREATE TABLE IF NOT EXISTS issue(
issue_id INT PRIMARY KEY AUTO_INCREMENT,
book_id INT,
student_name VARCHAR(100),
issue_date DATE,
return_date DATE,
FOREIGN KEY (book_id) REFERENCES books(book_id))
"""
               )
conn.commit()
print("Database and Tables are created successfully.")

# library management functions

def add_book():
    bid = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    status = "Available"
    cursor.execute("INSERT INTO books VALUES (%s, %s, %s, %s)", (bid, title, author, status))
    conn.commit()
    print("Book added successfully.")

def Display_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if not books:
        print("No books found.")
        return
    print("Book ID | Title | Author | Status")
    for book in books:
        print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
        # code changed

def issue_book():
    bid = int(input("Enter Book ID to issue: "))
    student_name = input("Enter Student Name: ")
    cursor.execute("SELECT status FROM books WHERE book_id = %s", (bid,))
    result = cursor.fetchone()
    if result is None:
        print("Book not found.")
        return
    if result and result[0] == "Available":
        cursor.execute("INSERT INTO issue (book_id, student_name, issue_date) VALUES (%s, %s, %s)", (bid, student_name, date.today()))
        cursor.execute("UPDATE books SET status = 'Issued' WHERE book_id = %s", (bid,))
        conn.commit()
        print("Book issued successfully.")
    elif result:
        print("Book is not available for issue.")
    else:
        print("Book id not found.")


def return_book():
    bid = int(input("Enter Book ID to return: "))
    cursor.execute("SELECT status FROM books WHERE book_id = %s", (bid,))
    result = cursor.fetchone()
    if result is None:
        print("Book not found.")
        return
    if result:
        cursor.execute("UPDATE issue SET return_date = %s WHERE book_id = %s AND return_date IS NULL", (date.today(), bid))
        cursor.execute("UPDATE books SET status = 'Available' WHERE book_id = %s", (bid,))
        conn.commit()
        print("Book returned successfully.")
    else:
        print("Book is not issued or not found.")

def delete_book():
    bid = int(input("Enter Book ID to delete: "))
    cursor.execute("DELETE FROM books WHERE book_id = %s", (bid,))
    conn.commit()
    print("Book deleted successfully.")

def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Delete Book")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_book()
        elif choice == '2':
            Display_books()
        elif choice == '3':
            issue_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            print("Thank you for using the Library Management System.")
        else:
            print("Invalid choice. Please try again.")