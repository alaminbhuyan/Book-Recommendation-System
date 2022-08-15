from flask import Flask, url_for, redirect, render_template, request
import numpy as np
import pickle


popular_df = pickle.load(file=open(file="popular_df.pkl", mode="rb"))
books = pickle.load(file=open(file="books.pkl", mode="rb"))
pt = pickle.load(file=open(file="pt.pkl", mode="rb"))
similarity_scores = pickle.load(
    file=open(file="similarity_scores.pkl", mode="rb"))


app = Flask(__name__)


@app.route(rule="/")
def home():
    return render_template(template_name_or_list="home.html",
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           year_publication=list(
                               popular_df['Year-Of-Publication'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           total_rating=list(
                               popular_df['total_number_of_rating'].values),
                           average_rating=list(
                               popular_df['average_number_of_rating'].values),
                           )


@app.route(rule="/recommend")
def recommend_UI():
    return render_template(template_name_or_list="recommend.html")



@app.route(rule="/recommendedBooks", methods=['GET', 'POST'])
def recommend_books():
    if request.method == "POST":
        try:
            book_name = request.form.get("bookname")
            book_name = book_name.lower()
            book_index = np.where(pt.index == book_name)[0][0]
            similar_books = sorted(list(enumerate(
            similarity_scores[book_index])), key=lambda x: x[1], reverse=True)[1:11]
        except:
            # return redirect(location="https://flask.palletsprojects.com/en/2.2.x/api/")
            return render_template(template_name_or_list="errorPage.html")
        else:
            books_info = []
            for i in similar_books:
                book_items = []
                temp_df = books[books["Book-Title"] == pt.index[i[0]]]
                book_items.extend(list(temp_df.drop_duplicates(
                    "Book-Title")["Book-Title"].values))
                book_items.extend(list(temp_df.drop_duplicates(
                    "Book-Title")["Book-Author"].values))
                book_items.extend(list(temp_df.drop_duplicates(
                    "Book-Title")["Image-URL-M"].values))

                books_info.append(book_items)

    return render_template(template_name_or_list="recommend.html", books_info=books_info)


if __name__ == "__main__":
    app.run(debug=True)
