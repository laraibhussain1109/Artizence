import pickle
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder

class EnsembleModel:
    def __init__(self, verbose=1):
        self.model = None
        self.label_encoder = None
        self.is_classifier = False
        self.verbose = verbose

    def fit(self, X, y):
        # if y is non-numeric, treat as classification
        if y.dtype == object or y.dtype.name == 'category':
            self.is_classifier = True
            # encode string labels to integers
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
            # enable verbose output for training
            self.model = GradientBoostingClassifier(verbose=self.verbose)
            self.model.fit(X, y_encoded)
        else:
            # regression with verbose output
            self.model = GradientBoostingRegressor(verbose=self.verbose)
            self.model.fit(X, y)
        return self

    def predict(self, X):
        preds = self.model.predict(X)
        if self.is_classifier:
            return self.label_encoder.inverse_transform(preds)
        return preds

    def save(self, path):
        # persist model + encoder
        with open(path + '.pkl', 'wb') as f:
            pickle.dump({
                'model': self.model,
                'label_encoder': self.label_encoder,
                'is_classifier': self.is_classifier
            }, f)
