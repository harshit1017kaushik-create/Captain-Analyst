import pandas as pd
import matplotlib.pyplot as plt
import os


# Create charts folder
charts_folder = "charts"

if not os.path.exists(charts_folder):
    os.makedirs(charts_folder)

print("Charts folder is ready.")

# Dataset loading is handled by the Streamlit app. Analysis functions receive the uploaded dataframe.





# -----------------------------------------
# Outlier Analysis
# -----------------------------------------

def analyze_outliers(df):

    outlier_analysis = {}

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for column in numerical_columns:

        data = df[column].dropna()

        unique_values = data.nunique()

        # Skip binary variables
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

        outlier_percentage = (
            outlier_count / total_count
        ) * 100

        outlier_analysis[column] = {

            "status": "Analyzed",

            "lower_limit": lower_limit,

            "upper_limit": upper_limit,

            "outlier_count": outlier_count,

            "outlier_percentage":
                outlier_percentage
        }

    return outlier_analysis


# -----------------------------------------
# Run Analysis
# -----------------------------------------
    results = analyze_outliers(df)


# -----------------------------------------
# Display Results
# -----------------------------------------
if __name__ == "__main__":
    results = analyze_outliers(df)
    print("\n================================")
    print("       OUTLIER ANALYSIS")
    print("================================")

    for column, analysis in results.items():

        print("\nColumn:", column)

        if analysis["status"] == (
            "Skipped - binary variable"
        ):

            print(
                "Status: Skipped - binary variable"
            )

        else:

            print(
                "Lower Limit:",
                round(
                    analysis["lower_limit"],
                    2
                )
            )

            print(
                "Upper Limit:",
                round(
                    analysis["upper_limit"],
                    2
                )
            )

            print(
                "Outlier Count:",
                analysis["outlier_count"]
            )

            print(
                "Outlier Percentage:",
                round(
                    analysis["outlier_percentage"],
                    2
                ),
                "%"
            )


    # -----------------------------------------
    # Correlation Analysis
    # -----------------------------------------

    correlation = df.select_dtypes(
        include=["number"]
    ).corr()

    print("\n================================")
    print("       CORRELATION ANALYSIS")
    print("================================")

    print(correlation.round(2))


    # -----------------------------------------
    # Strong Correlation Detection
    # -----------------------------------------

    print("\n================================")
    print("       STRONG CORRELATIONS")
    print("================================")

    columns = correlation.columns

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            column1 = columns[i]
            column2 = columns[j]

            value = correlation.loc[
                column1,
                column2
            ]

            if abs(value) >= 0.70:

                print(
                    column1,
                    "<->",
                    column2,
                    ":",
                    round(value, 2)
                )
    # -----------------------------------------
    # Categorical Analysis
    # -----------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    print("\n================================")
    print("       CATEGORICAL ANALYSIS")
    print("================================")

    for column in categorical_columns:

        print("\nColumn:", column)

        print(
            "Unique Values:",
            df[column].nunique()
        )

        print(
            "Value Distribution:"
        )

        print(
            df[column].value_counts(
                dropna=False
            )
        )
    # -----------------------------------------
    # Identifier Detection
    # -----------------------------------------

    print("\n================================")
    print("       IDENTIFIER DETECTION")
    print("================================")

    for column in df.columns:

        unique_count = df[column].nunique()

        total_count = len(df)

        unique_ratio = unique_count / total_count

        if unique_ratio >= 0.95:

            print(
                column,
                "-> Possible Identifier"
            )
    # -----------------------------------------
    # Categorical vs Numerical Analysis
    # -----------------------------------------

    print("\n================================")
    print("   IMPORTANT CATEGORY DIFFERENCES")
    print("================================")

    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for categorical in categorical_columns:

        # Skip identifier columns
        if df[categorical].nunique() / len(df) >= 0.95:
            continue

        for numerical in numerical_columns:

            result = df.groupby(
                categorical
            )[numerical].mean()

            if len(result) < 2:
                continue

            difference = result.max() - result.min()

            print(
                "\n",
                categorical,
                "vs",
                numerical
            )

            print(
                "Difference:",
                round(difference, 2)
            )

            print(
                "Highest:",
                result.idxmax(),
                "=",
                round(result.max(), 2)
            )

            print(
                "Lowest:",
                result.idxmin(),
                "=",
                round(result.min(), 2)
            )

    # -----------------------------------------
    # Important Relationship Detection
    # -----------------------------------------

    print("\n================================")
    print("   MOST IMPORTANT RELATIONSHIPS")
    print("================================")

    important_relationships = []

    for categorical in categorical_columns:

        if df[categorical].nunique() / len(df) >= 0.95:
            continue

        for numerical in numerical_columns:

            result = df.groupby(
                categorical
            )[numerical].mean()

            if len(result) < 2:
                continue

            difference = result.max() - result.min()

            important_relationships.append({
                "categorical": categorical,
                "numerical": numerical,
                "difference": difference
            })


    important_relationships.sort(
        key=lambda x: x["difference"],
        reverse=True
    )


    for relationship in important_relationships[:10]:

        print(
            relationship["categorical"],
            "vs",
            relationship["numerical"],
            "-> Difference:",
            round(
                relationship["difference"],
                2
            )
        )


    # -----------------------------------------
    # Possible Target Detection
    # -----------------------------------------

    print("\n================================")
    print("       POSSIBLE TARGET COLUMNS")
    print("================================")

    target_keywords = [
        "target",
        "churn",
        "outcome",
        "result",
        "label",
        "status",
        "response",
        "sales",
        "revenue",
        "profit"
    ]

    possible_targets = []

    for column in df.columns:

        column_lower = column.lower()

        for keyword in target_keywords:

            if keyword in column_lower:

                possible_targets.append(column)

                break


    for column in possible_targets:

        print(
            column,
            "-> Possible Target"
        )

    # -----------------------------------------
    # Target Rate Analysis
    # -----------------------------------------

    print("\n================================")
    print("       TARGET RATE ANALYSIS")
    print("================================")

    if possible_targets:

        target = possible_targets[0]

        print("\nTarget:", target)

        categorical_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in categorical_columns:

            if column == target:
                continue

            if df[column].nunique() / len(df) >= 0.95:
                continue

            target_rate = df.groupby(
                column
            )[target].apply(
                lambda x: (
                    x.astype(str).str.lower() == "yes"
                ).mean() * 100
            )

            print(
                "\n",
                column,
                "vs",
                target
            )

            print(
                target_rate.round(2)
            )


    # -----------------------------------------
    # Important Target Relationships
    # -----------------------------------------

    print("\n================================")
    print("   IMPORTANT TARGET RELATIONSHIPS")
    print("================================")

    target_relationships = []

    if possible_targets:

        target = possible_targets[0]

        for column in categorical_columns:

            if column == target:
                continue

            if df[column].nunique() / len(df) >= 0.95:
                continue

            target_rate = df.groupby(
                column
            )[target].apply(
                lambda x: (
                    x.astype(str).str.lower() == "yes"
                ).mean() * 100
            )

            if len(target_rate) < 2:
                continue

            spread = (
                target_rate.max()
                - target_rate.min()
            )

            target_relationships.append({
                "column": column,
                "spread": spread
            })

        target_relationships.sort(
            key=lambda x: x["spread"],
            reverse=True
        )

        for relationship in target_relationships[:10]:

            print(
                relationship["column"],
                "-> Target spread:",
                round(
                    relationship["spread"],
                    2
                ),
                "percentage points"
            )


    # -----------------------------------------
    # Numerical vs Target Analysis
    # -----------------------------------------

    print("\n================================")
    print("   NUMERICAL vs TARGET")
    print("================================")

    if possible_targets:

        target = possible_targets[0]

        for column in numerical_columns:

            result = df.groupby(
                target
            )[column].mean()

            print(
                "\n",
                column,
                "vs",
                target
            )

            print(
                result.round(2)
            )


    # -----------------------------------------
    # Important Numerical Target Relationships
    # -----------------------------------------

    print("\n================================")
    print(" IMPORTANT NUMERICAL RELATIONSHIPS")
    print("================================")

    numerical_target_relationships = []

    if possible_targets:

        target = possible_targets[0]

        for column in numerical_columns:

            result = df.groupby(
                target
            )[column].mean()

            if len(result) < 2:
                continue

            difference = result.max() - result.min()

            numerical_target_relationships.append({
                "column": column,
                "difference": difference
            })

        numerical_target_relationships.sort(
            key=lambda x: x["difference"],
            reverse=True
        )

        for relationship in numerical_target_relationships:

            print(
                relationship["column"],
                "-> Difference:",
                round(
                    relationship["difference"],
                    2
                )
            )



    # -----------------------------------------
    # Automatic Categorical Visualizations
    # -----------------------------------------

    print("\n================================")
    print("   CREATING CATEGORICAL CHARTS")
    print("================================")

    print("Categorical visualization started")
    print("Categorical columns:", categorical_columns)

    for column in categorical_columns:

        # Skip ID-like columns
        if column == "customerID":
            continue

        value_counts = df[column].value_counts()

        plt.figure(figsize=(8, 5))

        value_counts.plot(kind="bar")

        plt.title(
            "Distribution of " + column
        )

        plt.xlabel(column)

        plt.ylabel("Count")

        plt.xticks(rotation=45)

        plt.tight_layout()

        file_name = column.replace(" ", "_") + "_distribution.png"

        plt.savefig(
        os.path.join(charts_folder, file_name)
        )

        plt.show()

        plt.close()


    # -----------------------------------------
    # Target-Based Visualizations
    # -----------------------------------------

    print("\n================================")
    print("   CREATING TARGET CHARTS")
    print("================================")

    if possible_targets:

        target = possible_targets[0]

        for column in categorical_columns:

            if column == target:
                continue

            if column == "customerID":
                continue

            if df[column].nunique() > 10:
                continue

            cross_table = pd.crosstab(
                df[column],
                df[target]
            )

            cross_table.plot(
                kind="bar",
                figsize=(8, 5)
            )

            plt.title(
                column + " vs " + target
            )

            plt.xlabel(column)
            plt.ylabel("Count")

            plt.xticks(rotation=45)

            plt.tight_layout()

            file_name = (
                column.replace(" ", "_")
                + "_vs_"
                + target.replace(" ", "_")
                + ".png"
            )

            plt.savefig(
                os.path.join(
                    charts_folder,
                    file_name
                )
            )

            plt.show()

            plt.close()


    print("\n================================")
    print("   RELATIONSHIP INSIGHTS")
    print("================================")

    if possible_targets:

        target = possible_targets[0]

        relationship_scores = []

        for column in categorical_columns:

            if column == target:
                continue

            if column == "customerID":
                continue

            if df[column].nunique() > 10:
                continue

            target_rates = (
                df.groupby(column)[target]
                .apply(
                    lambda x: (x == "Yes").mean() * 100
                )
            )

            if len(target_rates) > 1:

                spread = (
                    target_rates.max()
                    - target_rates.min()
                )

                relationship_scores.append(
                    (column, spread)
                )

        relationship_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        print("\nStrongest categorical relationships:")

        for column, spread in relationship_scores[:5]:

            print(
                column,
                "-> Target rate spread:",
                round(spread, 2),
                "percentage points"
            )


    # -----------------------------------------
    # Category-Level Insights
    # -----------------------------------------

    print("\n================================")
    print("   CATEGORY-LEVEL INSIGHTS")
    print("================================")

    if possible_targets:

        target = possible_targets[0]

        for column, spread in relationship_scores[:5]:

            target_rates = (
                df.groupby(column)[target]
                .apply(
                    lambda x: (x == "Yes").mean() * 100
                )
            )

            highest_category = target_rates.idxmax()
            highest_rate = target_rates.max()

            lowest_category = target_rates.idxmin()
            lowest_rate = target_rates.min()

            print("\n", column)

            print(
                "Highest target rate:",
                highest_category,
                "->",
                round(highest_rate, 2),
                "%"
            )

            print(
                "Lowest target rate:",
                lowest_category,
                "->",
                round(lowest_rate, 2),
                "%"
            )

            print(
                "Difference:",
                round(spread, 2),
                "percentage points"
            )


