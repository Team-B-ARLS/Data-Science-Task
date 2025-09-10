import pandas as pd
import numpy as np
import joblib
import io

# Load model pipeline
pipeline = joblib.load("roi_pipeline.joblib")
model = pipeline["model"]
scaler = pipeline["scaler"]
model_columns = pipeline["model_columns"]

def predict_campaign_revenue(user_input: dict):
    one_hot_cols = ["Channel", "Objective", "Audience", "Geo", "Creative_Type"]
    binary_cols = ["Status"]
    numerical_cols = [
        col for col in model_columns
        if col not in binary_cols and not any(col.startswith(prefix + "_") for prefix in one_hot_cols)
    ]
    
    input_df = pd.DataFrame([user_input])
    for col in binary_cols:
        input_df[col] = input_df[col].map({"Completed": 1, "Active": 0})
    for col in numerical_cols:
        if col not in input_df.columns:
            input_df[col] = np.nan
    for col in one_hot_cols:
        if col not in input_df.columns:
            input_df[col] = "__MISSING__"

    input_encoded = pd.get_dummies(input_df, columns=one_hot_cols, drop_first=True, dtype='int')
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    input_scaled = pd.DataFrame(scaler.transform(input_encoded), columns=input_encoded.columns)
    prediction = model.predict(input_scaled)
    return prediction[0]

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Prediction_Output')
    return output.getvalue()
