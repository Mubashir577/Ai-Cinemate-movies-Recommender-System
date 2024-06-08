import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ttkthemes import ThemedStyle

# Load the data from the CSV file to a pandas dataframe
movies_data = pd.read_csv('movies.csv')

# Feature Selection
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Replace the missing values with a null string
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine all the 5 selected features
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

# Converting the text data to a feature vector
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Getting the similarity scores using cosine similarity
similarity = cosine_similarity(feature_vectors)

# Function to get movie recommendations with links
def get_movie_recommendations_with_links(movie_name):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    
    if not find_close_match:
        messagebox.showinfo("Movie Recommendation", "Movie not found. Please enter a valid movie name.")
        return []
    
    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    recommended_movies_with_links = []
    for i, movie in enumerate(sorted_similar_movies):
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['title'].values[0]
        homepage_link = movies_data[movies_data.index == index]['homepage'].values[0]
        if homepage_link:
            recommended_movies_with_links.append((title_from_index, homepage_link))
        else:
            recommended_movies_with_links.append((title_from_index, None))
        if i >= 30:
            break
    
    return recommended_movies_with_links

# Function to open a link in a web browser
def open_link(link):
    if link:
        webbrowser.open(link)

# Function to handle "Watch" button click
def watch_button_click(link):
    open_link(link)

# Function to handle button click
def on_button_click():
    movie_name = entry.get()
    recommendations = get_movie_recommendations_with_links(movie_name)
    
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    for i, (movie_title, homepage_link) in enumerate(recommendations, start=1):
        watch_button_text = f"Watch {i}"
        watch_button = ttk.Button(result_text, text=watch_button_text, command=lambda link=homepage_link: watch_button_click(link), style="Blue.TButton")
        result_text.window_create(tk.END, window=watch_button)
        result_text.insert(tk.END, f"{i}. {movie_title}\n", "movie_title")
        result_text.tag_configure("movie_title", foreground="#e74c3c", font=("Helvetica", 10, "bold"))
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("CinéMate Intelligent Movie Recommender")

# Create a themed style
style = ThemedStyle(root)
style.set_theme("blue")  # Choose the "blue" theme

# Create and place widgets
label = ttk.Label(root, text="Enter your favorite movie:")
label.pack(pady=10)

entry = ttk.Entry(root, width=30)
entry.pack(pady=10)

button = ttk.Button(root, text="Get Recommendations", command=on_button_click, style="Blue.TButton")
button.pack(pady=20)

result_text = scrolledtext.ScrolledText(root, width=50, height=15, state=tk.DISABLED)
result_text.pack(pady=20)

# Start the GUI event loop
root.mainloop()