def recommend_dashboard(cleaned_df, target_column=None):
    """
    Recommend KPIs, charts, and slicers
    based on the structure of the uploaded dataset.
    """

    recommendations = {
        "kpis": [],
        "charts": [],
        "slicers": []
    }

    # ---------------------------------
    # 1. Detect target automatically
    # ---------------------------------

    if target_column is None:

        target_keywords = [
            "target",
            "churn",
            "outcome",
            "label",
            "sales",
            "revenue",
            "profit"
        ]

        for column in cleaned_df.columns:

            column_name = str(column).lower()

            if any(
                keyword in column_name
                for keyword in target_keywords
            ):
                target_column = column
                break

    # ---------------------------------
    # 2. Identify column types
    # ---------------------------------

    numeric_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = cleaned_df.select_dtypes(
        include=[
            "object",
            "category",
            "string",
            "bool"
        ]
    ).columns.tolist()

    # ---------------------------------
    # 3. KPI recommendations
    # ---------------------------------

    recommendations["kpis"].append(
        "Total Records"
    )

    for column in numeric_columns:

        if column == target_column:
            continue

        if cleaned_df[column].nunique(
            dropna=True
        ) <= 2:
            continue

        recommendations["kpis"].append(
            f"Average {column}"
        )

        if len(recommendations["kpis"]) >= 5:
            break

    # Target KPIs

    if target_column is not None:

        recommendations["kpis"].append(
            f"{target_column} Count"
        )

        recommendations["kpis"].append(
            f"{target_column} Rate"
        )

    # ---------------------------------
    # 4. Target vs categorical columns
    # ---------------------------------

    if target_column is not None:

        for column in categorical_columns:

            if column == target_column:
                continue

            unique_count = (
                cleaned_df[column]
                .nunique(dropna=True)
            )

            if 2 <= unique_count <= 10:

                recommendations["charts"].append({

                    "column": column,

                    "comparison": target_column,

                    "visual": (
                        "Clustered Column Chart"
                    ),

                    "purpose": (
                        f"Compare {target_column} "
                        f"across {column}"
                    )
                })

    # ---------------------------------
    # 5. Target vs numerical columns
    # ---------------------------------

    if target_column is not None:

        for column in numeric_columns:

            if column == target_column:
                continue

            if cleaned_df[column].nunique(
                dropna=True
            ) <= 2:
                continue

            recommendations["charts"].append({

                "column": column,

                "comparison": target_column,

                "visual": (
                    "Box Plot / Histogram"
                ),

                "purpose": (
                    f"Analyze {column} "
                    f"against {target_column}"
                )
            })

    # ---------------------------------
    # 6. General charts
    # ---------------------------------

    for column in categorical_columns:

        if column == target_column:
            continue

        unique_count = (
            cleaned_df[column]
            .nunique(dropna=True)
        )

        if 2 <= unique_count <= 10:

            recommendations["charts"].append({

                "column": column,

                "comparison": "Distribution",

                "visual": "Bar Chart",

                "purpose": (
                    f"Show distribution of "
                    f"{column}"
                )
            })

    # ---------------------------------
    # 7. Numerical relationships
    # ---------------------------------

    if len(numeric_columns) >= 2:

        recommendations["charts"].append({

            "column": (
                f"{numeric_columns[0]} "
                f"vs "
                f"{numeric_columns[1]}"
            ),

            "comparison": (
                f"{numeric_columns[0]} "
                f"and "
                f"{numeric_columns[1]}"
            ),

            "visual": "Scatter Plot",

            "purpose": (
                "Analyze relationship between "
                "two numerical variables"
            )
        })

    # ---------------------------------
    # 8. Slicer recommendations
    # ---------------------------------

    for column in categorical_columns:

        unique_count = (
            cleaned_df[column]
            .nunique(dropna=True)
        )

        if 2 <= unique_count <= 10:

            recommendations["slicers"].append(
                column
            )

    # ---------------------------------
    # 9. Remove duplicate charts
    # ---------------------------------

    unique_charts = []

    for chart in recommendations["charts"]:

        if chart not in unique_charts:

            unique_charts.append(
                chart
            )

    recommendations["charts"] = (
        unique_charts
    )

    return recommendations


