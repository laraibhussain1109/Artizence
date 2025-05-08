from django.urls import path
from .views import (
    predict_winner_page,
    predict_score_page,
    PredictWinnerView,
    PredictScoreView,
)

urlpatterns = [
    # — Page views for HTML forms —
    path('predict/winner/', predict_winner_page, name='predict-winner-page'),
    path('api/predict/winner/', PredictWinnerView.as_view(), name='api-predict-winner'),
    path('predict/score/', predict_score_page, name='predict-score-page'),
    path('api/predict/score/', PredictScoreView.as_view(), name='api-predict-score'),
]
