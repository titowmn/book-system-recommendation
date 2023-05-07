from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

pickle_off = open("popular.pkl","rb")
popular_df = pd.read_pickle(pickle_off)

pickle_books = open("books.pkl","rb")
books = pd.read_pickle(pickle_books)

pickle_similarity = open("similarity_scores.pkl","rb")
similarity_scores = pd.read_pickle(pickle_similarity)

pickle_pt = open("pt.pkl","rb")
pt = pd.read_pickle(pickle_pt)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]

    data = []

    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
        print(data)
    return  render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

