# HealthTech Digital Twin Demo: Real-time Patient Monitoring Simulation
# ---------------------------------------------------------------
# This Python + Streamlit demo simulates a patient's biosignals (heart rate, SpO2, stress level)
# and visualizes them live as a 'Digital Twin' dashboard.
# You can run this on your laptop or online (e.g., Streamlit Cloud, Replit, or Colab with ngrok).

import streamlit as st
import time
import random
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="HealthTech Digital Twin", layout="wide")
st.title("🧬 HealthTech Digital Twin: Real-time Patient Simulation")

# Sidebar controls
st.sidebar.header("Simulation Controls")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
update_interval = st.sidebar.slider("Update interval (seconds)", 0.5, 5.0, 1.0)

# Initialize simulated data store
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["timestamp", "heart_rate", "spo2", "stress"])

# Simulate live data feed
def simulate_data():
    new_row = {
        "timestamp": time.time(),
        "heart_rate": random.randint(60, 110),
        "spo2": random.uniform(95, 100),
        "stress": random.uniform(0.1, 1.0)
    }
    return new_row

# Real-time visualization
placeholder = st.empty()

while True:
    new_row = simulate_data()
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])], ignore_index=True
    ).tail(60)  # keep last 60 seconds

    df = st.session_state.data

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        # Heart rate gauge
        with col1:
            fig1 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=df["heart_rate"].iloc[-1],
                title={'text': "Heart Rate (bpm)"},
                gauge={'axis': {'range': [50, 150]}, 'bar': {'color': "red"}}
            ))
            st.plotly_chart(fig1, use_container_width=True)

        # SpO2 gauge
        with col2:
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=df["spo2"].iloc[-1],
                title={'text': "SpO₂ (%)"},
                gauge={'axis': {'range': [90, 100]}, 'bar': {'color': "blue"}}
            ))
            st.plotly_chart(fig2, use_container_width=True)

        # Stress level gauge
        with col3:
            stress_value = df["stress"].iloc[-1]
            stress_color = "green" if stress_value < 0.4 else "orange" if stress_value < 0.7 else "red"
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stress_value,
                title={'text': "Stress Index"},
                gauge={'axis': {'range': [0, 1]}, 'bar': {'color': stress_color}}
            ))
            st.plotly_chart(fig3, use_container_width=True)

        # Real-time trend chart
        st.markdown(f"### Live Signal Trends for {patient_name}")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=df['timestamp'], y=df['heart_rate'], mode='lines', name='Heart Rate'))
        fig_line.add_trace(go.Scatter(x=df['timestamp'], y=df['spo2'], mode='lines', name='SpO2'))
        fig_line.add_trace(go.Scatter(x=df['timestamp'], y=df['stress'], mode='lines', name='Stress'))
        fig_line.update_layout(xaxis_title='Time', yaxis_title='Value', height=400)
        st.plotly_chart(fig_line, use_container_width=True)

    time.sleep(update_interval)
