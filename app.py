import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import os

# ✅ Page Config ko sabse pehle rakho
st.set_page_config(page_title="Growth Mindset Web App", page_icon="🧠", layout="wide")

st.title("🧠 Growth Mindset Project Web App with Advanced Features 🧠")

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("Enable Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            body, .stApp { background-color: #2E2E2E !important; color: white !important; }
            .stButton>button { background-color: #2D9CDB !important; color: white !important; }
            .stTextInput>div>div>input, .stFileUploader>div>div { background-color: #4F4F4F !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# User Authentication
st.sidebar.title("Authentication")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if username and password:
    st.sidebar.success("✅ Login successful!")
else:
    st.sidebar.warning("⚠️ Enter username and password")

# File Upload
df = None
uploaded_files = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], accept_multiple_files=False)
if uploaded_files:
    file_ext = os.path.splitext(uploaded_files.name)[-1].lower()
    try:
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_files)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_files, engine='openpyxl')
        st.success(f"✅ Successfully loaded {uploaded_files.name}")
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")

# Data Cleaning
df_cleaned = df.copy() if df is not None else None
if df_cleaned is not None:
    st.subheader("Data Cleaning Options:")
    if st.button("Remove Duplicates", key="remove_duplicates"):
        df_cleaned.drop_duplicates(inplace=True)
        st.success("✅ Duplicates Removed")

    # Predictive Model
    if st.checkbox("Run Predictive Model (Linear Regression)"):
        try:
            feature_col, target_col = st.selectbox("Feature Column", df_cleaned.columns), st.selectbox("Target Column", df_cleaned.columns)
            model = LinearRegression()
            model.fit(df_cleaned[[feature_col]], df_cleaned[target_col])
            df_cleaned['Predictions'] = model.predict(df_cleaned[[feature_col]])
            st.write(df_cleaned[['Predictions']])
        except Exception as e:
            st.error("❌ Ensure numerical data in selected columns.")

    # Visualizations
    st.subheader("Visualizations")
    plot_type = st.radio("Select Plot Type", ["Bar Chart", "Scatter Plot", "Pie Chart", "Line Chart"])
    if plot_type and len(df_cleaned.columns) >= 2:
        col_x, col_y = df_cleaned.columns[:2]
        try:
            if plot_type == "Bar Chart":
                st.plotly_chart(px.bar(df_cleaned, x=col_x, y=col_y, title="Bar Chart"))
            elif plot_type == "Scatter Plot":
                st.plotly_chart(px.scatter(df_cleaned, x=col_x, y=col_y, title="Scatter Plot"))
            elif plot_type == "Pie Chart":
                st.plotly_chart(px.pie(df_cleaned, names=col_x, values=col_y, title="Pie Chart"))
            elif plot_type == "Line Chart":
                st.plotly_chart(px.line(df_cleaned, x=col_x, y=col_y, title="Line Chart"))
        except Exception as e:
            st.error("❌ Error generating visualization: Ensure correct data format.")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data Cleaning", "Visualization", "Analysis"])
if page == "Data Cleaning":
    st.write("Perform data cleaning operations here.")
elif page == "Visualization":
    st.write("Create advanced visualizations here.")
elif page == "Analysis":
    st.write("Run predictive models and analysis here.")

st.write("🚀 Thank you for using the Growth Mindset Web App!")
