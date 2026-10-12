import pandas as pd



def load_dataset(file_path):
    """Load a CSV file."""
    df = pd.read_csv(file_path)
    return df


def detect_date_columns(df):
    """Try to identify genuine date columns."""

    date_columns = []

    for column in df.columns:

        # Only examine text columns
        if not pd.api.types.is_object_dtype(df[column]):
            continue

        # Ignore columns with too many unique values
        # because these are often IDs or free text
        if df[column].nunique() > 100:
            continue

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid_ratio = converted.notna().mean()

        if valid_ratio >= 0.80:
            date_columns.append(column)

    return date_columns


def detect_id_columns(df):
    """Identify columns that may represent IDs."""

    id_columns = []

    for column in df.columns:

        unique_count = df[column].nunique()
        total_count = len(df)

        # High uniqueness can indicate an ID column
        if total_count > 0:

            uniqueness_ratio = unique_count / total_count

            if uniqueness_ratio >= 0.95:
                id_columns.append(column)

    return id_columns

def detect_numeric_columns(df):
    """Detect columns that are stored as text but contain numbers."""

    numeric_columns = []

    for column in df.select_dtypes(include=["object", "string"]).columns:

        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        valid_ratio = converted.notna().mean()

        if valid_ratio >= 0.80:
            numeric_columns.append(column)

    return numeric_columns

def understand_dataset(df):
    """Create a complete profile of the dataset."""

    profile = {}

    # -----------------------------
    # Basic information
    # -----------------------------

    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]

    profile["column_names"] = df.columns.tolist()

    # -----------------------------
    # Data types
    # -----------------------------

    profile["data_types"] = (
        df.dtypes.astype(str).to_dict()
    )

    # -----------------------------
    # Numerical columns
    # -----------------------------

    profile["numerical_columns"] = (
        df.select_dtypes(
            include="number"
        ).columns.tolist()
    )

    profile["numeric_text_columns"] = detect_numeric_columns(df)

    # -----------------------------
    # Categorical columns
    # -----------------------------

    profile["categorical_columns"] = (
    df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()
   )

    # -----------------------------
    # Date columns
    # -----------------------------

    profile["date_columns"] = detect_date_columns(df)

    # -----------------------------
    # Possible ID columns
    # -----------------------------

    profile["possible_id_columns"] = detect_id_columns(df)

    # -----------------------------
    # Missing values
    # -----------------------------

    profile["missing_values"] = (
        df.isnull().sum().to_dict()
    )

    # -----------------------------
    # Duplicate rows
    # -----------------------------

    profile["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # -----------------------------
    # Unique values
    # -----------------------------

    profile["unique_values"] = (
        df.nunique().to_dict()
    )

    # -----------------------------
    # Basic statistics
    # -----------------------------

    profile["statistics"] = (
        df.describe(
            include="all"
        ).to_dict()
    )

    return profile


if __name__ == "__main__":

    # Your test dataset
    file_path = "Customer_Churn.csv"

    # Load dataset
    df = load_dataset(file_path)

    # Create profile
    profile = understand_dataset(df)

    print("\n================================")
    print("       DATASET PROFILE")
    print("================================")

    print("\nDataset Shape:")
    print("Rows:", profile["rows"])
    print("Columns:", profile["columns"])

    print("\nColumn Names:")
    print(profile["column_names"])

    print("\nData Types:")
    print(profile["data_types"])

    print("\nNumerical Columns:")
    print(profile["numerical_columns"])

    print("\nCategorical Columns:")
    print(profile["categorical_columns"])

    print("\nDate Columns:")
    print(profile["date_columns"])

    print("\nPossible ID Columns:")
    print(profile["possible_id_columns"])

    print("\nMissing Values:")
    print(profile["missing_values"])

    print("\nDuplicate Rows:")
    print(profile["duplicate_rows"])

    print("\nUnique Values:")
    print(profile["unique_values"])

    print("\nNumeric Columns Stored as Text:")
    print(profile["numeric_text_columns"])


def clean_dataset(df, profile):
    """
    Perform safe and explainable data cleaning.
    """

    # Make a copy so the original dataset is not changed
    cleaned_df = df.copy()

    cleaning_report = {
        "numeric_conversions": [],
        "missing_values_found": {},
        "duplicates_removed": 0,
        "whitespace_cleaned": []
    }

    # ---------------------------------
    # 1. Clean unnecessary whitespace
    # ---------------------------------

    text_columns = cleaned_df.select_dtypes(
        include=["object", "category", "string"]
    ).columns

    for column in text_columns:

        original = cleaned_df[column].copy()

        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.strip()
        )

        if not original.equals(cleaned_df[column]):
            cleaning_report["whitespace_cleaned"].append(column)

    # ---------------------------------
    # 2. Convert common missing markers
    # ---------------------------------

    missing_markers = [
        "",
        " ",
        "?",
        "NA",
        "N/A",
        "na",
        "n/a",
        "NULL",
        "null",
        "None",
        "none"
    ]

    cleaned_df = cleaned_df.replace(
        missing_markers,
        pd.NA
    )

    # ---------------------------------
    # 3. Convert numeric-looking text
    # ---------------------------------

    numeric_text_columns = profile[
        "numeric_text_columns"
    ]

    for column in numeric_text_columns:

        cleaned_df[column] = pd.to_numeric(
            cleaned_df[column],
            errors="coerce"
        )

        cleaning_report[
            "numeric_conversions"
        ].append(column)

    # ---------------------------------
    # 4. Handle missing values
    # ---------------------------------

    missing_values = cleaned_df.isnull().sum()

    cleaning_report[
        "missing_values_found"
    ] = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    # Apply 5% missing-value rule
    for column in cleaned_df.columns:

        missing_count = cleaned_df[column].isnull().sum()

        if missing_count == 0:
            continue

        missing_percentage = (
            missing_count / len(cleaned_df)
        ) * 100

        # More than 5% missing → drop rows
        if missing_percentage > 5:

            cleaned_df = cleaned_df.dropna(
                subset=[column]
            )

        # 5% or less → impute
        else:

            # Numerical column → median
            if pd.api.types.is_numeric_dtype(
                cleaned_df[column]
            ):

                median_value = cleaned_df[column].median()

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(median_value)
                )

            # Categorical/text column → mode
            else:

                mode_values = cleaned_df[column].mode()

                if not mode_values.empty:

                    mode_value = mode_values.iloc[0]

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(mode_value)
                    )

    # ---------------------------------
    # 5. Remove exact duplicate rows
    # ---------------------------------

    duplicate_count = int(
        cleaned_df.duplicated().sum()
    )

    cleaned_df = cleaned_df.drop_duplicates()

    cleaning_report[
        "duplicates_removed"
    ] = duplicate_count

    return cleaned_df, cleaning_report


