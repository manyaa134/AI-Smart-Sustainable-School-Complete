# 40 viva questions with answers

1. **What is the project?** A prototype estimating daily school resource use.
2. **Why this topic?** It connects data analysis with a practical sustainability problem.
3. **What is Data Science?** Using data and analytical methods to find patterns and support decisions.
4. **What is ML?** Methods that learn patterns from examples.
5. **Which ML type?** Supervised learning because training records include target values.
6. **Why regression?** Targets are numerical.
7. **Name targets.** Water litres, electricity kWh, waste kg.
8. **What are features?** Inputs such as attendance, weather and school status.
9. **Is demo data real?** No, it is simulated.
10. **Which SDGs?** 6, 7, 12 and 13.
11. **Linear Regression?** Models a numeric target using a linear combination of features.
12. **Decision Tree?** Splits records by feature conditions and predicts at a leaf.
13. **Random Forest?** Combines multiple decision trees.
14. **Why compare models?** Each target may have different patterns.
15. **What is a baseline?** A simple reference, here the training-set mean.
16. **Training set?** Data used to fit a model.
17. **Validation set?** Data used to select a model.
18. **Test set?** Held-out data used for final evaluation.
19. **Why chronological split?** It mimics using past data to predict later dates.
20. **Data leakage?** Using information that should not influence training or selection.
21. **MAE?** Average absolute error in the target's units.
22. **RMSE?** Square root of mean squared error; large errors matter more.
23. **R²?** Comparison against mean-based variation; it can be negative.
24. **Why not only R²?** MAE/RMSE show errors in litres, kWh or kg.
25. **Why a pipeline?** It keeps preprocessing with the model and reduces leakage risk.
26. **Why separate models?** Targets have different units and patterns.
27. **Why not classify LOW/HIGH directly?** Main task is regression; statuses interpret numerical predictions.
28. **How thresholds work?** Training-set 25th and 75th percentiles, not official standards.
29. **Is LOW always good?** No, it may mean closure or missing readings.
30. **Does correlation prove causation?** No.
31. **Feature importance?** Indicates model reliance, not causation.
32. **Orange's role?** Visual exploration and independent learner evaluation.
33. **Why scores differ between Orange/Python?** Splits, preprocessing and defaults can differ.
34. **What if R² is negative?** Report honestly and inspect baseline, errors and data.
35. **Missing values?** Impute eligible input features within training pipeline; do not invent targets.
36. **Privacy?** Prefer aggregate attendance and avoid identifiable student records.
37. **Are recommendations ML?** No, they use explicit rules on statuses/context.
38. **Guaranteed savings?** No, savings require separate measurement.
39. **Biggest limitation?** Simulated data does not prove real-world accuracy.
40. **Future scope?** Verified meter data, future testing, uncertainty estimates and school-specific thresholds.
