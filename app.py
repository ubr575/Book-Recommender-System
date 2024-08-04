import pickle  # unpack
import pandas as pd
import numpy as np
from flask import Flask, render_template,request

popular_df=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)
@app.route('/')
def index():
    # sending data to index.html page
    return render_template('index.html',
                           book_title=list(popular_df['Book-Title'] .values),    #extract data from df, values will convert it to numpy array and then convert it into list
                           book_author=list(popular_df['Book-Author'].values),
                           Image=list(popular_df['Image-URL-M'].values),
                           num_ratings=list(popular_df['num_ratings'].values),
                           avg_ratings=list(popular_df['avg_ratings'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods=['post'])

def recommend_books():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        # print(pt.index[i[0]])
        # print(books[books['Book-Title']==pt.index[i[0]]]) it contains duplicates
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    return render_template('/recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)