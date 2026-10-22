import numpy as np,pandas as pd
from src.model_training import prepare
from src.data_generator import TARGETS,FEATURES
def predict_resources(bundle,row):
    if not bundle or not bundle.get("models"):raise ValueError("No trained model available.")
    x=prepare(pd.DataFrame([row]));missing=[c for c in FEATURES if c not in x]
    if missing:raise ValueError("Missing features: "+", ".join(missing))
    out={}
    for t in TARGETS:
        if t not in bundle["models"]:out[t]=None;continue
        v=float(bundle["models"][t].predict(x[FEATURES])[0]);out[t]=max(0,v) if np.isfinite(v) else None
    return out
def status_for(v,th):
    if v is None or not np.isfinite(v):return "UNAVAILABLE"
    return "LOW" if v<th["low"] else ("NORMAL" if v<th["high"] else "HIGH")
