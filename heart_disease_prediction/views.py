from django.shortcuts import render
from django.http import HttpResponse
import pickle
import pandas as pd
import numpy as np

# Load the trained model at the start
model_filename = 'heart_disease_prediction_model.pkl'
with open(model_filename, 'rb') as file:
    heart_attack_detection_model = pickle.load(file)

# View to render the heart disease prediction form
def heart(request):
    return render(request, "heart_disease_prediction/heart.html")


from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import pandas as pd

def predict_heart(request):
    if request.method == 'POST':
        try:
            # Exclude csrfmiddlewaretoken and convert remaining values to float
            input_features = [float(value) for key, value in request.POST.items() if key != 'csrfmiddlewaretoken']

            # Ensure the number of features matches your model's expectation
            features_name = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]
            
            if len(input_features) != len(features_name):
                return JsonResponse({'error': 'Incorrect number of features provided.'}, status=400)
            
            df = pd.DataFrame([input_features], columns=features_name)

            # Replace with your actual model prediction code
            output = heart_attack_detection_model.predict(df)

            if output == 1:
                res_val = "a high risk of Heart Disease"
            else:
                res_val = "a low risk of Heart Disease"

            return render(request, 'heart_disease_prediction/heart_result.html', {'prediction_text': f'Patient has {res_val}'})

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse("Invalid request method.", status=405)
