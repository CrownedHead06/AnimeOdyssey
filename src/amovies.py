import pandas as pd
import numpy as np
import pickle
import streamlit as st
from pathlib import Path

# read the dataframe
movies = pd.read_csv(Path.cwd()/'datasets/anime_movies.csv')

# read the binary
movies_similarity = pickle.load(open(Path.cwd()/'assets/bin/movies_similarity.pkl', 'rb'))

# to choose a anime from dropdown
def chooseMovie(movies: pd.DataFrame) -> str:
    titles = movies.title.sort_values().values
    titles = np.insert(titles, 0, '')

    selectedAnime = st.selectbox(
        'Type or Select an Anime from the dropdown',
        titles
    )

    return selectedAnime

# recommend anime based on input
def recommendMovies() -> None:
    movie = chooseMovie(movies)
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(movies_similarity[index])),reverse=True,key = lambda x: x[1])

    for i in distances[1:16]:
        title = movies.iloc[i[0]].title
        poster = movies.iloc[i[0]].poster
        description = movies.iloc[i[0]].description
        url = movies.iloc[i[0]].link

        # divide the page into 2 columns
        col1, col2 = st.columns(2)

        # print the attributes on the page
        with col1:
            card_style = (
                    f"border-radius: 15px; box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.2); padding: 15px;"
                    f"background-color: white; display: inline-block; width: 250px"
                )

            st.markdown(
                f'<a href="{poster}" target="_blank">'
                f'<div style="{card_style}">'
                f'<img src="{poster}" width="100%" alt="Clickable Image">'
                f'</div></a>',
                unsafe_allow_html=True,
            )
            # st.image(poster, width=200)
        with col2:
            styled_title = f'<a href="{url}" style="color:red; font-size:1.2em;">{title}</a>'
            st.markdown(styled_title, unsafe_allow_html=True)
            st.write(description[0:500] + ' ...')
