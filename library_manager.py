import streamlit as st  # Streamlit ko import karna taake UI render ho sake, agar yeh na ho toh app run nahi hogi
import json  # JSON library import kar rahe hain taake file handling ho sake, agar yeh na ho toh library save/load nahi hogi

# File name for saving/loading the library
LIBRARY_FILE = "library.json"  # Yeh file library data store karne ke liye istemal hogi, agar yeh na ho toh data persist nahi hoga

def load_library():  # Function jo library ko file se load karega
    """Load the library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:  # File read mode mein open kar rahe hain
            return json.load(file)  # File ka data JSON format mein load kar rahe hain
    except (FileNotFoundError, json.JSONDecodeError):  # Agar file na mile ya data corrupt ho toh
        return []  # Empty list return hogi, warna program crash ho sakta hai

def save_library(library):  # Function jo library ko file mein save karega
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:  # File write mode mein open kar rahe hain
        json.dump(library, file, indent=4)  # JSON format mein data likh rahe hain taake structured ho

def add_book(library, title, author, year, genre, read):  # Function jo naye books library mein add karega
    """Add a new book to the library."""
    library.append({  # Library list mein ek naya dictionary object add kar rahe hain
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read
    })
    save_library(library)  # Data ko file mein save kar rahe hain taake persist rahe
    st.success("📚 Book added successfully! 🎉")  # Success message dikhayenge

def remove_book(library, title):  # Function jo book remove karega title ke basis par
    """Remove a book from the library by title."""
    for book in library:
        if book["Title"].lower() == title.lower():  # Title case insensitive comparison
            library.remove(book)  # Matching book remove kar rahe hain
            save_library(library)  # File update kar rahe hain
            st.success("🗑️ Book removed successfully! ✨")  # Success message dikhayenge
            return
    st.error("❌ Book not found.")  # Agar book nahi mili toh error message

def search_books(library, keyword, search_by):  # Function jo books search karega
    """Search for books by title or author."""
    if search_by == "Title":
        return [book for book in library if keyword.lower() in book["Title"].lower()]  # Title based search
    elif search_by == "Author":
        return [book for book in library if keyword.lower() in book["Author"].lower()]  # Author based search
    return []  # Agar kuch na mile toh empty list

def display_statistics(library):  # Function jo statistics dikhayega
    """Display statistics about the library."""
    total_books = len(library)  # Total books count
    read_books = sum(1 for book in library if book["Read"])  # Read books count
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0  # Read percentage calculate kar rahe hain
    return total_books, percentage_read  # Dono values return ho rahi hain

# Streamlit UI - Facebook Theme
st.set_page_config(page_title="Personal Library Manager", page_icon="📘", layout="wide")  # Facebook color scheme ka UI set karna
st.markdown("""
    <style>
    body {
        background: #ffffff; /* Pure white background */
        color: #003366; /* Dark blue text */
    }
    .stApp {
        background: #0056b3; /* Proper blue background */
        color: #ffffff; /* White text */
    }
</style>

""", unsafe_allow_html=True)

st.title("📘 Personal Library Manager 💙")  # Title dikhana

# Load library data
library = load_library()  # Library data load kar rahe hain taake existing books dikhen

# Sidebar menu with Facebook-themed emojis
menu = st.sidebar.radio("📌 Menu", ["➕ Add a Book", "🗑️ Remove a Book", "🔍 Search Books", "📚 View Library", "📊 Statistics"])  # Sidebar menu options

if menu == "➕ Add a Book":
    st.header("📖 Add a Book 📘")  # Section header
    title = st.text_input("📌 Title")  # Title input field
    author = st.text_input("👤 Author")  # Author input field
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, step=1)  # Year input field
    genre = st.text_input("📖 Genre")  # Genre input field
    read = st.checkbox("✅ Have you read this book?")  # Read status checkbox
    if st.button("📥 Add Book"):  # Button to add book
        add_book(library, title, author, year, genre, read)  # Function call

elif menu == "🗑️ Remove a Book":
    st.header("❌ Remove a Book")
    title = st.text_input("📌 Enter the title of the book to remove")  # Title input
    if st.button("🗑️ Remove Book"):  # Button to remove book
        remove_book(library, title)

elif menu == "🔍 Search Books":
    st.header("🔎 Search for a Book")
    search_by = st.radio("📌 Search by", ["📖 Title", "👤 Author"])  # Search type selection
    keyword = st.text_input("🔍 Enter search keyword")  # Keyword input
    if st.button("🔎 Search"):  # Button to start search
        results = search_books(library, keyword, search_by)  # Function call
        if results:
            for book in results:
                status = "✅ Read" if book["Read"] else "📖 Unread"  # Read/Unread status
                st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
        else:
            st.warning("⚠️ No matching books found.")

elif menu == "📚 View Library":
    st.header("📚 Your Library")
    if library:
        for book in library:
            status = "✅ Read" if book["Read"] else "📖 Unread"
            st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
    else:
        st.warning("📭 Your library is empty.")

elif menu == "📊 Statistics":
    st.header("📊 Library Statistics")
    total_books, percentage_read = display_statistics(library)  # Stats function call
    st.metric(label="📚 Total Books", value=total_books)  # Total books display
    st.metric(label="✅ Books Read (%)", value=f"{percentage_read:.2f}%")  # Read percentage display