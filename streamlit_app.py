import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import random
import time

# Connect to the Google Sheet using the connection info in secrets.toml
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read()

st.title("Which taxi colour has a higher average tip?")

# --- Data Processing ---
# If the 'tip' values come with commas as decimal separators, convert them to floats.
if data['tip'].dtype == object:
    data['tip'] = data['tip'].str.replace(',', '.').astype(float)

# --- Define Chart Functions ---

def plot_bar_chart(data):
    """Creates a bar chart comparing the average tip by taxi colour."""
    fig, ax = plt.subplots()
    # We know our colors are "green" and "yellow"; ensure that order.
    ax.bar(data['color'], data['tip'], color=['green', 'yellow'])
    ax.set_xlabel("Taxi Colour")
    ax.set_ylabel("Average Tip")
    ax.set_title("Average Tip by Taxi Colour (Bar Chart)")
    return fig

def plot_pie_chart(data):
    """Creates a pie chart showing the tip distribution by taxi colour."""
    fig, ax = plt.subplots()
    ax.pie(data['tip'], labels=data['color'], autopct='%1.1f%%', colors=['green', 'yellow'])
    ax.set_title("Tip Distribution by Taxi Colour (Pie Chart)")
    return fig

# --- Manage Session State ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'chart_shown' not in st.session_state:
    st.session_state.chart_shown = False
if 'chart_choice' not in st.session_state:
    st.session_state.chart_choice = None

# --- Build the Interactive UI ---

# Button to display a randomly selected chart
if st.button("Show a Chart"):
    st.session_state.start_time = time.time()  # record the time when the chart is shown
    st.session_state.chart_shown = True
    st.session_state.chart_choice = random.choice(['bar', 'pie'])

# If a chart has been shown, display it and the confirmation button.
if st.session_state.chart_shown:
    if st.session_state.chart_choice == 'bar':
        st.write("Displaying Bar Chart")
        fig = plot_bar_chart(data)
    else:
        st.write("Displaying Pie Chart")
        fig = plot_pie_chart(data)
    st.pyplot(fig)
    
    if st.button("I answered your question"):
        end_time = time.time()
        duration = end_time - st.session_state.start_time
        st.write(f"You took {duration:.2f} seconds to answer!")
        # Optionally, reset the session state if you want the process to restart.
        st.session_state.chart_shown = False
        st.session_state.start_time = None
