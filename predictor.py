import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future_risk(df):
    daily = df.groupby("date")["amount"].sum().reset_index()
    daily["day_index"] = range(len(daily))

    X = daily[["day_index"]]
    y = daily["amount"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array([[len(daily) + i] for i in range(7)])
    prediction = model.predict(future_days)

    return round(prediction.mean(), 2)
