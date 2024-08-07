import pandas as pd
import streamlit as st

MAX_RESULTS = 50  # Limit the number of results displayed

# Function to search for books based on keywords
def search_books(keyword, books_df):
    if keyword:
        results = books_df[
            books_df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
        ]
        return results
    return pd.DataFrame()

# Load Excel data into a DataFrame
books_df = pd.read_excel('books.xlsx')

# Setup the Streamlit interface with custom CSS for black background and smooth card animations
st.markdown(
    """
    <style>
    body {
        background-color: coral;
        color: white;
        font-family: Arial, sans-serif;
    }
    .stApp {
        background-color: #121212;
        color: blue;
    }
    @keyframes colorShift {
        0% {
            background: linear-gradient(145deg, #ff6f61, #ffcc70);
        }
        50% {
            background: linear-gradient(145deg, #ff5722, #ff9800);
        }
        100% {
            background: linear-gradient(145deg, #ff6f61, #ffcc70);
        }
    }
    .card {
        background: linear-gradient(145deg, #ff6f61, #ffcc70);
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        padding: 20px;
        margin: 15px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: #333;
        overflow: hidden; /* Ensure images don't overflow the card */
        position: relative;
        animation: colorShift 4s infinite;
    }
    .card:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5);
        background: linear-gradient(145deg, #ff5722, #ff9800);
        animation: none; /* Remove the color shift animation on hover */
    }
    .card img {
        border-radius: 10px;
        width: 100%;
        height: auto;
        border: 4px solid #ff5722;
        transition: transform 0.3s ease;
    }
    .card img:hover {
        transform: scale(1.05);
    }
    .card-content {
        padding: 10px 0;
    }
    .card h3 {
        color: #fff;
        margin: 0;
    }
    .card p {
        color: #f1f1f1;
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Library Search")

keyword = st.text_input("Enter a keyword to search:")

if st.button("Search"):
    results = search_books(keyword.lower(), books_df)
    if not results.empty:
        displayed_count = 0
        for index, row in results.iterrows():
            if displayed_count >= MAX_RESULTS:
                st.write("...and more")
                break

            # Create a card layout for each result
            card_html = f"""
            <div class="card">
                <div class="card-content">
                    <h3>ID: {row['ID']}</h3>
                    <p><strong>Title:</strong> {row['Title']}</p>
                    <p><strong>Author:</strong> {row['Author']}</p>
                    <p><strong>Genre:</strong> {row['Genre']}</p>
                    <p><strong>Edition:</strong> {row['Edition']}</p>
                    <p><strong>Description:</strong> {row['Description']}</p>
                    """
            if 'Image' in row and pd.notna(row['Image']):
                card_html += f'<img src="{row["Image"]}" alt="Book Image">'
            card_html += "</div></div>"

            st.markdown(card_html, unsafe_allow_html=True)
            displayed_count += 1
    else:
        st.write("No books found matching the keyword.")