# -----------------------------------------
# AI Insights Engine
# -----------------------------------------

def generate_insights(cleaned_df):

    insights = []

    # ---------------------------------
    # Dataset overview
    # ---------------------------------

    rows = len(cleaned_df)
    columns = len(cleaned_df.columns)

    insights.append(
        f"The dataset contains {rows:,} records "
        f"and {columns} columns."
    )

    # ---------------------------------
    # Numerical insights
    # ---------------------------------

    numerical_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    for column in numerical_columns:

        data = cleaned_df[column].dropna()

        if len(data) == 0:
            continue

        mean_value = data.mean()
        max_value = data.max()
        min_value = data.min()

        insights.append(
            f"{column}: average = {mean_value:.2f}, "
            f"minimum = {min_value:.2f}, "
            f"maximum = {max_value:.2f}."
        )

    # ---------------------------------
    # Categorical insights
    # ---------------------------------

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category", "string", "bool"]
    ).columns.tolist()

    for column in categorical_columns:

        unique_count = cleaned_df[column].nunique(
            dropna=True
        )

        if unique_count == 0:
            continue

        # Avoid extremely high-cardinality columns
        if unique_count > 20:
            continue

        most_common = (
            cleaned_df[column]
            .value_counts(dropna=True)
            .head(1)
        )

        if not most_common.empty:

            category = most_common.index[0]
            count = most_common.iloc[0]

            percentage = (
                count / len(cleaned_df)
            ) * 100

            insights.append(
                f"{column}: '{category}' is the "
                f"most common category "
                f"({percentage:.1f}% of records)."
            )

    # ---------------------------------
    # Missing value insight
    # ---------------------------------

    missing = cleaned_df.isna().sum().sum()

    if missing > 0:

        insights.append(
            f"The cleaned dataset still contains "
            f"{missing:,} missing values."
        )

    else:

        insights.append(
            "No missing values remain after cleaning."
        )

    # ---------------------------------
    # Duplicate insight
    # ---------------------------------

    duplicates = cleaned_df.duplicated().sum()

    if duplicates > 0:

        insights.append(
            f"{duplicates:,} duplicate records "
            f"are present in the cleaned dataset."
        )

    else:

        insights.append(
            "No duplicate records are present "
            "in the cleaned dataset."
        )

    return insights

