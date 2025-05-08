from pipelines import build_feature_pipeline
from ensemble_model import EnsembleModel
import joblib
import pandas as pd

df = pd.read_csv('data/raw_cricket_stats.csv', parse_dates=['match_date'])
pipeline = build_feature_pipeline()
X = pipeline.fit_transform(df)
joblib.dump(pipeline, 'ml/fitted_pipeline.pkl')

# Winner model
y_win = df['match_winner']
winner_model = EnsembleModel()
winner_model.fit(X, y_win)
joblib.dump(winner_model, 'models/winner_model.pkl')

# Win score
y_sw = df['win_score']
sw_model = EnsembleModel()
sw_model.fit(X, y_sw)
joblib.dump(sw_model, 'models/score_win_model.pkl')

# Loss score
y_sl = df['loss_score']
sl_model = EnsembleModel()
sl_model.fit(X, y_sl)
joblib.dump(sl_model, 'models/score_loss_model.pkl')
