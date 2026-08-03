import joblib
import pandas as pd

# Load Model
model = joblib.load("ml/model.pkl")

# Load Encoders
domain_encoder = joblib.load("ml/domain_encoder.pkl")
priority_encoder = joblib.load("ml/priority_encoder.pkl")
risk_encoder = joblib.load("ml/risk_encoder.pkl")


def predict_risk(domain, budget, team_size, timeline, priority):
    # Normalize user input
    domain = domain.strip().title()
    priority = priority.strip().title()

    data = pd.DataFrame([{
        "Budget": float(budget),
        "Team_Size": int(team_size),
        "Timeline": int(timeline),
        "Priority": priority_encoder.transform([priority])[0],
        "Domain": domain_encoder.transform([domain])[0]
    }])

    prediction = model.predict(data)

    return risk_encoder.inverse_transform(prediction)[0]