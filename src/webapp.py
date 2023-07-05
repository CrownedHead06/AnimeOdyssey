# import appropriate libraries
import streamlit as st
from PIL import Image
from pathlib import Path

# importing helper files
from aseries import recommendSeries
from amovies import recommendMovies

# page configuration
st.set_page_config(
    page_title='Anime Odyssey',
    page_icon='https://em-content.zobj.net/thumbs/120/apple/354/ninja_1f977.png',
    initial_sidebar_state='expanded'
)

# displaying logo on the sidebar
logo = Image.open(Path.cwd()/'assets/pictures/logo.png')
st.sidebar.image(logo, caption='ANIME ODYSSEY')

# What is Anime Odyssey?
description = """Anime Odyssey is a community originally formed by a passionate otaku who shared his love for anime across various social media platforms. Over time, he recognized a common dilemma among his fellow members - the struggle to find new anime series or movies to watch after finishing their current favorites. To address this issue, he took a bold step and created an anime recommender system.

This system became a beacon of hope for anime enthusiasts who often found themselves at a loss for what to watch next. By utilizing his own experiences and preferences, TECH TITAN curated a collection of personalized recommendations for each user. Now, with just a few clicks, any otaku can receive tailored suggestions based on their favorite anime series or movies. Whether one enjoys action-packed shounen adventures or heartwarming slice-of-life tales, Anime Odyssey's recommendation engine ensures that no one feels lost in the vast sea of anime again."""

st.sidebar.title('What is Anime Odyssey? 🥷')
st.sidebar.write(description)


st.title('Anime Odyssey: Embark on a Journey of Recommendations 🥷')

# divide the section into two columns
col1, col2 = st.columns(2)

# select one
with col1:
    option = st.selectbox('Select Anime Type: 👇', ['Anime Series', 'Anime Movies'])

# now time to start suggesting
if option == 'Anime Series':
    try:
        recommendSeries()
    except:
        pass
if option == 'Anime Movies':
    try:
        recommendMovies()
    except:
        pass

# copyright section
st.markdown('# ')
st.markdown('# ')
copyright = "&copy; 2023 Tech Titans Inc. All rights reserved."
st.markdown(f'<p style="text-align:center;">{copyright}</p>', unsafe_allow_html=True)