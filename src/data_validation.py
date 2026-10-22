import pandas as pd
TARGETS=["water_consumption_litres","electricity_consumption_kwh","waste_generation_kg"]
REQ=["date","school_open","student_attendance","total_students","temperature_c","rainfall_mm","humidity_percent","is_school_event",*TARGETS]
class DataValidationError(ValueError): pass
def validate_data(df,require_targets=True):
    if not isinstance(df,pd.DataFrame) or df.empty: raise DataValidationError("CSV is empty.")
    missing=[c for c in REQ if c not in df]
    if not require_targets: missing=[c for c in missing if c not in TARGETS]
    if missing: raise DataValidationError("Missing columns: "+", ".join(missing))
    x=df.copy(); x["date"]=pd.to_datetime(x.date,errors="coerce")
    if x.date.isna().any(): raise DataValidationError("Invalid date; use YYYY-MM-DD.")
    warns=[]
    if x.date.duplicated().any(): warns.append("Duplicate dates found.")
    nums=["student_attendance","total_students","temperature_c","rainfall_mm","humidity_percent",*TARGETS]
    for c in nums:
        if c in x:x[c]=pd.to_numeric(x[c],errors="coerce")
    if x[["student_attendance","total_students"]].isna().any().any():raise DataValidationError("Attendance/population must be numeric.")
    if (x.student_attendance<0).any() or (x.total_students<=0).any() or (x.student_attendance>x.total_students).any():raise DataValidationError("Attendance must be from zero to total_students.")
    if not x.rainfall_mm.dropna().ge(0).all():raise DataValidationError("Rainfall cannot be negative.")
    if not x.humidity_percent.dropna().between(0,100).all():raise DataValidationError("Humidity must be 0–100%.")
    for c in TARGETS:
        if (x[c].dropna()<0).any():raise DataValidationError(f"{c} has negative values.")
        if x[c].isna().any():warns.append(f"{c} has missing targets; those rows will not train that target.")
    if len(x)<180:warns.append("Fewer than 180 rows: seasonal evaluation may be unstable.")
    return x.sort_values("date").reset_index(drop=True),warns
