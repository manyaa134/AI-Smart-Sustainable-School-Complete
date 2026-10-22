# AI Smart Sustainable School | Class XII Project Report

**Student:** [Name] | **Class:** XII | **School:** [School] | **Teacher:** [Teacher] | **Session:** [Year]

## Certificate template
This is to certify that [Student Name] of Class XII completed the project titled *AI Smart Sustainable School* under my guidance. The work and results should be reviewed before submission.

## Acknowledgement
I thank my subject teacher, school and family for their guidance. I acknowledge the open-source Python, pandas, scikit-learn, Streamlit, Plotly and Orange communities.

## Abstract
This project demonstrates how data science can estimate daily school water, electricity and waste use. A reproducible synthetic dataset makes the prototype runnable without private school records. Python compares a training-mean baseline, Linear Regression, Decision Tree and Random Forest using chronological train, validation and test periods. A Streamlit dashboard presents exploratory charts, point predictions, statistical status bands and rule-based sustainability prompts. Orange can independently explore and evaluate the shared dataset. Simulated results do not establish real-school accuracy; recommendations do not guarantee savings.

## Introduction and problem
Schools use water and electricity and generate waste. Structured records and data analysis can help staff explore patterns, estimate resource demand and investigate unusual readings.

## Objectives
Generate reproducible data; validate CSVs; explore patterns; compare regression models; show interactive estimates; provide actionable rule-based prompts; explain alignment with SDGs 6, 7, 12 and 13.

## SDGs
**SDG 6:** water-use monitoring may support leak checks. **SDG 7:** electricity estimates may support schedule reviews. **SDG 12:** waste estimates may inform segregation and reuse. **SDG 13:** monitoring may support informed decisions, but the app does not prove emissions reductions.

## Architecture
CSV → validation and exploration → Orange independent visual workflow / Python ML pipelines → Streamlit dashboard → predictions, statistical bands and recommendations.

## Dataset and preprocessing
The dataset contains calendar, school status, attendance, weather, event context and three resource targets. See `data/dataset_dictionary.md`. The school calendar and generated relationships are assumptions. Validation checks dates, required columns, attendance, humidity, rainfall and non-negative targets. Missing target measurements are not invented.

## Machine learning
Each resource is a separate supervised regression task. The first 65% of chronological records train models, the next 15% select by validation MAE, and the final 20% are held out for testing. Preprocessing is fitted inside pipelines on training data only. MAE and RMSE use target units; R² can be negative. A training-mean baseline provides a simple reference.

## Orange and Python integration
Both tools use the same CSV and documented features. Orange independently supports visual analysis and learner evaluation; scikit-learn pipelines power the dashboard. Models are not automatically transferred between tools. Scores may differ due to preprocessing, splitting and defaults.

## Dashboard and recommendation engine
Pages include Overview, Data Explorer, Prediction Centre, Model Evaluation and About & SDGs. LOW/NORMAL/HIGH use training-set 25th and 75th percentiles, not official standards. Rules suggest meter/leak checks, equipment scheduling and waste segregation. These are prompts, not guaranteed savings.

## Testing
Run `pytest -q` and report the actual result. Include genuine screenshots only after running the application.

## Ethics, limitations and future scope
Prefer aggregate attendance; avoid identifiable student data without permission. Simulated data cannot prove real-world accuracy. Future work may use verified meter records, evaluate future real data, add uncertainty estimates and set school-specific thresholds.

## Results and conclusion
Insert actual local metrics and screenshots here. Do not invent measurements, accuracy, school approval or environmental savings. The prototype demonstrates a transparent data science workflow; operational usefulness requires verified data and human review.
