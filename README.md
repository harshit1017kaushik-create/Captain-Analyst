# Captain Analyst 🧢

**Captain Analyst** is a Streamlit-based data analysis application. Upload a CSV or Excel dataset and explore automated data profiling, cleaning, exploratory data analysis (EDA), AI-style insight summaries, dashboard recommendations, and a downloadable HTML analysis report.

## Features

- Upload CSV and Excel (`.xlsx`) datasets
- Profile dataset dimensions, column types, missing values, duplicates, and possible ID/date/numeric-text columns
- Clean common missing-value markers, whitespace, numeric-looking text, missing values, and duplicate rows
- Explore numerical and categorical summaries, outlier analysis, correlations, relationships, and target-related patterns
- Generate data-driven insight summaries
- Recommend dashboard KPIs, charts, X/Y axes, and filter fields
- Download a portable HTML analysis report and a cleaned CSV

> **Note:** Recommendations and insights depend on the columns and values in the uploaded dataset. Review automated findings before using them for business decisions.

## Project structure

```text
Captain_Analyst/
├── captain_simulator.py   # Streamlit application
├── data_engine.py         # Dataset profiling and cleaning
├── analyze.py             # EDA and insight functions
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- pip

## Run locally

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. (Recommended) Create and activate a virtual environment.

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run captain_simulator.py
   ```

6. Open the local URL printed in the terminal by Streamlit and upload your own CSV or Excel dataset.

## Dependencies

The core app uses Streamlit, pandas, Matplotlib, and openpyxl for Excel file support. See `requirements.txt` for the package list.

## Data and privacy

No dataset is included in this repository by default. Upload a dataset from the app. Do not upload private, confidential, or personally identifiable data to a public repository. Use anonymized/sample data for demos and screenshots.

## Known limitations

- Automated cleaning choices (such as row removal when a column has substantial missingness) may not suit every dataset. Check the cleaning output before relying on results.
- Dashboard recommendations are suggestions; they are not a substitute for validating chart choices and business context.
- AI-style insights are generated from available data and should be checked for correctness.

## Future improvements

## 🚀 Live Demo

**Try Captain Analyst here:** [[Open Captain Analyst](YOUR_STREAMLIT_APP_URL)](https://captain-analyst-h33zrtldmxkpteikyv8per.streamlit.app/)

Upload a CSV or Excel dataset to explore automated data analysis, AI-generated insights, interactive dashboards, and downloadable reports.

- Add automated tests and a sample dataset with non-sensitive data
- Add deployment instructions for a hosted Streamlit version
- Add screenshots and a short demo video
