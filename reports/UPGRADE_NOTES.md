# Upgrade notes

This revision improves the Streamlit interface and usability while preserving the project's Class 12 scope.

## Changes
- Replaced the light interface with a restrained dark teal/navy dashboard.
- Added consistent labels and units for water, electricity and waste.
- Added dataset-health checks and active-source labelling.
- Added filtered data exports and an active-dataset download.
- Added a single-prediction CSV export.
- Improved model comparison presentation and evaluation-summary export.
- Added more explicit source authenticity, synthetic-data and Orange-workflow limitations.
- Kept LOW/NORMAL/HIGH as percentile-based reference bands, not official standards.
- Cached model evaluation within a Streamlit session to reduce repeated computation.

## Verification still required on the student's laptop
1. Install dependencies and run `python -m pytest -q`.
2. Launch with `streamlit run app.py` and test each page.
3. Upload a valid CSV and an invalid CSV to verify both paths.
4. Build and save the Orange workflow in the installed Orange version, then capture genuine screenshots.
5. Do not describe the app as real-time or claim measured school savings unless connected to real instruments and validated data.
