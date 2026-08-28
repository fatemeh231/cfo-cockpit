import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

# -------------------------------------------------------------------
# Page Config
# -------------------------------------------------------------------
st.set_page_config(
    page_title="CFO Cockpit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------
def load_data():
    project_root = Path(__file__).parent.parent
    data_path = project_root / 'data' / 'processed' / 'all_companies_revenue.csv'
    
    if not data_path.exists():
        st.error(f"❌ File not found: {data_path}")
        st.stop()
    
    df = pd.read_csv(data_path)
    
    # --- CLEANING ---
    df['ds'] = pd.to_datetime(df['ds'])
    df = df[df['y'] < 500]
    df = df[df['y'] > 0]
    df = df.sort_values('ds').drop_duplicates(subset=['ticker', 'ds'], keep='last')
    df = df.reset_index(drop=True)
    
    return df

# -------------------------------------------------------------------
# Prophet Forecasting
# -------------------------------------------------------------------
def run_prophet(df_company, forecast_periods=12):
    # --- AGGRESSIVE CLEANING FOR PROPHET ---
    df_prophet = df_company[['ds', 'y']].copy()
    df_prophet = df_prophet.sort_values('ds')
    df_prophet = df_prophet.drop_duplicates(subset=['ds'], keep='last')
    df_prophet = df_prophet.reset_index(drop=True)
    
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=forecast_periods, freq='Q')
    forecast = model.predict(future)
    
    forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
    forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)
    forecast['yhat'] = forecast['yhat'].clip(lower=0)
    
    return model, forecast

# -------------------------------------------------------------------
# Main UI
# -------------------------------------------------------------------
def main():
    st.title("📊 CFO Cockpit — Financial Planning & Forecasting")
    st.markdown("### Interactive revenue forecasting for major US companies")
    
    df_all = load_data()
    
    if df_all.empty:
        st.warning("No data loaded. Please check the data file.")
        return
    
    with st.sidebar:
        st.header("⚙️ Controls")
        companies = sorted(df_all['ticker'].unique())
        selected_ticker = st.selectbox("Select Company", companies)
        forecast_quarters = st.slider("Forecast Horizon (Quarters)", 4, 20, 12)
        st.subheader("📈 Scenario Analysis")
        growth_rate = st.slider("Revenue Growth Rate (%)", -20, 40, 10) / 100
        marketing_spend = st.slider("Marketing Spend ($M)", 0, 1000, 500)
        st.markdown("---")
        st.caption(f"Data source: SEC EDGAR | {len(df_all)} total records")
    
    df_company = df_all[df_all['ticker'] == selected_ticker].copy()
    df_company = df_company.sort_values('ds').reset_index(drop=True)
    
    if df_company.empty:
        st.warning(f"No data found for {selected_ticker}")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    latest_revenue = df_company['y'].iloc[-1]
    avg_revenue = df_company['y'].mean()
    min_revenue = df_company['y'].min()
    max_revenue = df_company['y'].max()
    
    with col1:
        st.metric("Latest Revenue", f"${latest_revenue:.2f}B")
    with col2:
        st.metric("Avg Revenue", f"${avg_revenue:.2f}B")
    with col3:
        st.metric("Min Revenue", f"${min_revenue:.2f}B")
    with col4:
        st.metric("Max Revenue", f"${max_revenue:.2f}B")
    
    st.subheader(f"📈 {selected_ticker} — Historical Revenue")
    fig_hist = px.line(df_company, x='ds', y='y', title=f"{selected_ticker} Quarterly Revenue (in Billions USD)", labels={'ds': 'Date', 'y': 'Revenue ($B)'}, markers=True)
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.subheader(f"🔮 {selected_ticker} — Revenue Forecast")
    with st.spinner("Training Prophet model..."):
        model, forecast = run_prophet(df_company, forecast_periods=forecast_quarters)
    
    fig_forecast = model.plot(forecast)
    st.pyplot(fig_forecast)
    
    st.subheader("📋 Forecast Data")
    forecast_table = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_quarters)
    forecast_table['yhat'] = forecast_table['yhat'].round(2)
    forecast_table['yhat_lower'] = forecast_table['yhat_lower'].round(2)
    forecast_table['yhat_upper'] = forecast_table['yhat_upper'].round(2)
    forecast_table.columns = ['Date', 'Forecast ($B)', 'Lower Bound', 'Upper Bound']
    st.dataframe(forecast_table, use_container_width=True)
    
    st.subheader("🧠 Scenario Analysis (What-If)")
    last_value = df_company['y'].iloc[-1]
    scenario_value = last_value * (1 + growth_rate)
    scenario_impact = scenario_value - last_value
    if scenario_value < 0:
        scenario_value = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Adjusted Revenue (Next Quarter)", f"${scenario_value:.2f}B", delta=f"{scenario_impact:+.2f}B")
    with col2:
        st.metric("Marketing Spend Impact", f"${marketing_spend}M", delta="Scenario input")
    
    st.caption(f"Growth rate: {growth_rate*100:.0f}% | Marketing spend: ${marketing_spend}M")
    
    st.markdown("---")
    st.caption(f"Built with ❤️ using Streamlit, Prophet, and SEC EDGAR data")

if __name__ == "__main__":
    main()
