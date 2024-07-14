from django.shortcuts import render
from django.http import HttpRequest
import numpy as np
import joblib
import pickle

# Using joblib to load the pickle file
popular_df = joblib.load('popular.pkl')
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

def index(request):
    context = {
        'books': [
            {
                'title': title,
                'author': author,
                'image': image,
                'votes': votes,
                'rating': rating
            }
            for title, author, image, votes, rating in zip(
                popular_df['Book-Title'],
                popular_df['Book-Author'],
                popular_df['Image-URL-M'],
                popular_df['num_ratings'],
                popular_df['avg_rating']
            )
        ]
    }
    return render(request, 'book_recommender_system/index.html', context)

def recommend_ui(request):
    return render(request, 'book_recommender_system/recommend.html')

def recommend_books(request: HttpRequest):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        try:
            index = np.where(pt.index == user_input)[0][0]
        except IndexError:
            return render(request, 'book_recommender_system/recommend.html', {'error': 'Book not found'})

        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        return render(request, 'book_recommender_system/recommend.html', {'data': data})
    return render(request, 'book_recommender_system/recommend.html')
