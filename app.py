import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(page_title="Book Price Analytics", layout="wide")

sns.set_style("whitegrid")


# ---------------------------------------------------
# Load Data and Model
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("books_cleaned_data.csv")


@st.cache_resource
def load_model():
    return joblib.load("book_price_model.pkl")


df = load_data()
model = load_model()


# ---------------------------------------------------
# Title and Introduction
# ---------------------------------------------------
st.title("Book Price Analytics Dashboard")

st.write(
    """
This dashboard provides a complete view of competitor book pricing behavior.
It also includes a Machine Learning model that predicts the estimated book price based on:
- Star Rating
- Stock Availability
"""
)

st.markdown("---")


# ---------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------
st.sidebar.header("Dashboard Controls")

# ML Prediction Tool
st.sidebar.subheader("AI Price Predictor")
st.sidebar.write("Enter book rating and stock to predict expected price.")

rating_input = st.sidebar.selectbox("Book Rating", [1, 2, 3, 4, 5], index=2)
stock_input = st.sidebar.number_input("Stock Available", min_value=0, max_value=500, value=10)

if st.sidebar.button("Predict Price"):
    input_data = pd.DataFrame([[rating_input, stock_input]], columns=["Rating", "Stock"])
    predicted_price = model.predict(input_data)[0]
    st.sidebar.success(f"Estimated Price: £{predicted_price:.2f}")

st.sidebar.markdown("---")

# Filters
st.sidebar.subheader("Data Filters")

selected_ratings = st.sidebar.multiselect(
    "Select Ratings",
    options=[1, 2, 3, 4, 5],
    default=[1, 2, 3, 4, 5]
)

st.sidebar.write("Price Filter (£)")
min_limit = int(df["Price"].min())
max_limit = int(df["Price"].max())

col_min, col_max = st.sidebar.columns(2)

with col_min:
    min_price = st.number_input(
        "Min Price",
        min_value=min_limit,
        max_value=max_limit,
        value=min_limit
    )

with col_max:
    max_price = st.number_input(
        "Max Price",
        min_value=min_limit,
        max_value=max_limit,
        value=max_limit
    )


# ---------------------------------------------------
# Apply Filters
# ---------------------------------------------------
filtered_df = df[
    (df["Rating"].isin(selected_ratings)) &
    (df["Price"] >= min_price) &
    (df["Price"] <= max_price)
]

# If no data after filtering
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust the filters.")
    st.stop()


# ---------------------------------------------------
# KPI Metrics Section
# ---------------------------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Books", len(filtered_df))
col2.metric("Average Price", f"£{filtered_df['Price'].mean():.2f}")
col3.metric("Total Stock", int(filtered_df["Stock"].sum()))
col4.metric("Average Rating", f"{filtered_df['Rating'].mean():.1f} / 5")

st.markdown("---")


# ---------------------------------------------------
# Market Insights Section
# ---------------------------------------------------
st.subheader("Quick Market Insights")

highest_price = filtered_df["Price"].max()
lowest_price = filtered_df["Price"].min()
most_common_rating = filtered_df["Rating"].mode()[0]
avg_stock = filtered_df["Stock"].mean()

st.write(f"- Highest price in selection: **£{highest_price:.2f}**")
st.write(f"- Lowest price in selection: **£{lowest_price:.2f}**")
st.write(f"- Most common rating: **{most_common_rating} stars**")
st.write(f"- Average stock availability: **{avg_stock:.1f} units**")

st.markdown("---")


# ---------------------------------------------------
# Charts Section
# ---------------------------------------------------
st.subheader("Market Analysis Charts")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Price Distribution", "Rating Count", "Price vs Rating", "Stock vs Price"]
)

with tab1:
    st.write("### Distribution of Book Prices")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df["Price"], bins=20, kde=True, ax=ax)
    ax.set_xlabel("Price (£)")
    ax.set_ylabel("Number of Books")
    st.pyplot(fig)

with tab2:
    st.write("### Count of Books by Rating")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.countplot(x="Rating", data=filtered_df, ax=ax, palette="viridis")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)

with tab3:
    st.write("### Price Spread by Star Rating")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(x="Rating", y="Price", data=filtered_df, ax=ax, palette="coolwarm")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Price (£)")
    st.pyplot(fig)

with tab4:
    st.write("### Stock vs Price Relationship")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.scatterplot(
        x="Stock",
        y="Price",
        hue="Rating",
        data=filtered_df,
        ax=ax,
        palette="deep",
        alpha=0.7
    )
    ax.set_xlabel("Stock Available")
    ax.set_ylabel("Price (£)")
    ax.set_title("Price vs Stock (Colored by Rating)")
    st.pyplot(fig)

st.markdown("---")


# ---------------------------------------------------
# Feature Importance Section (Professional Touch)
# ---------------------------------------------------
st.subheader("Model Explanation (Feature Importance)")

if hasattr(model, "feature_importances_"):
    importance_df = pd.DataFrame({
        "Feature": ["Rating", "Stock"],
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x="Importance", y="Feature", data=importance_df, ax=ax, palette="Blues_r")
    ax.set_title("Random Forest Feature Importance")
    st.pyplot(fig)

    st.write("This chart shows which feature contributes more to predicting the book price.")
else:
    st.info("Feature importance is only available for tree-based models like Random Forest.")

st.markdown("---")


# ---------------------------------------------------
# Top 10 Expensive Books Section
# ---------------------------------------------------
st.subheader("Top 10 Most Expensive Books (Filtered Data)")

top_10_books = filtered_df.sort_values(by="Price", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x="Price", y="Title", data=top_10_books, ax=ax, palette="magma")
ax.set_title("Highest Priced Books in Selected Data")
ax.set_xlabel("Price (£)")
ax.set_ylabel("Book Title")
st.pyplot(fig)

st.markdown("---")


# ---------------------------------------------------
# Dataset Preview + Download
# ---------------------------------------------------
st.subheader("Filtered Dataset Preview")

left_col, right_col = st.columns([3, 1])

with left_col:
    st.dataframe(filtered_df.head(100), use_container_width=True)

with right_col:
    st.write("Download filtered dataset:")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="filtered_books_data.csv",
        mime="text/csv"
    )


# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed By :  Preetham Sharvin Danthi")
