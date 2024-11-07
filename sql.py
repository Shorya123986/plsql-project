import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Connect to (or create) the database file
conn = sqlite3.connect('library_management.db')
cursor = conn.cursor()

# Create tables if they don't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    course TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS BookIssues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    issue_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
);
""")

conn.commit()

# Function to add a new student
def add_student():
    student_id = entry_student_id.get()
    student_name = entry_student_name.get()
    course = entry_student_course.get()
    
    if student_id and student_name and course:
        cursor.execute("INSERT INTO Students (student_id, student_name, course) VALUES (?, ?, ?)",
                       (student_id, student_name, course))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully.")
        entry_student_id.delete(0, tk.END)
        entry_student_name.delete(0, tk.END)
        entry_student_course.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Function to add a new book
def add_book():
    book_id = entry_book_id.get()
    title = entry_book_title.get()
    author = entry_book_author.get()
    
    if book_id and title and author:
        cursor.execute("INSERT INTO Books (book_id, title, author) VALUES (?, ?, ?)",
                       (book_id, title, author))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully.")
        entry_book_id.delete(0, tk.END)
        entry_book_title.delete(0, tk.END)
        entry_book_author.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Function to issue a book
def issue_book():
    student_id = entry_issue_student_id.get()
    book_id = entry_issue_book_id.get()
    issue_date = datetime.now().strftime("%Y-%m-%d")  # Current date
    
    if student_id and book_id:
        cursor.execute("INSERT INTO BookIssues (student_id, book_id, issue_date) VALUES (?, ?, ?)",
                       (student_id, book_id, issue_date))
        conn.commit()
        messagebox.showinfo("Success", f"Book ID {book_id} issued to Student ID {student_id} on {issue_date}.")
        entry_issue_student_id.delete(0, tk.END)
        entry_issue_book_id.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Function to show data from a table
def show_table(table_name):
    # Create a new window to display the table data
    window = tk.Toplevel(root)
    window.title(f"{table_name} Table")
    
    # Treeview widget to display the table contents
    tree = ttk.Treeview(window)
    tree.grid(row=0, column=0, padx=10, pady=10)
    
    # Define columns based on the table name
    if table_name == "Students":
        cursor.execute("SELECT * FROM Students")
        columns = ["Student ID", "Name", "Course"]
    elif table_name == "Books":
        cursor.execute("SELECT * FROM Books")
        columns = ["Book ID", "Title", "Author"]
    elif table_name == "BookIssues":
        cursor.execute("SELECT * FROM BookIssues")
        columns = ["Issue ID", "Student ID", "Book ID", "Issue Date"]
    
    # Set up the columns in the Treeview
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)
    
    # Insert data into the Treeview
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# Set up the Tkinter GUI
root = tk.Tk()
root.title("Library Management System")

# Main Title
title_label = tk.Label(root, text="Library Management System", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Student Frame
frame_student = tk.LabelFrame(root, text="Add New Student")
frame_student.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(frame_student, text="Student ID:").grid(row=0, column=0)
entry_student_id = tk.Entry(frame_student)
entry_student_id.grid(row=0, column=1)

tk.Label(frame_student, text="Name:").grid(row=1, column=0)
entry_student_name = tk.Entry(frame_student)
entry_student_name.grid(row=1, column=1)

tk.Label(frame_student, text="Course:").grid(row=2, column=0)
entry_student_course = tk.Entry(frame_student)
entry_student_course.grid(row=2, column=1)

tk.Button(frame_student, text="Add Student", command=add_student).grid(row=3, columnspan=2, pady=5)

# Book Frame
frame_book = tk.LabelFrame(root, text="Add New Book")
frame_book.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(frame_book, text="Book ID:").grid(row=0, column=0)
entry_book_id = tk.Entry(frame_book)
entry_book_id.grid(row=0, column=1)

tk.Label(frame_book, text="Title:").grid(row=1, column=0)
entry_book_title = tk.Entry(frame_book)
entry_book_title.grid(row=1, column=1)

tk.Label(frame_book, text="Author:").grid(row=2, column=0)
entry_book_author = tk.Entry(frame_book)
entry_book_author.grid(row=2, column=1)

tk.Button(frame_book, text="Add Book", command=add_book).grid(row=3, columnspan=2, pady=5)

# Issue Book Frame
frame_issue = tk.LabelFrame(root, text="Issue Book")
frame_issue.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(frame_issue, text="Student ID:").grid(row=0, column=0)
entry_issue_student_id = tk.Entry(frame_issue)
entry_issue_student_id.grid(row=0, column=1)

tk.Label(frame_issue, text="Book ID:").grid(row=1, column=0)
entry_issue_book_id = tk.Entry(frame_issue)
entry_issue_book_id.grid(row=1, column=1)

tk.Button(frame_issue, text="Issue Book", command=issue_book).grid(row=2, columnspan=2, pady=5)

# Buttons to show each table
frame_show = tk.Frame(root)
frame_show.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

tk.Button(frame_show, text="Show Students", command=lambda: show_table("Students")).grid(row=0, column=0, padx=5)
tk.Button(frame_show, text="Show Books", command=lambda: show_table("Books")).grid(row=0, column=1, padx=5)
tk.Button(frame_show, text="Show Issued Books", command=lambda: show_table("BookIssues")).grid(row=0, column=2, padx=5)

# Run the Tkinter main loop
root.mainloop()

# Close the connection after the GUI is closed
conn.close()





