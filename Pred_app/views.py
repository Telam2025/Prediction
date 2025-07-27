import os
import pandas as pd
import pickle
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def home(request):
    return render(request, 'Pred_app/Home.html')

def contact(request):
    success = False
    error = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            try:
                send_mail(
                    subject=f"Contact de {name}",
                    message=message,
                    from_email=email,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],  # ou un email de réception réel
                )
                success = True
            except Exception as e:
                error = f"Erreur lors de l'envoi : {e}"
        else:
            error = "Tous les champs sont obligatoires."

    return render(request, 'Pred_app/Contact.html', {
        'success': success,
        'error': error
    })


MODEL_PATHS = {
    'random_forest': 'C:/Users/radja/Documents/model_RF.pkl',
    'xgboost': 'C:/Users/radja/Documents/model_GB.pkl',
    'sarimax': 'C:/Users/radja/Documents/model_SAR.pkl',
    'Rand_ford_hist':'C:/Users/radja/Documents/best_rf_model.pkl',
}

MODEL_COLUMNS = {
    'random_forest': ['CAPerDay','Death_rate','is_holiday','is_Day_of_Black_Friday'],
    'xgboost': ['numberOfOrdersPerDay','CAPerDay', 'Death_rate'],
    'sarimax': ['CAPerDay','numberOfOrdersPerDay','Death_rate','is_Day_of_Black_Friday','is_holiday'],
    'Rand_ford_hist':['CAPerDay'],
}

@login_required
def upload_view(request):
    prediction = None
    error = None

    if request.method == 'POST':
        model_key = request.POST.get('model')
        file = request.FILES.get('file')

        if not model_key or not file:
            error = "Modèle ou fichier manquant."
        elif model_key not in MODEL_PATHS:
            error = "Modèle non supporté."
        else:
            try:
                model_path = MODEL_PATHS[model_key]
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)

                df = pd.read_excel(file)
                required_cols = MODEL_COLUMNS[model_key]

                if not all(col in df.columns for col in required_cols):
                    error = f"Colonnes manquantes. Requises: {required_cols}"
                else:
                    X = df[required_cols].copy()
                    for col in required_cols:
                        X[col] = pd.to_numeric(X[col], errors='coerce')
                    prediction = model.predict(X).tolist()

            except Exception as e:
                error = f"Erreur de prédiction: {str(e)}"

    return render(request, 'Pred_app/upload.html', {
        'prediction': prediction,
        'error': error
    })