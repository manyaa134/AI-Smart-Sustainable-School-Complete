from pathlib import Path
import json,joblib,numpy as np,pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from src.data_generator import TARGETS,FEATURES
MODELS={"Linear Regression":LinearRegression(),"Decision Tree":DecisionTreeRegressor(max_depth=8,min_samples_leaf=5,random_state=42),"Random Forest":RandomForestRegressor(n_estimators=160,min_samples_leaf=3,random_state=42,n_jobs=-1)}
def prepare(d):
    x=d.copy()
    if "date" in x:
        dt=pd.to_datetime(x.date,errors="coerce");x["day_of_week"]=dt.dt.dayofweek;x["month"]=dt.dt.month
    if "attendance_rate" not in x:x["attendance_rate"]=x.student_attendance/x.total_students.replace(0,np.nan)
    if "is_weekend" not in x:x["is_weekend"]=(x.day_of_week>=5).astype(int)
    if "holiday_or_exam_day" not in x:x["holiday_or_exam_day"]=0
    return x
def score(y,p):return {"MAE":float(mean_absolute_error(y,p)),"RMSE":float(np.sqrt(mean_squared_error(y,p))),"R2":float(r2_score(y,p)) if len(y)>1 else float("nan")}
def pipeline(model):
    prep=ColumnTransformer([("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]),FEATURES)])
    return Pipeline([("prep",prep),("model",model)])
def train_models(df,model_dir=None):
    df=prepare(df).sort_values("date").reset_index(drop=True)
    if len(df)<60:raise ValueError("At least 60 records required.")
    out={"features":FEATURES,"models":{},"thresholds":{},"reports":{}}
    for target in TARGETS:
        d=df.dropna(subset=[target]).copy()
        if len(d)<60:out["reports"][target]={"warning":"Fewer than 60 target records"};continue
        n=len(d);i=int(.65*n);j=int(.80*n);tr,va,te=d.iloc[:i],d.iloc[i:j],d.iloc[j:]
        Xtr=prepare(tr)[FEATURES];yv=va[target].astype(float);Xv=prepare(va)[FEATURES];Xt=prepare(te)[FEATURES];yt=te[target].astype(float);ytr=tr[target].astype(float)
        base=float(ytr.mean()); comps=[{"model":"Training mean baseline","validation":score(yv,np.full(len(yv),base)),"test":score(yt,np.full(len(yt),base))}]
        fitted={}
        for name,m in MODELS.items():
            p=pipeline(m);p.fit(Xtr,ytr);fitted[name]=p
            comps.append({"model":name,"validation":score(yv,np.maximum(0,p.predict(Xv))),"test":score(yt,np.maximum(0,p.predict(Xt)))})
        best=min(MODELS,key=lambda name:score(yv,np.maximum(0,fitted[name].predict(Xv)))["MAE"]);p=fitted[best];pred=np.maximum(0,p.predict(Xt))
        out["models"][target]=p;out["thresholds"][target]={"low":float(ytr.quantile(.25)),"high":float(ytr.quantile(.75))}
        out["reports"][target]={"selected_model":best,"train_rows":len(tr),"validation_rows":len(va),"test_rows":len(te),"comparisons":comps,"test_actual":yt.tolist(),"test_predicted":pred.tolist(),"test_metrics":score(yt,pred)}
    if model_dir:
        p=Path(model_dir);p.mkdir(parents=True,exist_ok=True);joblib.dump(out,p/"model_bundle.joblib")
        compact={k:{a:b for a,b in v.items() if a not in ("test_actual","test_predicted")} for k,v in out["reports"].items()}
        (p/"model_evaluation.json").write_text(json.dumps(compact,indent=2))
    return out
