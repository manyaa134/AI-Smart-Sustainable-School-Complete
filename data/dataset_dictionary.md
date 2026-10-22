# Dataset dictionary
730 simulated daily records from 2024-01-01, generated with seed 42. These are not real school measurements.

| Column | Type/unit | Purpose |
|---|---|---|
| date | ISO date | Record date |
| day_of_week | integer, Monday=0 | Weekday |
| month | integer 1–12 | Calendar month |
| is_weekend | binary | Weekend flag |
| school_open | binary | Simulated school operation |
| student_attendance | students | Attending students |
| total_students | students | Assumed population (850) |
| attendance_rate | proportion | Attendance divided by population |
| temperature_c | °C | Simulated temperature |
| rainfall_mm | mm | Simulated rainfall |
| humidity_percent | % | Simulated humidity |
| is_school_event | binary | Event flag |
| event_type | category | Event category or none |
| holiday_or_exam_day | binary | Simplified calendar flag |
| water_consumption_litres | L/day | Regression target |
| electricity_consumption_kwh | kWh/day | Regression target |
| waste_generation_kg | kg/day | Regression target |

The generator encodes plausible directional relationships plus random variation. Calendar and population are simplified assumptions. Target formulas are not exposed as input columns.
