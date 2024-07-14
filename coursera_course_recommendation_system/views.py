# views.py

from django.shortcuts import render
from django.http import HttpResponse
import os
import pickle
import numpy as np
import pandas as pd

# Assuming courses.pkl and similarity_course.pkl are in the same directory as views.py
# current_dir = os.path.dirname(__file__)
# courses_path = os.path.join(current_dir, 'courses.pkl')
# similarity_path = os.path.join(current_dir, 'similarity_course.pkl')

# courses_list = pd.read_pickle(courses_path)
# similarity = pd.read_pickle(similarity_path)
try:
# Load courses_list and similarity
    courses_list = pickle.load(open('courses.pkl', 'rb'))
    similarity = pickle.load(open('similarity_course.pkl', 'rb'))

except FileNotFoundError:
    courses_list = pd.DataFrame()  # Empty DataFrame if files not found
    similarity = np.zeros((1, 1))  # Dummy similarity matrix

def recommend(course):
    # course=course.rstrip(" ")
    if courses_list.empty:
        return []  # Return empty list if courses_list is empty
    
    index = courses_list[courses_list['course_name'] == course].index
    if len(index) == 0:
        return []  # Return empty list if course not found

    index = index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_course_names = [courses_list.iloc[i[0]].course_name for i in distances[1:7]]
    return recommended_course_names

def index(request):
    courses = {'courses_list': courses_list['course_name'].tolist()}  # Assuming 'course_name' is the column name in courses_list

    if request.method == 'GET':
        return render(request, 'coursera_course_recommendation_system/index.html', context=courses)

    elif request.method == 'POST':
        selected_course = request.POST.get('selected_course')
        recommended_course_names = recommend(selected_course)
        context = {
            'courses_list': courses_list['course_name'].tolist(),
            'selected_course': selected_course,
            'recommended_course_names': recommended_course_names,
        }
        return render(request, 'coursera_course_recommendation_system/index.html', context)