# -----------------------------------------
# Numerical EDA Analysis
# -----------------------------------------

def analyze_numerical_columns(cleaned_df):

    numerical_analysis = {}

    numerical_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns

    for column in numerical_columns:

        data = cleaned_df[column].dropna()

        if len(data) == 0:
            continue

        numerical_analysis[column] = {
            "count": int(data.count()),
            "mean": float(data.mean()),
            "median": float(data.median()),
            "minimum": float(data.min()),
            "maximum": float(data.max()),
            "standard_deviation": float(data.std())
        }

    return numerical_analysis

# -----------------------------------------
# Categorical EDA Analysis
# -----------------------------------------

def analyze_categorical_columns(cleaned_df):

    categorical_analysis = {}

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category", "string", "bool"]
    ).columns

    for column in categorical_columns:

        data = cleaned_df[column]

        unique_categories = int(
            data.nunique(dropna=True)
        )

        missing = int(
            data.isna().sum()
        )

        distribution = (
            data.value_counts(
                dropna=False
            )
            .to_dict()
        )

        if not data.dropna().empty:

            most_common = (
                data.dropna()
                .value_counts()
                .idxmax()
            )

            most_common_count = int(
                data.dropna()
                .value_counts()
                .max()
            )

        else:

            most_common = None
            most_common_count = 0

        categorical_analysis[column] = {

            "unique_categories":
                unique_categories,

            "missing":
                missing,

            "most_common":
                most_common,

            "most_common_count":
                most_common_count,

            "distribution":
                distribution
        }

    return categorical_analysis


