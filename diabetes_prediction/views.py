from django.shortcuts import render
from django.http import HttpResponse
import pickle
import numpy as np

# Load the trained model
filename = 'diabetes-prediction-rfc-model.pkl'
with open(filename, 'rb') as file:
    classifier = pickle.load(file)

# View to render the form for diabetes prediction
def diabetes(request):
    return render(request, "diabetes_prediction/diabetes.html")

# View to handle the form submission and prediction
def predict(request):
    if request.method == 'POST':
        preg = request.POST['pregnancies']
        glucose = request.POST['glucose']
        bp = request.POST['bloodpressure']
        st = request.POST['skinthickness']
        insulin = request.POST['insulin']
        bmi = request.POST['bmi']
        dpf = request.POST['dpf']
        age = request.POST['age']

        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]], dtype=float)
        my_prediction = classifier.predict(data)[0]

        return render(request, 'diabetes_prediction/diab_result.html', {'prediction': my_prediction})

    return HttpResponse("Invalid request method.", status=405)
