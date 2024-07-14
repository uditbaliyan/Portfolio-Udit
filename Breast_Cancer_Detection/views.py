from django.shortcuts import render
import joblib
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

def cancer(request):
    return render(request, "Breast_Cancer_Detection/cancer.html")


def predict(request):
    if request.method == "POST":
        # Extract input features from the form
        # input_features = [int(x) for x in request.POST.values()]
        input_features = [int(request.POST[x]) for x in request.POST if x != 'csrfmiddlewaretoken']


        # Create a DataFrame from the input features
        features_name = ['clump_thickness', 'uniform_cell_size', 'uniform_cell_shape', 'marginal_adhesion',
                         'single_epithelial_size', 'bare_nuclei', 'bland_chromatin', 'normal_nucleoli', 'mitoses']
        df = pd.DataFrame([input_features], columns=features_name)

        # Load the trained breast cancer detection model
        with open('breast_cancer_detection_model.pkl', 'rb') as model_file:
            breast_cancer_detection_model = pickle.load(model_file)

        # Make predictions using the loaded model
        prediction = breast_cancer_detection_model.predict(df)

        # Determine the result based on the prediction
        if prediction[0] == 4:
            res_val = "a high risk of Breast Cancer"
        else:
            res_val = "a low risk of Breast Cancer"

        # Render the template with the prediction result
        return render(request, 'Breast_Cancer_Detection/cancer_result.html', {'prediction_text': f'Patient has {res_val}'})
    else:
        return render(request, 'Breast_Cancer_Detection/cancer.html')  # Render the form if the request is GET
