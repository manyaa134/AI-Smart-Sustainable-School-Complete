# AI Smart Sustainable School 🌱
Class 12 project demonstrating resource-use prediction with synthetic school data.

**Important:** Supplied data is simulated, not real measurements. Predictions are point estimates. Percentile bands are not official standards. Recommendations do not guarantee savings.

## Windows setup
Python 3.11 is recommended. Orange may have separate compatibility needs.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.data_generator
pytest -q
streamlit run app.py
```

Run commands from the project root. If `py -3.11` is unavailable, install Python 3.11 and enable Python Launcher.

## Structure
`app.py` dashboard; `src/` generator, validation, training, prediction and rules; `data/` demo and real-data template; `orange/ORANGE_WORKFLOW_GUIDE.md`; `reports/` report, presentation, viva and demo script; `tests/` automated checks.

## Data and modelling
Required CSV columns are date, school_open, student_attendance, total_students, temperature_c, rainfall_mm, humidity_percent, is_school_event and the three target columns. Keep units consistent. Missing target values are not invented. Separate models compare a training mean baseline, Linear Regression, Decision Tree and Random Forest. First 65% dates train, next 15% select by validation MAE, final 20% test.

## Orange
Build and save the real `.ows` in Orange using the workflow guide. No fake placeholder is supplied. Orange models do not automatically power the dashboard.

## Troubleshooting
If Streamlit is not found, activate `.venv` and reinstall requirements. If `src` cannot be imported, run from project root. Keep Orange in a separate environment if packages conflict. Invalid CSVs are rejected rather than silently replaced by demo data.

## Submission checklist
- [ ] Generate dataset and run `pytest -q`
- [ ] Launch dashboard and verify simulated label
- [ ] Change inputs and confirm predictions update
- [ ] Test valid and invalid CSV uploads
- [ ] Build, run and save Orange workflow
- [ ] Capture genuine screenshots
- [ ] Add student details and actual results to report
