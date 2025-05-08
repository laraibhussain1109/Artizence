import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from pmdarima.preprocessing import FourierFeaturizer

NUM_FEATURES = ['avg_runs_last5', 'avg_wkts_last5', 'team_momentum']
CAT_FEATURES = ['team_home', 'team_away']

class FourierExogOnly(TransformerMixin, BaseEstimator):
    """
    Wraps pmdarima's FourierFeaturizer to return only the exogenous feature matrix.
    """
    def __init__(self, m, k, prefix=None):
        self.m = m
        self.k = k
        self.prefix = prefix
        self.ff = None

    def fit(self, X, y=None):
        self.ff = FourierFeaturizer(m=self.m, k=self.k, prefix=self.prefix)
        return self

    def fit_transform(self, X, y=None):
        y_series = X.squeeze()
        _, exog = FourierFeaturizer(m=self.m, k=self.k, prefix=self.prefix).fit_transform(y_series)
        return exog

    def transform(self, X):
        y_series = X.squeeze()
        res = self.ff.transform(y_series)
        # unpack if tuple
        if isinstance(res, tuple):
            return res[1]
        return res

temporal_pipeline = Pipeline([
    ('fourier', FourierExogOnly(m=7, k=3, prefix='fourier')),
])


temporal_feature = ['match_date']
preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('scale', StandardScaler()),
    ]), NUM_FEATURES),
    ('cat', Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ]), CAT_FEATURES),
    ('time', temporal_pipeline, temporal_feature),
])

def build_feature_pipeline():
    """Return transformer for numeric, categorical, and Fourier time features."""
    return preprocessor

