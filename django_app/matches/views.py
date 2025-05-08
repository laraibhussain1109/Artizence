# django_app/matches/views.py

import joblib
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MatchFeaturesSerializer, PredictionSerializer
# matches/views.py
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import requests

PIPELINE_PATH = 'ml/fitted_pipeline.pkl'
MODEL_SCORE_WIN_PATH = 'models/score_win_model.pkl'
MODEL_SCORE_LOSS_PATH = 'models/score_loss_model.pkl'
MODEL_WINNER_PATH = 'models/winner_model.pkl'
def load_pipeline():
    from ml.pipelines import FourierExogOnly
    return joblib.load(PIPELINE_PATH)
model_score_win = joblib.load(MODEL_SCORE_WIN_PATH)
model_score_loss = joblib.load(MODEL_SCORE_LOSS_PATH)
model_winner = joblib.load(MODEL_WINNER_PATH)



# def predict_winner_page(request):
#     return render(request, 'rest_framework/predict_winner.html')

# pipeline = joblib.load(PIPELINE_PATH)


class PredictWinnerView(APIView):
    def post(self, request):
        serializer = MatchFeaturesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pipeline= load_pipeline()

        df = pd.DataFrame([serializer.validated_data])
       
        X = pipeline.transform(df)
        pred = model_winner.predict(X)[0]
        return Response({'predicted_winner': float(pred)}, status=status.HTTP_200_OK)


class PredictScoreView(APIView):
    def post(self, request):
        serializer = MatchFeaturesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        df = pd.DataFrame([serializer.validated_data])
        pipeline = load_pipeline()
        X = pipeline.transform(df)

        score_win = model_score_win.predict(X)[0]
        score_loss = model_score_loss.predict(X)[0]

        resp = {
            'predicted_score_win': float(score_win),
            'predicted_score_loss': float(score_loss)
        }
        return Response(resp, status=status.HTTP_200_OK)
def predict_winner_page(request):
    context = {}
    if request.method == 'POST':
        # build the same payload as your DRF expects
        payload = {
            'team_home': request.POST['team_home'],
            'team_away': request.POST['team_away'],
            'avg_runs_last5': request.POST['avg_runs_last5'],
            'avg_wkts_last5': request.POST['avg_wkts_last5'],
            'team_momentum': request.POST['team_momentum'],
            'match_date': request.POST['match_date'],
        }
        # call your own API (you could also call the pipeline/model directly here)
        api_url = request.build_absolute_uri(reverse('api-predict-winner'))
        resp = requests.post(api_url, json=payload, cookies=request.COOKIES)
        if resp.ok:
            context['prediction'] = resp.json()['predicted_winner']
        else:
            context['errors'] = resp.json()
    return render(request, 'rest_framework/predict_winner.html', context)
def predict_score_page(request):


    context = {}
    if request.method == 'POST':
        # Extract and cast form fields
        data = {
            'team_home':      request.POST['team_home'],
            'team_away':      request.POST['team_away'],
            'avg_runs_last5': float(request.POST['avg_runs_last5']),
            'avg_wkts_last5': float(request.POST['avg_wkts_last5']),
            'team_momentum':  float(request.POST['team_momentum']),
            # assume the form supplies UNIX timestamp
            'match_date':     int(request.POST['match_date']),
        }
        # Build a DataFrame for sklearn
        df = pd.DataFrame([data])

        # Transform & predict
        pipeline= load_pipeline()
        X = pipeline.transform(df)
        win_score  = model_score_win.predict(X)[0]
        loss_score = model_score_loss.predict(X)[0]

        # Add to context
        context['predicted_score_win']  = round(win_score,  2)
        context['predicted_score_loss'] = round(loss_score, 2)

    return render(request, 'rest_framework/predict_score.html', context)