# -----------------------------------------
# Outlier EDA Analysis
# -----------------------------------------

def analyze_outliers(cleaned_df):

    outlier_analysis = {}

    numerical_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns

    for column in numerical_columns:

        data = cleaned_df[column].dropna()

        if len(data) == 0:
            continue

        unique_values = data.nunique()

        # Skip binary variables
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

        outlier_percentage = (
            outlier_count / total_count
        ) * 100

        outlier_analysis[column] = {

            "status": "Analyzed",

            "lower_limit": float(
                lower_limit
            ),

            "upper_limit": float(
                upper_limit
            ),

            "outlier_count": int(
                outlier_count
            ),

            "outlier_percentage": float(
                outlier_percentage
            )
        }

    return outlier_analysis

# -----------------------------------------
# Correlation EDA Analysis
# -----------------------------------------

def analyze_correlations(cleaned_df):

    numerical_df = cleaned_df.select_dtypes(
        include=["number"]
    )

    if numerical_df.shape[1] < 2:

        return {
            "correlation_matrix": {},
            "strong_correlations": []
        }

    correlation_matrix = (
        numerical_df.corr()
    )

    strong_correlations = []

    columns = correlation_matrix.columns

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            column1 = columns[i]
            column2 = columns[j]

            value = correlation_matrix.loc[
                column1,
                column2
            ]

            if abs(value) >= 0.70:

                strong_correlations.append({

                    "column1": column1,

                    "column2": column2,

                    "correlation": float(value)
                })

    return {

        "correlation_matrix":
            correlation_matrix,

        "strong_correlations":
            strong_correlations
    }

