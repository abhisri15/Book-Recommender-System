import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the data and the model
popular_df = pd.read_pickle(open('model/popular.pkl', 'rb'))
pt = pd.read_pickle(open('model/pt.pkl', 'rb'))
books = pd.read_pickle(open('model/books.pkl', 'rb'))
similarity_scores = pd.read_pickle(open('model/similarity_scores.pkl', 'rb'))


def recommend_books(user_input):
    index = np.where(pt.index == user_input)[0]
    if len(index) == 0:
        return None
    index = index[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return data
def render_home():
    st.subheader('Top 50 Books')
    for i in range(0, len(popular_df), 3):
        # Create columns to display 3 books in each row
        col1, col2, col3 = st.columns(3)

        with col1:
            if 'Image-URL-M' in popular_df.columns and pd.notnull(popular_df['Image-URL-M'].iloc[i]):
                st.image(popular_df['Image-URL-M'].iloc[i], use_column_width=True)
            st.subheader(popular_df['Book-Title'].iloc[i])
            st.write(popular_df['Book-Author'].iloc[i])
            st.write(f"Votes: {popular_df['num_ratings'].iloc[i]}")
            st.write(f"Rating: {popular_df['avg_ratings'].iloc[i]}")

        with col2:
            if i + 1 < len(popular_df):
                if 'Image-URL-M' in popular_df.columns and pd.notnull(popular_df['Image-URL-M'].iloc[i + 1]):
                    st.image(popular_df['Image-URL-M'].iloc[i + 1], use_column_width=True)

                st.subheader(popular_df['Book-Title'].iloc[i + 1])
                st.write(popular_df['Book-Author'].iloc[i + 1])
                st.write(f"Votes: {popular_df['num_ratings'].iloc[i + 1]}")
                st.write(f"Rating: {popular_df['avg_ratings'].iloc[i + 1]}")

        with col3:
            if i + 2 < len(popular_df):
                if 'Image-URL-M' in popular_df.columns and pd.notnull(popular_df['Image-URL-M'].iloc[i + 2]):
                    st.image(popular_df['Image-URL-M'].iloc[i + 2], use_column_width=True)
                st.subheader(popular_df['Book-Title'].iloc[i + 2])
                st.write(popular_df['Book-Author'].iloc[i + 2])
                st.write(f"Votes: {popular_df['num_ratings'].iloc[i + 2]}")
                st.write(f"Rating: {popular_df['avg_ratings'].iloc[i + 2]}")

        # Add equal spacing after every row using beta_container and CSS
        st.write(" ")

def render_recommend():
    st.title('Recommend Books')
    user_input = st.selectbox('Select a Book Title:', pt.index)
    if st.button('Recommend'):
        if user_input:
            data = recommend_books(user_input)
            if data:
                st.subheader('Recommended Books:')
                num_columns = 2
                num_items = len(data)
                num_rows = (num_items + num_columns - 1) // num_columns

                for i in range(num_rows):
                    columns = st.columns(num_columns)
                    for j in range(num_columns):
                        item_index = i * num_columns + j
                        if item_index < num_items:
                            item = data[item_index]
                            if len(item) >= 3 and 'Image-URL-M' in popular_df.columns:
                                image_url = item[2]
                                if pd.notnull(image_url):
                                    columns[j].image(image_url, width=150)
                            columns[j].subheader(item[0])
                            columns[j].write(item[1])
                            if len(item) >= 3 and 'Image-URL-M' in popular_df.columns:
                                columns[j].write(f"Image-URL-M: {image_url}")
            else:
                st.warning("Book not found. Please check the title and try again.")

def main():
    st.set_page_config(page_title='Book Recommender System', page_icon=':books:', layout='centered')

    st.markdown(
        """
        <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .navbar {
            background-color: #00a65a;
            color: #FFFFFF;
        }
        .navbar-brand {
            font-size: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('My Book Recommender')
    nav_choice = st.sidebar.radio('Navigation:', ('Home', 'Recommend Books'))

    if nav_choice == 'Home':
        render_home()
    elif nav_choice == 'Recommend Books':
        render_recommend()


if __name__ == '__main__':
    main()
