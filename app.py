# import pickle
# import streamlit as st
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import pandas as pd

# # Spotify API credentials
# CLIENT_ID = "7907cb3370254544a1443ba57ea8a1d0"
# CLIENT_SECRET = "2dab789122454f40b8978d80d1bf20cf"

# # Initialize the Spotify client
# client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # Load the CSV file
# music_data = pd.read_csv('D:\shadab\Diploma Projects\project sem-5\MLproject\Music_Recommender_System-main\Music_Recommender_System-main/spotify_millsongdata.csv')

# # Function to get the album cover URL from Spotify
# def get_song_album_cover_url(song_name, artist_name):
#     search_query = f"track:{song_name} artist:{artist_name}"
#     results = sp.search(q=search_query, type="track")

#     if results and results["tracks"]["items"]:
#         track = results["tracks"]["items"][0]
#         album_cover_url = track["album"]["images"][0]["url"]
#         return album_cover_url
#     else:
#         # Default image if not found
#         return "https://i.postimg.cc/0QNxYz4V/social.png"

# # Function to get lyrics (limited to 3 lines)
# def get_song_lyrics(song_name):
#     song_entry = music_data[music_data['song'] == song_name]
#     if not song_entry.empty:
#         lyrics = song_entry['text'].values[0]
#         # Limit to 3 lines (or 3 sentences)
#         return "\n".join(lyrics.splitlines()[:3])
#     else:
#         return "Lyrics not found."

# # Function to get recommendations
# def recommend(song):
#     index = music[music['song'] == song].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
#     recommended_music_names = []
#     recommended_music_posters = []
    
#     for i in distances[1:6]:
#         artist = music.iloc[i[0]].artist
#         song_name = music.iloc[i[0]].song
#         recommended_music_posters.append(get_song_album_cover_url(song_name, artist))
#         recommended_music_names.append(song_name)
    
#     return recommended_music_names, recommended_music_posters

# # Streamlit app layout
# st.header('Music Recommender System')

# # Load pre-trained model data
# music = pickle.load(open('df.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # Dropdown for selecting a song
# music_list = music['song'].values
# selected_song = st.selectbox(
#     "Type or select a song from the dropdown",
#     music_list
# )

# # Button to display recommendations
# if st.button('Show Recommendation'):
#     recommended_music_names, recommended_music_posters = recommend(selected_song)
    
#     # Loop to display the recommended songs and posters with lyrics
#     for i in range(5):
#         col1, col2 = st.columns([1, 3])  # Column 1 for image, Column 2 for text
#         with col1:
#             st.image(recommended_music_posters[i], width=150)  # Set width to 150 pixels for album cover
#         with col2:
#             st.write(f"*{recommended_music_names[i]}*")  # Display song name next to the image
#             lyrics = get_song_lyrics(recommended_music_names[i])
#             # Display lyrics in quotation marks
#             st.write(f'"{lyrics}"')  # Add quotation marks around lyrics


import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
CLIENT_ID = "7907cb3370254544a1443ba57ea8a1d0"
CLIENT_SECRET = "2dab789122454f40b8978d80d1bf20cf"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Streamlit app layout
st.title("Music Recommender System")

# Step 1: Upload CSV file
st.header("Upload Music Dataset")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        music_data = pd.read_csv(uploaded_file)
        st.success("CSV file loaded successfully!")
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        st.stop()
else:
    st.warning("Please upload a CSV file to proceed.")
    st.stop()

# Ensure required columns are present
required_columns = {'artist', 'song', 'text'}
if not required_columns.issubset(music_data.columns):
    st.error("The uploaded CSV file does not contain the required columns: artist, song, text.")
    st.stop()

# Step 2: Load pre-trained model files
try:
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    st.success("Pre-trained model files loaded successfully!")
except FileNotFoundError:
    st.error("Model files (df.pkl or similarity.pkl) are missing. Please ensure these files are in the same directory as the app.")
    st.stop()

# Function to get the album cover URL from Spotify
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        # Default image if not found
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to get lyrics (limited to 3 lines)
def get_song_lyrics(song_name):
    song_entry = music_data[music_data['song'] == song_name]
    if not song_entry.empty:
        lyrics = song_entry['text'].values[0]
        # Limit to 3 lines
        return "\n".join(lyrics.splitlines()[:3])
    else:
        return "Lyrics not found."

# Function to get recommendations
def recommend(song):
    try:
        index = music[music['song'] == song].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    except IndexError:
        st.error("The selected song is not in the dataset.")
        st.stop()
    
    recommended_music_names = []
    recommended_music_posters = []
    
    for i in distances[1:6]:  # Top 5 recommendations
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        recommended_music_posters.append(get_song_album_cover_url(song_name, artist))
        recommended_music_names.append(song_name)
    
    return recommended_music_names, recommended_music_posters

# Step 3: Select a song from the dropdown
st.header("Find Recommendations")
music_list = music['song'].values
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

# Step 4: Show recommendations
if st.button("Show Recommendation"):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    
    # Display recommendations
    for i in range(5):
        col1, col2 = st.columns([1, 3])  # Column 1 for image, Column 2 for text
        with col1:
            st.image(recommended_music_posters[i], width=150)  # Set width to 150 pixels for album cover
        with col2:
            st.write(f"*{recommended_music_names[i]}*")  # Display song name
            lyrics = get_song_lyrics(recommended_music_names[i])
            st.write(f'"{lyrics}"')  # Display lyrics in quotation marks
