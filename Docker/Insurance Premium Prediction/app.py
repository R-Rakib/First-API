from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Schema.user_input import UserInput
from Schema.prediction_response import PredictionResponse
from config.city_tier import tier_1_cities, tier_2_cities
from Model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

# Human Readable Root
@app.get('/')
def home():
    return {'message': "Insurance Premium Prediction API"}

# Health Check Endpoint
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'Model Available': model is not None
    }

# Prediction Endpoint
@app.post('/predict')
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,  # Fixed from income_lpa to income
        'occupation': data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})