# -----------------------------------------
# Categorical vs Numerical Analysis
# -----------------------------------------

def analyze_relationships(cleaned_df):

    relationships = []

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category", "string", "bool"]
    ).columns

    numerical_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns

    for categorical in categorical_columns:

        # Skip identifier-like columns
        if len(cleaned_df) > 0:

            unique_ratio = (
                cleaned_df[categorical].nunique(
                    dropna=True
                ) / len(cleaned_df)
            )

            if unique_ratio >= 0.95:
                continue

        for numerical in numerical_columns:

            grouped = cleaned_df.groupby(
                categorical,
                dropna=False
            )[numerical].mean()

            if len(grouped) < 2:
                continue

            difference = (
                grouped.max() -
                grouped.min()
            )

            relationships.append({

                "categorical":
                    categorical,

                "numerical":
                    numerical,

                "difference":
                    float(difference),

                "highest_category":
                    str(grouped.idxmax()),

                "highest_value":
                    float(grouped.max()),

                "lowest_category":
                    str(grouped.idxmin()),

                "lowest_value":
                    float(grouped.min())
            })

    relationships.sort(
        key=lambda x: x["difference"],
        reverse=True
    )

    return relationships


# -----------------------------------------
# Target EDA Analysis
# -----------------------------------------

def analyze_target(cleaned_df):

    target_keywords = [

        "target",
        "churn",
        "outcome",
        "result",
        "label",
        "status",
        "response",
        "sales",
        "revenue",
        "profit"
    ]

    possible_targets = []

    for column in cleaned_df.columns:

        column_lower = str(
            column
        ).lower()

        for keyword in target_keywords:

            if keyword in column_lower:

                possible_targets.append(
                    column
                )

                break

    target_analysis = {

        "possible_targets":
            possible_targets,

        "target_distributions":
            {}
    }

    # ---------------------------------
    # Target distribution
    # ---------------------------------

    for target in possible_targets:

        distribution = (
            cleaned_df[target]
            .value_counts(
                dropna=False
            )
            .to_dict()
        )

        target_analysis[
            "target_distributions"
        ][target] = distribution

    return target_analysis


# -----------------------------------------
# Automatic EDA Visualization Engine
# -----------------------------------------

