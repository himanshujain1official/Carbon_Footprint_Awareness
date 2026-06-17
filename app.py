import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Load environment variables if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from assets import get_custom_css, get_threejs_html
from ai_agent import process_user_input
from calculations import get_daily_baseline

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Carbon 0 - Daily Carbon Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECT CSS ---
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- INJECT THREE.JS TEXT PARTICLES ---
components.html(get_threejs_html(), height=200, scrolling=False)

# --- INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "daily_emissions" not in st.session_state:
    st.session_state.daily_emissions = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "total_kg": 0.0,
        "activities": []
    }

# --- CACHED FUNCTIONS ---
@st.cache_data
def get_baseline():
    return get_daily_baseline()

@st.cache_data
def generate_bar_chart(total_emission: float, baseline: float):
    """Bar chart comparing current emission vs baseline."""
    data = pd.DataFrame({
        "Category": ["Current", "Baseline"],
        "Emissions (kg)": [total_emission, baseline]
    })
    
    fig = px.bar(
        data, 
        x="Category", 
        y="Emissions (kg)", 
        color="Category",
        color_discrete_map={
            "Current": "#EA4335" if total_emission > baseline else "#4285F4", # Google Red if over, Google Blue if under
            "Baseline": "#34A853" # Google Green
        },
        text_auto='.2f'
    )
    
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#202124",
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=300
    )
    return fig

def generate_pie_chart(activities: list):
    """Generates an attractive Donut (Pie) chart breaking down emissions."""
    if not activities:
        # Empty donut
        fig = go.Figure(go.Pie(labels=["No Data"], values=[1], hole=0.6, marker_colors=["#DADCE0"]))
        fig.update_layout(showlegend=False, paper_bgcolor="#FFFFFF", height=300, margin=dict(t=20, b=20, l=20, r=20))
        return fig

    # Aggregate by category
    df = pd.DataFrame(activities)
    agg_df = df.groupby("category")["emission_kg"].sum().reset_index()
    
    # Map to Google colors
    color_map = {
        "transport": "#4285F4", # Blue
        "electricity": "#FBBC05", # Yellow
        "diet": "#EA4335", # Red (if added later)
        "other": "#34A853" # Green
    }
    
    fig = px.pie(
        agg_df, 
        values='emission_kg', 
        names='category', 
        hole=0.5, # Makes it a donut chart
        color='category',
        color_discrete_map=color_map
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        font_color="#202124",
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=300
    )
    return fig

# --- SIDEBAR NAVIGATION & TIPS ---
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    st.markdown("Welcome to **Carbon 0**. Track and optimize your daily carbon emissions.")
    
    st.markdown("---")
    st.markdown("### 💡 Tips for Low Carbon")
    st.info("**Transport 🚌**\n\nOpt for public transit, carpool, or cycle. Switching to an EV can save ~70% emissions per km. \n\n✓ Use buses, trains, carpooling, or a bicycle when possible. \n\n✓ Electric vehicles EVs create much less pollution than petrol or diesel vehicles. \n\n✓ Walking or cycling for short trips can reduce your carbon footprint to zero.")
    st.warning("**Electricity ⚡**\n\nTurn off the AC when leaving the room. A 1°C increase in thermostat saves 6% electricity. \n\n✓ Set your AC to 24-26°C in summer and 18-20°C in winter. \n\n✓ Use energy-efficient appliances and LED bulbs. \n\n✓ Setting the AC temperature 1°C higher can reduce electricity use by about 6%.")
    st.success("**Diet 🥗**\n\nReducing red meat consumption can dramatically lower your personal carbon footprint. \n\n✓ Consider plant-based meals or reducing red meat intake. \n\n✓ Eating more plant-based foods can significantly reduce your carbon footprint. \n\n✓ Even small changes, like having one meatless day per week, can make a difference.")
    st.info("**General 🌱**\n\nSmall lifestyle changes can add up to big carbon savings. \n\n✓ Unplug devices when not in use to avoid 'phantom' energy drain. \n\n✓ Reduce, reuse, recycle to minimize waste. \n\n✓ Supporting renewable energy and sustainable products can drive larger systemic change.")
    
    st.markdown("---")
    if st.button("RESET DATA", help="Reset all carbon footprint data and chat history to start over"):
        st.session_state.daily_emissions = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "total_kg": 0.0,
            "activities": []
        }
        st.session_state.chat_history = []
        st.rerun()

# --- MAIN UI ---
# Security Warning Check
if not os.environ.get("GEMINI_API_KEY"):
    if not st.secrets.get("GEMINI_API_KEY", None):
        st.error("⚠️ GEMINI_API_KEY not found. Please add it securely to enable the AI Agent.")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("## 📊 Analytics Dashboard")
    baseline = get_baseline()
    current_emission = st.session_state.daily_emissions["total_kg"]
    
    # Render Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Today's Footprint", f"{current_emission:.2f} kg", delta=f"{current_emission - baseline:.2f} kg vs baseline", delta_color="inverse", help="Total carbon emissions logged today")
    m2.metric("Daily Baseline", f"{baseline:.2f} kg", help="Standard average daily footprint for comparison")
    status = "Optimal" if current_emission <= baseline else "Critical"
    m3.metric("System Status", status, help="Status indicating if you are below or above the baseline")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Charts side by side
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("### Emission vs Baseline")
        st.caption("Visual representation of your current carbon emissions compared to the baseline.")
        st.plotly_chart(generate_bar_chart(current_emission, baseline), use_container_width=True)
    with chart_col2:
        st.markdown("### Emission by Category")
        st.caption("Donut chart breaking down your carbon emissions by category.")
        st.plotly_chart(generate_pie_chart(st.session_state.daily_emissions["activities"]), use_container_width=True)
    
    # Render Activities Log
    if st.session_state.daily_emissions["activities"]:
        st.markdown("### Recent Activity Logs")
        df_activities = pd.DataFrame(st.session_state.daily_emissions["activities"])
        st.dataframe(df_activities, use_container_width=True, hide_index=True)

with col2:
    st.markdown("## 🤖 Smart Assistant")
    st.caption("Log activities naturally. E.g., 'I drove 20km in a petrol car and used AC for 3 hours.' or 'I cooked with electricity for 1 hour.'")
    
    # Chat Interface Container
    chat_container = st.container(height=550)
    
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # Chat Input
    # Note: st.chat_input does not support the 'help' parameter. 
    # For accessibility, the descriptive caption above serves as context.
    user_input = st.chat_input("Enter your activity here...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
                
        with st.spinner("Analyzing..."):
            agent_response = process_user_input(user_input)
            
            if agent_response.get("success"):
                added_emissions = agent_response["total_emission_kg"]
                advice = agent_response["advice"]
                
                st.session_state.daily_emissions["total_kg"] += added_emissions
                st.session_state.daily_emissions["activities"].extend(agent_response["activities"])
                
                # Clear chart caches
                generate_bar_chart.clear()
                
                reply = f"**Logged:** {added_emissions:.2f} kg CO2e.\n\n**Advice:** {advice}"
            else:
                reply = f"**Error:** {agent_response.get('error')}"
                
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(reply)
                
        st.rerun()
