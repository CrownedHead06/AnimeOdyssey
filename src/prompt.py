import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import streamlit as st
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# read and merge dataset 
series = pd.read_csv(Path.cwd()/'datasets/anime_series.csv')
movies = pd.read_csv(Path.cwd()/'datasets/anime_movies.csv')
animes = series.append(movies)

# read binary
vectors = pickle.load(open(Path.cwd()/'assets/bin/dembeddings.pkl', 'rb'))

# making cosine_similarity function
def cosine_similarity(embeddings, vectors):
    similarity = list()
    for vector in vectors:
        dot_product = np.dot(embeddings, vector)
        norm1 = np.linalg.norm(embeddings)
        norm2 = np.linalg.norm(vector)
        similarity.append(dot_product / (norm1 * norm2))
    return np.array(similarity)

# take description as input from user
def userInput():
    # text area
    describe = st.text_area('Describe an Anime in your own words to get recommendations')
    
    # convert description to vector
    embeddings = model.encode(describe)

    # check similarity b/w description of user and all animes
    similarity = cosine_similarity(embeddings.reshape(1, 384), vectors).reshape(1, animes.shape[0])

    return similarity


# recommend animes accd. to user description
def recommendAnimes() -> None:
    similarity_score = userInput()

    # sorting by similarity score
    distances = sorted(list(enumerate(similarity_score[0])), reverse=True, key=lambda x: x[1])

    # time to display best match according to prompt
    if st.button('Recommend'):
        for i in distances[0:15]:
            try:
                title = animes.iloc[i[0]].title
                poster = animes.iloc[i[0]].poster
                description = animes.iloc[i[0]].description
                url = animes.iloc[i[0]].link

                # divide the page into 2 columns
                col1, col2 = st.columns(2)

                # print the attributes on the page
                with col1:
                    st.image(poster, width=200)
                with col2:
                    styled_title = f'<a href="{url}" style="color:red; font-size:1.2em;">{title}</a>'
                    st.markdown(styled_title, unsafe_allow_html=True)
                    st.write(description[0:400] + ' ...')
            except:
                continue
