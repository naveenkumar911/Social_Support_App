from app.services.eligibility_service import predict_eligibility
def test_low_income_eligible():
    features = {'income':3000,'family_size':4,'employment_years':2.0,'assets_value':2000}
    res = predict_eligibility(features)
    assert res['prediction'] in ['approve','soft_decline']