def generate_eda_charts(cleaned_df):

    import os
    import matplotlib.pyplot as plt

    charts_folder = "charts"

    os.makedirs(
        charts_folder,
        exist_ok=True
    )

    # Remove old charts from previous dataset
    for file_name in os.listdir(charts_folder):

        file_path = os.path.join(
            charts_folder,
            file_name
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

    print("Old charts cleared.")

    generated_charts = []

    # ---------------------------------
    # Numerical columns
    # ---------------------------------

    numerical_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    # ---------------------------------
    # Categorical columns
    # ---------------------------------

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category", "string", "bool"]
    ).columns.tolist()

    # ---------------------------------
    # 1. Numerical distributions
    # ---------------------------------

    for column in numerical_columns:

        data = cleaned_df[column].dropna()

        if len(data) == 0:
            continue

        # Skip binary numerical variables
        if data.nunique() <= 2:
            continue

        fig, ax = plt.subplots(
            figsize=(6, 4),
            dpi=120
        )

        ax.hist(
            data,
            bins=20
        )

        ax.set_title(
            f"Distribution of {column}",
            fontsize=12
        )

        ax.set_xlabel(
            column,
            fontsize=10
        )

        ax.set_ylabel(
            "Frequency",
            fontsize=10
        )

        fig.tight_layout()

        filename = (
            f"{charts_folder}/"
            f"{column}_distribution.png"
        )

        fig.savefig(
            filename,
            dpi=120,
            bbox_inches="tight"
        )

        plt.close(fig)

        generated_charts.append(filename)

    # ---------------------------------
    # 2. Categorical distributions
    # ---------------------------------

    for column in categorical_columns:

        unique_count = (
            cleaned_df[column]
            .nunique(
                dropna=True
            )
        )

        # Avoid high-cardinality columns
        if unique_count == 0 or unique_count > 15:
            continue

        value_counts = (
            cleaned_df[column]
            .value_counts(
                dropna=False
            )
            .head(15)
        )

        if value_counts.empty:
            continue

        fig, ax = plt.subplots(
            figsize=(6, 4),
            dpi=120
        )

        value_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            f"Distribution of {column}",
            fontsize=12
        )

        ax.set_xlabel(
            column,
            fontsize=10
        )

        ax.set_ylabel(
            "Count",
            fontsize=10
        )

        ax.tick_params(
            axis="x",
            labelrotation=45
        )

        fig.tight_layout()

        filename = (
            f"{charts_folder}/"
            f"{column}_distribution.png"
        )

        fig.savefig(
            filename,
            dpi=120,
            bbox_inches="tight"
        )

        plt.close(fig)

        generated_charts.append(filename)

    # ---------------------------------
    # 3. Correlation heatmap
    # ---------------------------------

    if len(numerical_columns) >= 2:

        correlation = (
            cleaned_df[
                numerical_columns
            ].corr()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5),
            dpi=120
        )

        image = ax.imshow(
            correlation,
            cmap="coolwarm",
            aspect="auto"
        )

        fig.colorbar(
            image,
            ax=ax,
            label="Correlation"
        )

        ax.set_xticks(
            range(len(correlation.columns))
        )

        ax.set_xticklabels(
            correlation.columns,
            rotation=45,
            ha="right"
        )

        ax.set_yticks(
            range(len(correlation.columns))
        )

        ax.set_yticklabels(
            correlation.columns
        )

        ax.set_title(
            "Correlation Heatmap",
            fontsize=12
        )

        fig.tight_layout()

        filename = (
            f"{charts_folder}/"
            "correlation_heatmap.png"
        )

        fig.savefig(
            filename,
            dpi=120,
            bbox_inches="tight"
        )

        plt.close(fig)

        generated_charts.append(filename)

    # ---------------------------------
    # 4. Numerical vs Numerical
    # ---------------------------------

    if len(numerical_columns) >= 2:

        x_column = numerical_columns[0]
        y_column = numerical_columns[1]

        plot_df = cleaned_df[
            [x_column, y_column]
        ].dropna()

        if len(plot_df) > 0:

            fig, ax = plt.subplots(
                figsize=(6, 4),
                dpi=120
            )

            ax.scatter(
                plot_df[x_column],
                plot_df[y_column],
                alpha=0.5
            )

            ax.set_title(
                f"{y_column} vs {x_column}",
                fontsize=12
            )

            ax.set_xlabel(
                x_column,
                fontsize=10
            )

            ax.set_ylabel(
                y_column,
                fontsize=10
            )

            fig.tight_layout()

            filename = (
                f"{charts_folder}/"
                f"{y_column}_vs_{x_column}.png"
            )

            fig.savefig(
                filename,
                dpi=120,
                bbox_inches="tight"
            )

            plt.close(fig)

            generated_charts.append(
                filename
            )

    return generated_charts

