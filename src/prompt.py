import pandas as pd
import pickle
from pathlib import Path
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# read binary and dataset 
animes = pd.read_csv(Path.cwd()/'datasets/anime_series.csv')
vectors = pickle.load(open(Path.cwd()/'assets/bin/vectors.pkl', 'rb'))

# take description as input from user
def userInput():
    # text area
    describe = st.text_area('Describe an Anime in your own words to get recommendations')
    
    # convert description to vector
    embeddings = model.encode(describe)

    # check similarity b/w description of user and all animes
    similarity = cosine_similarity(embeddings.reshape(1, 384), vectors)

    return similarity


# recommend animes accd. to user description
def recommendAnimes() -> None:
    similarity_score = userInput()

    # sorting by similarity score
    distances = sorted(list(enumerate(similarity_score[0])), reverse=True, key=lambda x: x[1])

    # time to display best match according to prompt
    if st.button('Recommend'):
        for i in distances[0:15]:
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
