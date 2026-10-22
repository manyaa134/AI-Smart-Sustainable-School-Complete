# Build a genuine Orange workflow
This package does not claim an unverified placeholder `.ows` is executable. Build and save the real canvas in Orange.

1. Add **File** and load `data/simulated_school_data.csv`.
2. Connect File → **Data Table**.
3. Connect File → **Select Columns**. Set one target (water first) as Target; move contextual variables to Features; ignore the other targets and date text.
4. Connect Select Columns → **Impute** if required.
5. Connect prepared data to **Distributions**, **Scatter Plot**, and **Correlations** where supported.
6. Add **Linear Regression**, **Tree**, **Random Forest** and connect learner outputs plus prepared data to **Test & Score**.
7. Choose a supported evaluation method, inspect regression metrics, then repeat for electricity and waste targets.
8. Add **Predictions** only if the installed Orange version supports the desired connections.
9. Resolve warnings, run the canvas, and save as `orange/school_sustainability.ows`.

Widget ports/settings vary by version. If Orange cannot perform a chronological split, label its scores separately; use the Python chronological split as the primary forecast-oriented evaluation. Orange models do not automatically power the Streamlit app.

Screenshots: full canvas, target selection, Test & Score for each target, and one exploratory chart.
