from django.shortcuts import render
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return ""

def recommend(request):
    if request.method == 'POST':
        selected_movie = request.POST.get('selected_movie')
        selected_movie=selected_movie.title()
        movies = pickle.load(open('movie_list.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))

        # Check if the movie exists in the DataFrame
        movie_indices = movies[movies['title'] == selected_movie].index
        if movie_indices.empty:
            return render(request, 'Recommender_System/index.html', {
                'error': 'Movie not found. Please try another movie.'
            })

        index = movie_indices[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id  # Assuming movie_id is a column in your movie_list.pkl
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return render(request, 'Recommender_System/index.html', {
            'selected_movie': selected_movie,
            'recommended_movies': zip(recommended_movie_names, recommended_movie_posters)
        })

    else:
        movies = pickle.load(open('movie_list.pkl', 'rb'))['title'].tolist()
        return render(request, 'Recommender_System/index.html', {'movies': movies})
