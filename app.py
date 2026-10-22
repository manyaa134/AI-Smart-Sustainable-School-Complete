from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_generator import generate_data, TARGETS
from src.data_validation import validate_data
from src.model_training import train_models
from src.prediction import predict_resources, status_for
from src.recommendations import recommendations

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "simulated_school_data.csv"
UNITS = {
    "water_consumption_litres": "L",
    "electricity_consumption_kwh": "kWh",
    "waste_generation_kg": "kg",
}
LABELS = {
    "water_consumption_litres": "Water",
    "electricity_consumption_kwh": "Electricity",
    "waste_generation_kg": "Waste",
}

st.set_page_config(page_title="AI Smart Sustainable School", page_icon="🌱", layout="wide")
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp { background: radial-gradient(ellipse at top left, #142b31 0%, #0b1118 48%, #0a0f15 100%); color: #e8eef2; }
[data-testid="stSidebar"] { background: #101a22; border-right: 1px solid #263842; }
h1,h2,h3 { color: #e9f5f0 !important; letter-spacing: -0.02em; }
p, label, .stCaption { color: #c2d0d8; }
[data-testid="stMetric"] { background: linear-gradient(135deg,#152832,#14211f); border: 1px solid #29434a; padding: 16px; border-radius: 14px; }
[data-testid="stMetricLabel"] { color: #a9c5c2 !important; }
[data-testid="stMetricValue"] { color: #f2fbf8 !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-color: #29404a !important; border-radius: 14px; }
.stButton > button, .stDownloadButton > button { border-radius: 10px; border: 1px solid #3e7770; }
.small-note { color: #9bb0ba; font-size: .88rem; }
.kicker { color:#77d7b0; text-transform:uppercase; letter-spacing:.13em; font-size:.75rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="kicker">CLASS XII · DATA SCIENCE · SDGs 6, 7, 12, 13</div>', unsafe_allow_html=True)
st.title("🌱 AI Smart Sustainable School")
st.caption("A machine-learning decision-support prototype for school resource planning.")

with st.sidebar:
    st.markdown("## 🌿 Project workspace")
    source = st.radio("Data source", ["Simulated demo data", "Upload CSV"], help="Uploaded files are validated but their real-world authenticity cannot be verified by the app.")
    upload = st.file_uploader("Choose a school data CSV", type=["csv"], disabled=source != "Upload CSV")
    page = st.radio("Navigate", ["Overview", "Explore data", "Predict resources", "Compare models", "Project & SDGs"])
    st.divider()
    st.markdown("**Prediction targets**")
    st.caption("Water · Electricity · Waste")
    st.caption("Python + scikit-learn + Streamlit + Orange guide")

if source == "Simulated demo data":
    if not DATA.exists():
        generate_data().to_csv(DATA, index=False)
    df = pd.read_csv(DATA)
    source_label = "SIMULATED DEMO DATA"
    warnings = []
else:
    if upload is None:
        st.info("Upload a CSV to continue. Demo data will not be silently substituted.")
        st.stop()
    try:
        df, warnings = validate_data(pd.read_csv(upload))
        source_label = "UPLOADED DATA · AUTHENTICITY UNVERIFIED"
    except Exception as exc:
        st.error(f"CSV validation failed: {exc}")
        st.stop()

for warning in warnings:
    st.warning(warning)

if source == "Simulated demo data":
    st.warning("DEMO MODE · The bundled dataset is simulated. Predictions and scores are educational examples, not verified forecasts for a real school.")
else:
    st.info("DATA SOURCE · Uploaded data passed the app's structural checks. This does not prove the records are genuine, complete or representative.")

@st.cache_data(show_spinner=False)
def train_cached(frame):
    return train_models(frame)

with st.spinner("Preparing and evaluating models…"):
    try:
        bundle = train_cached(df)
    except Exception as exc:
        st.error(f"Model training failed: {exc}")
        st.stop()

st.caption(f"Active source: **{source_label}** · {len(df):,} records · {pd.to_datetime(df['date']).min().date()} to {pd.to_datetime(df['date']).max().date()}")

if page == "Overview":
    st.subheader("Resource overview")
    st.caption("These are dataset summaries, not forecasts for a specific day.")
    cols = st.columns(3)
    for col, target in zip(cols, TARGETS):
        col.metric(f"{LABELS[target]} · average", f"{df[target].mean():,.1f} {UNITS[target]}")
    left, right = st.columns([1.6, 1])
    with left:
        st.markdown("### Daily resource trends")
        trend_target = st.selectbox("Choose a resource", TARGETS, format_func=lambda x: LABELS[x])
        trend = df.copy()
        trend["date"] = pd.to_datetime(trend["date"])
        st.plotly_chart(px.line(trend, x="date", y=trend_target, template="plotly_dark", title=f"Daily {LABELS[trend_target].lower()} use ({UNITS[trend_target]})"), use_container_width=True)
    with right:
        st.markdown("### Dataset health")
        quality = pd.DataFrame({"Check": ["Rows", "Columns", "Duplicate dates", "Missing cells"], "Result": [f"{len(df):,}", str(len(df.columns)), str(pd.to_datetime(df.date).duplicated().sum()), str(int(df.isna().sum().sum()))]})
        st.dataframe(quality, hide_index=True, use_container_width=True)
        st.markdown("### What this prototype does")
        st.write("1. Validates the selected dataset.\n2. Compares regression models against a baseline.\n3. Estimates three resource quantities.\n4. Converts estimates into transparent review prompts.")
    st.markdown("### Latest records")
    st.dataframe(df.tail(8), hide_index=True, use_container_width=True)
    st.download_button("Download active dataset as CSV", df.to_csv(index=False).encode("utf-8"), file_name="school_resource_data.csv", mime="text/csv")

elif page == "Explore data":
    st.subheader("Explore the data")
    dates = pd.to_datetime(df.date)
    date_range = st.date_input("Date range", value=(dates.min().date(), dates.max().date()), min_value=dates.min().date(), max_value=dates.max().date())
    view = df.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        day = pd.to_datetime(view.date).dt.date
        view = view[(day >= date_range[0]) & (day <= date_range[1])]
    st.caption(f"Showing {len(view):,} of {len(df):,} records")
    target = st.selectbox("Resource trend", TARGETS, format_func=lambda x: LABELS[x])
    plot = view.copy(); plot["date"] = pd.to_datetime(plot.date)
    st.plotly_chart(px.line(plot, x="date", y=target, template="plotly_dark", title=f"{LABELS[target]} over time"), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        group = st.selectbox("Compare by context", ["school_open", "is_weekend", "is_school_event", "holiday_or_exam_day"])
        st.plotly_chart(px.box(view, x=group, y=target, template="plotly_dark", title=f"{LABELS[target]} by {group}"), use_container_width=True)
    with c2:
        st.plotly_chart(px.scatter(view, x="student_attendance", y=target, color="school_open", template="plotly_dark", title=f"Attendance vs {LABELS[target]}"), use_container_width=True)
    numeric = view.select_dtypes(include=np.number)
    st.plotly_chart(px.imshow(numeric.corr(), text_auto=".2f", aspect="auto", template="plotly_dark", title="Numeric feature correlation · association is not causation"), use_container_width=True)
    with st.expander("View filtered records and data types"):
        st.dataframe(view, hide_index=True, use_container_width=True)
        st.dataframe(pd.DataFrame({"Column": df.columns, "Data type": [str(df[c].dtype) for c in df.columns], "Missing values": [int(df[c].isna().sum()) for c in df.columns]}), hide_index=True, use_container_width=True)
    st.download_button("Download filtered records", view.to_csv(index=False).encode("utf-8"), file_name="filtered_school_resource_data.csv", mime="text/csv")

elif page == "Predict resources":
    st.subheader("Prediction centre")
    st.caption("Change the inputs to estimate daily resource use. The output is a point estimate, not a guaranteed range.")
    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            target_date = st.date_input("Target date", value=pd.Timestamp.today().date())
            opened = st.checkbox("School expected to be open", value=True)
            total = st.number_input("Total student population", min_value=1, max_value=10000, value=850, step=10)
        with c2:
            attendance = st.number_input("Expected attendance", min_value=0, max_value=int(total), value=min(740, int(total)), step=10)
            temp = st.number_input("Temperature (°C)", min_value=-10.0, max_value=55.0, value=29.0, step=0.5)
            rain = st.number_input("Rainfall (mm)", min_value=0.0, max_value=1000.0, value=2.0, step=1.0)
        with c3:
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
            event = st.checkbox("School event planned")
            holiday = st.checkbox("Holiday or exam day")
        submitted = st.form_submit_button("Estimate resource use", type="primary", use_container_width=True)
    if submitted and attendance > total:
        st.error("Expected attendance cannot exceed the total student population. Update the inputs and try again.")
    if submitted and attendance <= total:
        d = pd.Timestamp(target_date)
        row = {"date": str(target_date), "day_of_week": d.dayofweek, "month": d.month, "is_weekend": int(d.dayofweek >= 5), "school_open": int(opened), "student_attendance": int(attendance if opened else min(attendance, 8)), "total_students": int(total), "attendance_rate": float(attendance / total), "temperature_c": temp, "rainfall_mm": rain, "humidity_percent": humidity, "is_school_event": int(event and opened), "holiday_or_exam_day": int(holiday)}
        try:
            predictions = predict_resources(bundle, row)
            statuses = {}
            result_cols = st.columns(3)
            for col, target in zip(result_cols, TARGETS):
                value = predictions.get(target)
                thresholds = bundle["thresholds"].get(target, {"low": 0, "high": float("inf")})
                status = status_for(value, thresholds)
                statuses[target] = status
                with col:
                    st.metric(LABELS[target], "Unavailable" if value is None else f"{value:,.1f} {UNITS[target]}")
                    if status == "HIGH": st.error("HIGH · Review context")
                    elif status == "LOW": st.info("LOW · Verify context")
                    elif status == "NORMAL": st.success("NORMAL · Monitor")
                    else: st.warning("Prediction unavailable")
                    st.caption(f"Reference bands from training data: LOW below {thresholds['low']:,.1f}; HIGH at/above {thresholds['high']:,.1f}.")
                    st.caption("Selected model: " + bundle["reports"].get(target, {}).get("selected_model", "Unavailable"))
            st.markdown("### Recommended review actions")
            for label, heading, action in recommendations(predictions, statuses, row):
                with st.container(border=True):
                    st.markdown(f"**{label} · {heading}**")
                    st.write(action)
            export = pd.DataFrame([row | predictions | {f"{t}_status": statuses[t] for t in TARGETS}])
            st.download_button("Download this prediction", export.to_csv(index=False).encode("utf-8"), file_name="school_resource_prediction.csv", mime="text/csv")
        except Exception as exc:
            st.error(f"Could not produce a prediction: {exc}")

elif page == "Compare models":
    st.subheader("Model evaluation")
    st.info("Models are selected using validation MAE. Final test metrics use the later held-out period. Scores on simulated data do not establish real-school accuracy.")
    for target in TARGETS:
        report = bundle["reports"].get(target, {})
        with st.container(border=True):
            st.markdown(f"### {LABELS[target]}")
            if "comparisons" not in report:
                st.warning(report.get("warning", "No evaluation report available."))
                continue
            rows = [{"Model": item["model"], "Validation MAE": item["validation"]["MAE"], "Validation RMSE": item["validation"]["RMSE"], "Validation R²": item["validation"]["R2"], "Test MAE": item["test"]["MAE"], "Test RMSE": item["test"]["RMSE"], "Test R²": item["test"]["R2"]} for item in report["comparisons"]]
            metrics = pd.DataFrame(rows)
            st.dataframe(metrics.round(3), hide_index=True, use_container_width=True)
            st.markdown(f"**Selected on validation data:** {report['selected_model']}")
            st.caption(f"Rows: train {report['train_rows']:,} · validation {report['validation_rows']:,} · test {report['test_rows']:,}")
            comparison = pd.DataFrame({"Actual": report["test_actual"], "Predicted": report["test_predicted"]})
            st.plotly_chart(px.scatter(comparison, x="Actual", y="Predicted", template="plotly_dark", title="Held-out test: actual vs predicted"), use_container_width=True)
    st.download_button("Download evaluation summary", pd.json_normalize(bundle["reports"], sep="_").to_csv(index=False).encode("utf-8"), file_name="model_evaluation_summary.csv", mime="text/csv")

else:
    st.subheader("Project architecture")
    st.code("CSV data → validation → exploration → model comparison → predictions → status bands + action prompts", language="text")
    st.markdown("### Technology stack")
    tech = pd.DataFrame({"Tool": ["Python", "pandas / NumPy", "scikit-learn", "Streamlit", "Plotly", "Orange Data Mining"], "Role": ["Application logic", "Data handling and numerical operations", "Regression training and evaluation", "Interactive dashboard", "Charts and visual analysis", "Visual workflow for independent exploration and model comparison"]})
    st.dataframe(tech, hide_index=True, use_container_width=True)
    st.markdown("### Sustainable Development Goals")
    for sdg, title, explanation in [
        ("SDG 6", "Clean Water and Sanitation", "Review unusual water use and investigate possible leaks."),
        ("SDG 7", "Affordable and Clean Energy", "Review electricity use and equipment schedules."),
        ("SDG 12", "Responsible Consumption and Production", "Monitor waste patterns, segregation and reuse."),
        ("SDG 13", "Climate Action", "Use resource data to inform planning; the prototype does not prove emissions reductions."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{sdg} · {title}**")
            st.write(explanation)
    st.markdown("### Responsible use and limitations")
    st.markdown("- Demo records are synthetic and must not be presented as school measurements.\n- Uploaded data is structurally checked, but authenticity is not verified.\n- LOW/NORMAL/HIGH bands are based on training-data percentiles, not official standards.\n- Recommendations are transparent rule-based prompts, not automated control.\n- Correlation and feature relationships do not prove causation.\n- Prefer aggregate records and never upload identifiable student information.")
    st.markdown("### Orange workflow status")
    st.warning("The included Orange guide describes how to build and verify the workflow in the installed Orange version. Do not claim a genuine .ows workflow or Orange-to-Python model transfer until you have created and tested it locally.")
    st.markdown("### Project files")
    st.write("See README.md for setup, reports/ for the project report and viva preparation, tests/ for automated checks, and orange/ for the workflow guide.")
