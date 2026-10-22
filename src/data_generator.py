from pathlib import Path
import numpy as np, pandas as pd
TARGETS=["water_consumption_litres","electricity_consumption_kwh","waste_generation_kg"]
FEATURES=["day_of_week","month","is_weekend","school_open","student_attendance","total_students","attendance_rate","temperature_c","rainfall_mm","humidity_percent","is_school_event","holiday_or_exam_day"]
def generate_data(days=730,seed=42):
    rng=np.random.default_rng(seed); dates=pd.date_range("2024-01-01",periods=days); rows=[]; pop=850
    for d in dates:
        dow,month=d.dayofweek,d.month
        br=(month==6 or (month==5 and d.day>=20) or (month==12 and d.day>=24) or (month==1 and d.day<=5))
        weekend=int(dow>=5); opened=int(not weekend and not br); holiday=int(br or (month==3 and 10<=d.day<=16))
        event=int(opened and rng.random()<.075); et=str(rng.choice(["sports","assembly","festival","parent_meeting"])) if event else "none"
        rate=float(np.clip(rng.normal(.88 if opened else .015,.055),0,1)); attend=int(round(pop*rate)) if opened else int(rng.integers(0,8))
        temp=float(np.clip(25+8*np.sin((month-3)/12*2*np.pi)+rng.normal(0,3),5,44))
        rain=float(max(0,rng.gamma(1.2,4) if month in [6,7,8,9] else rng.gamma(.7,1.5)-.5))
        hum=float(np.clip(54+rain*2.1+rng.normal(0,9),18,100))
        water=max(0,110+attend*13.2+temp*7+event*420+rng.normal(0,430))
        elec=max(0,105+opened*250+attend*.72+max(0,temp-27)*18+event*95+rng.normal(0,75))
        waste=max(0,2.2+attend*.105+event*17+rng.normal(0,7))
        if not opened:
            water=max(0,35+temp*2+rng.normal(0,12)); elec=max(0,18+max(0,temp-27)*3+rng.normal(0,8)); waste=max(0,.8+rng.normal(0,1.1))
        rows.append(dict(date=d.date().isoformat(),day_of_week=dow,month=month,is_weekend=weekend,school_open=opened,student_attendance=attend,total_students=pop,attendance_rate=round(attend/pop,4),temperature_c=round(temp,1),rainfall_mm=round(rain,1),humidity_percent=round(hum,1),is_school_event=event,event_type=et,holiday_or_exam_day=holiday,water_consumption_litres=round(water,1),electricity_consumption_kwh=round(elec,1),waste_generation_kg=round(waste,1)))
    return pd.DataFrame(rows)
if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]; d=generate_data(); d.to_csv(root/"data/simulated_school_data.csv",index=False)
    t=d.drop(columns=TARGETS).copy()
    for c in TARGETS:t[c]=np.nan
    t.head(30).to_csv(root/"data/real_data_template.csv",index=False)
    print(f"Generated {len(d)} synthetic rows.")
