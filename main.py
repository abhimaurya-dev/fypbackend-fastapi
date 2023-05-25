from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import numpy as np
import pickle

app = FastAPI()

origins = ["https://soft-klepon-49df2a.netlify.app", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def root():
    return """<html>
              <head>
                <title>Home</title>
              </head>
              <body style='overflow:hidden;'>
                <h1 style='display:flex; align-items:center; justify-content:center; width:100vw; font-size:4rem; height:100vh'>Welcome To Final Year Project</h1>
              </body>
              </html>"""

@app.post("/predict/", tags=['CROP_RECOMMENDATION'])
async def recommendCrop(body: dict) -> dict:
    try:
        query_array = body['query_array']
        query_array = list(map(float,query_array))
        query_array = np.array(query_array).reshape(1,-1)
        response_data={}
        with open("mlmodel\\trainedModel\\trained_model",'rb') as f:
          model = pickle.load(f)
          predict_result = model.predict(query_array)
          response_data['success'] = 'true'
          response_data['predicted_crop'] = predict_result[0]
        return response_data
    except:
        return {
                  'success': 'false',
                  'message':'Invalid request'
              }
    
@app.post("/yeild-predict", tags=['YEILD_PREDICTION'])
async def yeild_predict(body:dict) -> dict:
    try:
      query_array = body['query_array']
      query_array = list(map(float,query_array))
      query_array = np.array(query_array).shape(1,-1)
      response_data = {}
      with open('mlmodel\\yeildPrediction\\trained)mpdel', 'rb') as f:
        model = pickle.load(f)
        predict_result = model.predict(query_array)
        response_data['predicted_result'] = predict_result[0]
      return response_data
    except:
      return {
        'success': 'false',
        'message': 'Invalid request'
      }