if __name__ == "__main__":
    profile = understand_dataset(df)
        # Clean the dataset
    cleaned_df, cleaning_report = clean_dataset(
        df,
        profile
    )
    print("\n================================")
    print("       CLEANING REPORT")
    print("================================")

    print("\nNumeric conversions:")
    print(cleaning_report["numeric_conversions"])

    print("\nWhitespace cleaned:")
    print(cleaning_report["whitespace_cleaned"])

    print("\nMissing values found:")
    print(cleaning_report["missing_values_found"])

    print("\nDuplicate rows removed:")
    print(cleaning_report["duplicates_removed"])

    print("\nOriginal shape:")
    print(df.shape)

    print("\nCleaned shape:")
    print(cleaned_df.shape)
    cleaned_profile = understand_dataset(
        cleaned_df
     )
    print("\n================================")
    print("   AFTER CLEANING")
    print("================================")

    print("\nData Types:")
    print(cleaned_profile["data_types"])

    print("\nNumerical Columns:")
    print(cleaned_profile["numerical_columns"])

    print("\nCategorical Columns:")
    print(cleaned_profile["categorical_columns"])

def analyze_numerical_columns(df, profile):

    numerical_analysis = {}

    numerical_columns = profile[
        "numerical_columns"
    ]

    for column in numerical_columns:

        data = df[column]

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)

        numerical_analysis[column] = {
            "count": int(data.count()),
            "missing": int(data.isnull().sum()),
            "mean": float(data.mean()),
            "median": float(data.median()),
            "minimum": float(data.min()),
            "maximum": float(data.max()),
            "standard_deviation": float(data.std()),
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(q3 - q1)
        }

    return numerical_analysis

def analyze_categorical_columns(df, profile):

    categorical_analysis = {}

    categorical_columns = profile[
        "categorical_columns"
    ]

    for column in categorical_columns:

        data = df[column]

        value_counts = data.value_counts(
            dropna=False
        )

        categorical_analysis[column] = {
            "unique_categories": int(
                data.nunique(dropna=True)
            ),
            "missing": int(
                data.isnull().sum()
            ),
            "most_common": (
                value_counts.index[0]
                if len(value_counts) > 0
                else None
            ),
            "most_common_count": (
                int(value_counts.iloc[0])
                if len(value_counts) > 0
                else 0
            ),
            "distribution": value_counts.to_dict()
        }

    return categorical_analysis


def analyze_outliers(df, profile):
    """
    Detect outliers in numerical columns using the IQR method.
    """

    outlier_analysis = {}

    numerical_columns = profile["numerical_columns"]

    for column in numerical_columns:

        data = df[column].dropna()

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)

        iqr = q3 - q1

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        outliers = data[
            (data < lower_limit) |
            (data > upper_limit)
        ]

        outlier_count = len(outliers)
        total_count = len(data)

        if total_count > 0:
            outlier_percentage = (
                outlier_count / total_count
            ) * 100
        else:
            outlier_percentage = 0

        outlier_analysis[column] = {
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_limit": float(lower_limit),
            "upper_limit": float(upper_limit),
            "outlier_count": int(outlier_count),
            "outlier_percentage": float(
                outlier_percentage
            )
        }

    return outlier_analysis




