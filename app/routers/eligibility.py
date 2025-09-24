from fastapi import APIRouter
from pydantic import BaseModel
from app.services.eligibility_service import predict_eligibility

router = APIRouter()

class AppRequest(BaseModel):
    income: float
    family_size: int
    employment_years: float
    assets_value: float

@router.post('/predict')
def predict(req: AppRequest):
    res = predict_eligibility({
        'income': req.income,
        'family_size': req.family_size,
        'employment_years': req.employment_years,
        'assets_value': req.assets_value
    })
    return res