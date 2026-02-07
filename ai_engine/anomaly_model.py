from sklearn.ensemble import IsolationForest

def train_model(data):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(data)
    return model

