import pandas as pd,pytest,numpy as np
from src.data_generator import generate_data,TARGETS
from src.data_validation import validate_data,DataValidationError
from src.model_training import train_models
from src.prediction import predict_resources,status_for
from src.recommendations import recommendations
def test_data_reproducible():
    pd.testing.assert_frame_equal(generate_data(365,7),generate_data(365,7))
def test_targets_and_attendance_valid():
    d=generate_data(365);assert (d[TARGETS]>=0).all().all();assert (d.student_attendance<=d.total_students).all()
def test_missing_columns_rejected():
    with pytest.raises(DataValidationError):validate_data(pd.DataFrame({"date":["2025-01-01"]}))
def test_invalid_attendance_rejected():
    d=generate_data(365);d.loc[0,"student_attendance"]=9999
    with pytest.raises(DataValidationError):validate_data(d)
def test_models_predict():
    d=generate_data(365);b=train_models(d);p=predict_resources(b,d.iloc[-1].to_dict())
    assert all(p[t] is not None and np.isfinite(p[t]) and p[t]>=0 for t in TARGETS)
def test_thresholds_and_recommendations():
    assert status_for(20,{"low":10,"high":20})=="HIGH"
    r=recommendations({"water_consumption_litres":100},{"water_consumption_litres":"HIGH"},{"school_open":1,"is_school_event":1})
    assert any("leak" in x[2].lower() for x in r)