if __name__ == "__main__":

    file_path = "customer_churn.csv"

    # Load dataset
    df = load_dataset(file_path)

    # Create initial profile
    profile = understand_dataset(df)

    # Clean dataset
    cleaned_df, cleaning_report = clean_dataset(
        df,
        profile
    )

    # Create profile after cleaning
    cleaned_profile = understand_dataset(
        cleaned_df
    )

    # EDA
    numerical_analysis = analyze_numerical_columns(
        cleaned_df,
        cleaned_profile
    )
    categorical_analysis = analyze_categorical_columns(
    cleaned_df,
    cleaned_profile
    )
    outlier_analysis = analyze_outliers(
    cleaned_df,
    cleaned_profile
    )


def analyze_outliers(df, profile):
    """
    Detect outliers in continuous numerical columns
    using the IQR method.
    """
    print("NEW OUTLIER FUNCTION IS RUNNING")

    outlier_analysis = {}

    numerical_columns = profile["numerical_columns"]

    for column in numerical_columns:

        data = df[column].dropna()

        # Check whether the column is binary
        unique_values = data.nunique()

        if unique_values <= 2:

            outlier_analysis[column] = {
                "status": "Skipped - binary variable",
                "outlier_count": 0,
                "outlier_percentage": 0
            }

            continue

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)

        iqr = q3 - q1

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        outliers = data[
            (data < lower_limit) |
            (data > upper_limit)
        ]

        outlier_count = len(outliers)
        total_count = len(data)

        if total_count > 0:
            outlier_percentage = (
                outlier_count / total_count
            ) * 100
        else:
            outlier_percentage = 0

        outlier_analysis[column] = {
            "status": "Analyzed",
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_limit": float(lower_limit),
            "upper_limit": float(upper_limit),
            "outlier_count": int(outlier_count),
            "outlier_percentage": float(
                outlier_percentage
            )
        }

    return outlier_analysis

    categorical_analysis = analyze_categorical_columns(
        cleaned_df,
        cleaned_profile
    )

    outlier_analysis = analyze_outliers(
    cleaned_df,
    cleaned_profile
    )

    print("\n================================")
    print("       NUMERICAL ANALYSIS")
    print("================================")

    for column, analysis in numerical_analysis.items():

        print("\nColumn:", column)
        print("Count:", analysis["count"])
        print("Missing:", analysis["missing"])
        print("Mean:", round(analysis["mean"], 2))
        print("Median:", round(analysis["median"], 2))
        print("Minimum:", round(analysis["minimum"], 2))
        print("Maximum:", round(analysis["maximum"], 2))
        print(
            "Standard Deviation:",
            round(analysis["standard_deviation"], 2)
        )
        print("Q1:", round(analysis["q1"], 2))
        print("Q3:", round(analysis["q3"], 2))
        print("IQR:", round(analysis["iqr"], 2))

    print("\n================================")
    print("       CATEGORICAL ANALYSIS")
    print("================================")

    for column, analysis in categorical_analysis.items():

        print("\nColumn:", column)
        print(
            "Unique Categories:",
            analysis["unique_categories"]
        )
        print("Missing:", analysis["missing"])
        print(
            "Most Common:",
            analysis["most_common"]
        )
        print(
            "Most Common Count:",
            analysis["most_common_count"]
        )
        print(
            "Distribution:",
            analysis["distribution"]
        )

    categorical_analysis = analyze_categorical_columns(
    cleaned_df,
    cleaned_profile
)
    outlier_analysis = analyze_outliers(
        cleaned_df,
        cleaned_profile
    )

    print(
    "Distribution:",
    analysis["distribution"]
)
    #print("\n================================")
    #print("       OUTLIER ANALYSIS")
    #print("================================")

#for column, analysis in outlier_analysis.items():

    #print("\nColumn:", column)

    #if "status" not in analysis:
     #   print("DEBUG - Missing status:", analysis)
      #  continue

#    if analysis["status"] == "Skipped - binary variable":

 #       print("Status: Skipped - binary variable")

  #  else:

   #     print(
    #        "Lower Limit:",
     #       round(analysis["lower_limit"], 2)
      #  )

       # print(
        #    "Upper Limit:",
         #   round(analysis["upper_limit"], 2)
        #)

        #print(
         #   "Outlier Count:",
          #  analysis["outlier_count"]
        #)

        #print(
         #   "Outlier Percentage:",
          #  round(
           #     analysis["outlier_percentage"],
            #    2
           # ),
            #"%"
        #)


