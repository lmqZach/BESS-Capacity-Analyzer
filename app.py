import streamlit as st
import pandas as pd
import re
import plotly.graph_objects as go
from io import BytesIO

GUARANTEED_ENERGY_KWH = 5499.78

def load_and_parse_amps(file):
    df = pd.read_excel(file, header=[0, 1])
    df.columns = [' '.join(col).strip() for col in df.columns]

    amps_dict = {}
    for col in df.columns:
        match = re.search(r'BMS\.(\d+\.[A-Z]\.\d+)', col)
        if match:
            amps_key = match.group(1)
            if amps_key not in amps_dict:
                amps_dict[amps_key] = []
            amps_dict[amps_key].append(col)

    amps_info = []
    for amps, cols in amps_dict.items():
        pb_set = set()
        for col in cols:
            match = re.search(r'BMS\.(\d+\.[A-Z]\.\d+)\.(\d+)', col)
            if match:
                pb_set.add(match.group(2))
        amps_info.append({
            "AMPS ID": amps,
            "Number of Columns": len(cols),
            "Number of Power Blocks": len(pb_set)
        })

    return df, pd.DataFrame(amps_info), amps_dict

def filter_columns_by_keywords(columns, pattern, keywords):
    return [col for col in columns if pattern in col and any(k in col.lower() for k in keywords)]

def forward_fill_columns(df, columns, time_col):
    if not columns:
        return None
    tab = df[[time_col] + columns].copy()
    tab.iloc[:, 1:] = tab.iloc[:, 1:].ffill()
    return tab

def calculate_summary(df, time_col, pattern, pb_number):
    pb_prefix = f"{pattern}.{pb_number}"
    soc_col = next((col for col in df.columns if pb_prefix in col and "soc" in col.lower()), None)
    charge_col = next((col for col in df.columns if pb_prefix in col and "charge amount of energy" in col.lower()), None)
    discharge_col = next((col for col in df.columns if pb_prefix in col and "discharge amount of energy" in col.lower()), None)

    if soc_col is None or charge_col is None or discharge_col is None:
        return None

    df_calc = df[[time_col, soc_col, charge_col, discharge_col]].copy()
    df_calc.iloc[:, 1:] = df_calc.iloc[:, 1:].ffill()
    df_calc[time_col] = pd.to_datetime(df_calc[time_col], errors='coerce')

    soc_series = df_calc[soc_col].dropna()
    if soc_series.empty:
        return None

    t1_index = soc_series.idxmax()
    t0_index = soc_series.loc[:t1_index][soc_series.loc[:t1_index] == soc_series.loc[:t1_index].min()].index[0]
    t2_index = soc_series.loc[t1_index:][soc_series.loc[t1_index:] == soc_series.loc[t1_index:].min()].index[0]

    energy_charged = df_calc[charge_col][t1_index] - df_calc[charge_col][t0_index]
    energy_discharged = df_calc[discharge_col][t2_index] - df_calc[discharge_col][t1_index]
    percent_guaranteed_energy = energy_discharged / GUARANTEED_ENERGY_KWH if energy_discharged else 0
    rte = energy_discharged / energy_charged if energy_charged else 0
    pass_res = "PASS" if percent_guaranteed_energy > 1 else "FAIL"

    return {
        "AMPS ID": pattern.split('.')[-2] + '.' + pattern.split('.')[-1],
        "Power Block": pb_number,
        "Energy Charged (MWh)": round(energy_charged, 2),
        "Energy Discharged (MWh)": round(energy_discharged, 2),
        "Percent of Guaranteed Energy": f"{percent_guaranteed_energy * 100:.2f}%",
        "RTE": f"{rte * 100:.2f}%",
        "Final Result": pass_res
    }