# -----------------------------------------
# Dashboard Blueprint PNG Generator
# -----------------------------------------

# -----------------------------------------
# Dashboard Blueprint PNG Generator
# -----------------------------------------

def generate_dashboard_png(
    recommendations,
    output_path="dashboard_blueprint.png"
):

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    # ---------------------------------
    # Extract recommendations
    # ---------------------------------

    kpis = recommendations.get(
        "kpis",
        []
    )

    charts = recommendations.get(
        "charts",
        []
    )

    slicers = recommendations.get(
        "slicers",
        []
    )

    # ---------------------------------
    # Create dashboard canvas
    # ---------------------------------

    fig = plt.figure(
        figsize=(14, 9)
    )

    fig.patch.set_facecolor(
        "#F5F6FA"
    )

    # ---------------------------------
    # Dashboard title
    # ---------------------------------

    fig.text(
        0.05,
        0.95,
        "AI Recommended Dashboard",
        fontsize=22,
        fontweight="bold"
    )

    fig.text(
        0.05,
        0.915,
        "Automatically generated from dataset analysis",
        fontsize=11
    )

    # ---------------------------------
    # KPI CARDS
    # ---------------------------------

    max_kpis = min(
        len(kpis),
        5
    )

    for i in range(max_kpis):

        left = (
            0.05 +
            i * 0.18
        )

        card = Rectangle(
            (
                left,
                0.78
            ),
            0.15,
            0.09,
            facecolor="white",
            edgecolor="#D9DCE3",
            linewidth=1.5
        )

        fig.add_artist(card)

        fig.text(
            left + 0.075,
            0.835,
            str(kpis[i]),
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold"
        )

        fig.text(
            left + 0.075,
            0.80,
            "KPI CARD",
            ha="center",
            va="center",
            fontsize=8
        )

    # ---------------------------------
    # SLICERS
    # ---------------------------------

    fig.text(
        0.05,
        0.73,
        "Recommended Slicers",
        fontsize=12,
        fontweight="bold"
    )

    slicer_text = (
        " | ".join(
            str(x)
            for x in slicers[:8]
        )
        if slicers
        else "No suitable slicers detected"
    )

    fig.text(
        0.05,
        0.70,
        slicer_text,
        fontsize=9
    )

    # ---------------------------------
    # CHARTS
    # ---------------------------------

    max_charts = min(
        len(charts),
        6
    )

    positions = [
        (0.05, 0.43),
        (0.37, 0.43),
        (0.69, 0.43),
        (0.05, 0.12),
        (0.37, 0.12),
        (0.69, 0.12)
    ]

    for i in range(max_charts):

        left, bottom = positions[i]

        chart_box = Rectangle(
            (
                left,
                bottom
            ),
            0.27,
            0.23,
            facecolor="white",
            edgecolor="#D9DCE3",
            linewidth=1.5
        )

        fig.add_artist(
            chart_box
        )

        chart_info = charts[i]

        column = chart_info.get(
            "column",
            "Unknown"
        )

        visual = chart_info.get(
            "visual",
            "Chart"
        )

        purpose = chart_info.get(
            "purpose",
            ""
        )

        fig.text(
            left + 0.135,
            bottom + 0.185,
            str(visual),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold"
        )

        fig.text(
            left + 0.135,
            bottom + 0.135,
            str(column),
            ha="center",
            va="center",
            fontsize=10
        )

        fig.text(
            left + 0.135,
            bottom + 0.075,
            str(purpose),
            ha="center",
            va="center",
            fontsize=7,
            wrap=True
        )

    # ---------------------------------
    # Footer
    # ---------------------------------

    fig.text(
        0.05,
        0.04,
        "Generated automatically by AI Data Analyst",
        fontsize=9
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    return output_path
