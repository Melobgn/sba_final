from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from model_utils import load_model, prediction
import pandas as pd

app = FastAPI()

class FeaturesInput(BaseModel):
    State: str
    BankState: str
    RevLineCr: str
    LowDoc: str
    NewExist: int
    UrbanRural: int
    #FranchiseBinary: int
    Zip: int
    NAICS: int
    Term: int
    NoEmp: int
    CreateJob: int
    RetainedJob: int
    FranchiseCode: int
    GrAppv: float
    SBA_Appv: float
    #Industry: str

class PredictionOutput(BaseModel):
    prediction: int

model = load_model()  

@app.post('/predict', response_model=PredictionOutput)
def prediction_root(feature_input: FeaturesInput):
    data_dict = feature_input.dict()
    data_dict['FranchiseBinary'] = 0 if feature_input.FranchiseCode in [0, 1] else 1
    data_dict['Industry'] = map_naics_to_industry(feature_input.NAICS)
    input_df = pd.DataFrame([data_dict])
    prediction_final = model.predict(input_df)
    
    #input_df = pd.DataFrame([feature_input.dict()])
    #prediction_final = model.predict(input_df)
    
    return PredictionOutput(prediction=int(prediction_final[0]))



def map_naics_to_industry(naics_code: int) -> str:
    # logique de mapping basée sur le code NAICS
    mapping = {
        11: 'Ag/For/Fish/Hunt',
        21: 'Min/Quar/Oil_Gas_ext',
        22: 'Utilities',
        23: 'Construction',
        31: 'Manufacturing',
        32: 'Manufacturing',
        33: 'Manufacturing',
        42: 'Wholesale_trade',
        44: 'Retail_trade',
        45: 'Retail_trade',
        48: 'Trans/Ware',
        49: 'Trans/Ware',
        51: 'Information',
        52: 'Finance/Insurance',
        53: 'RE/Rental/Lease',
        54: 'Prof/Science/Tech',
        55: 'Mgmt_comp',
        56: 'Admin_sup/Waste_Mgmt_Rem',
        61: 'Educational',
        62: 'Healthcare/Social_assist',
        71: 'Arts/Entertain/Rec',
        72: 'Accom/Food_serv',
        81: 'Other_no_pub',
        92: 'Public_Admin',
    }
    return mapping.get(naics_code, "Unknown Industry")

#uvicorn main:app --reload
#/docs pour tester les requetes