def plot_combined_dual_axis(time_col, kwh_df, soc_df, temp_df):
    fig = go.Figure()

    if kwh_df is not None:
        for col in kwh_df.columns[1:]:
            fig.add_trace(go.Scatter(x=kwh_df[time_col], y=kwh_df[col], name=f"{col}", yaxis="y1"))

    if soc_df is not None:
        for col in soc_df.columns[1:]:
            fig.add_trace(go.Scatter(x=soc_df[time_col], y=soc_df[col], name=f"{col}", yaxis="y2", line=dict(dash="dot", color="green")))

    if temp_df is not None:
        for col in temp_df.columns[1:]:
            fig.add_trace(go.Scatter(x=temp_df[time_col], y=temp_df[col], name=f"{col}", yaxis="y2", line=dict(dash="dash", color="red")))

    fig.update_layout(
        title="Combined Visualization: Energy (kWh), SOC (%), Temperature (°C)",
        xaxis=dict(title="Timestamp"),
        yaxis=dict(title="Energy (kWh)", side="left"),
        yaxis2=dict(title="SOC / Temperature", overlaying="y", side="right"),
        legend=dict(orientation="h", x=0, y=1.15),
        height=600,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="BESS Capacity Analyzer", layout="wide")
    st.title("Samsung EKS – BESS Capacity Analyzer")

    st.markdown("**Author:** Zach (Muqing) Li  \n"
                "**Title:** Performance Engineer  \n"
                "**Division:** Engineering Solutions & Standard, EPC, The AES Corporation")

    project_name = st.text_input("Project Name")
    bess_type = st.selectbox("BESS Type", ["Samsung E4L Category", "Tesla MegaPack", "Sungrow PowerTitan"])
    delivery_point = st.selectbox("Delivery / Measurement Point", ["BMS point", "PCS DC Feed", "PCS AC Busbar"])
    scada_type = st.selectbox("SCADA Data Type", ["Bluence SCADA - Isotrol", "Vantage SCADA - Trimark"])

    st.markdown("**App Purpose:**")
    st.info("This app analyzes capacity test data of a BESS power plant, cleans and visualizes SCADA trends, and generates performance reports using deterministic statistical methods.")

    uploaded_file = st.file_uploader("📁 Upload Raw SCADA Excel File", type=["xlsx"])
    if uploaded_file:
        df, df_summary, amps_dict = load_and_parse_amps(uploaded_file)
        st.success("✅ File loaded successfully!")
        st.dataframe(df_summary)

        amps_ids = list(amps_dict.keys())
        selected_amps = st.selectbox("Select AMPS ID for Plotting", amps_ids)

        pb_set = sorted(set(
            match.group(2)
            for col in amps_dict[selected_amps]
            if (match := re.search(r'BMS\.(\d+\.[A-Z]\.\d+)\.(\d+)', col))
        ))

        selected_pb = st.selectbox("Select Power Block", pb_set)
        pattern = f"BMS.{selected_amps}"
        pb_pattern = f"{pattern}.{selected_pb}"
        time_col = df.columns[0]

        kwh_df = forward_fill_columns(df, filter_columns_by_keywords(df.columns, pb_pattern, ["kwh"]), time_col)
        soc_df = forward_fill_columns(df, filter_columns_by_keywords(df.columns, pb_pattern, ["soc"]), time_col)
        temp_df = forward_fill_columns(df, filter_columns_by_keywords(df.columns, pb_pattern, ["temp", "temperature"]), time_col)

        st.markdown("### 📊 Combined Visualization")
        plot_combined_dual_axis(time_col, kwh_df, soc_df, temp_df)

        if st.button("🔍 Show Summary for This PCS"):
            summary = [calculate_summary(df, time_col, pattern, pb) for pb in ['1', '2', '3']]
            summary = [s for s in summary if s]
            summary_df = pd.DataFrame(summary)
            st.subheader("Summary Results for Selected PCS")
            st.dataframe(summary_df)

            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                summary_df.to_excel(writer, sheet_name="PCS Summary", index=False)
            buffer.seek(0)
            st.download_button("📥 Download PCS Summary Excel", buffer, file_name=f"{selected_amps}_summary.xlsx")

        if st.button("📊 Show Summary for All AMPS + Power Blocks"):
            full_summary = []
            for amps_id in amps_dict:
                pattern_all = f"BMS.{amps_id}"
                for pb in ['1', '2', '3']:
                    result = calculate_summary(df, time_col, pattern_all, pb)
                    if result:
                        full_summary.append(result)
            if full_summary:
                full_df = pd.DataFrame(full_summary)
                st.subheader("🌐 Full Plant Summary")
                st.dataframe(full_df)

                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    full_df.to_excel(writer, sheet_name="Full Summary", index=False)
                buffer.seek(0)
                st.download_button("📥 Download Full Summary Excel", buffer, file_name="Full_BESS_Summary.xlsx")

if __name__ == "__main__":
    main()
