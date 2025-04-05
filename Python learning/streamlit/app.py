import streamlit as st

# st.title("My First App")
# st.write("Hello world!")
#  ctrl + c to quit streamlit terminal

st.title("Streamlit Beginner to Pro 🚀")
st.write("Welcome to the ultimate Streamlit walkthrough!")

# Sidebar for navigation
section = st.sidebar.selectbox("Choose a section", [
    "🏁 Basic Intro",
    "🧰 Widgets",
    "📊 Charts",
    "📁 Upload CSV & Explore",
    "⚽ Real Football Example (Coming Soon!)"
])

# Each section builds up from the basics
if section == "🏁 Basic Intro":
    st.header("🏁 Basic Intro")
    st.write("This is the simplest Streamlit app.")
    st.write("No HTML, no CSS, just Python and web magic.")

elif section == "🧰 Widgets":
    st.header("🧰 Interactive Widgets")
    name = st.text_input("What's your name?")
    st.write(f"Hello {name} 👋")

    age = st.slider("Your age", 0, 100, 25)
    st.write(f"You're {age} years old!")

elif section == "📊 Charts":
    st.header("📊 Streamlit Charts")
    import pandas as pd
    import numpy as np
    data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(data)

elif section == "📁 Upload CSV & Explore":
    st.header("📁 Upload and Explore CSV")
    uploaded = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.write(df.head())
        st.bar_chart(df.select_dtypes(include='number'))

elif section == "⚽ Real Football Example (Coming Soon!)":
    st.header("⚽ Football Stats App (Coming Soon)")
    st.write("This will load real football data and let you filter players, teams, etc.")

