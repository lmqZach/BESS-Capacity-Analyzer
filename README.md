# 🔋 BESS Capacity Analyzer

A Streamlit-based diagnostic app for analyzing SCADA data from Battery Energy Storage Systems (BESS), automating performance metrics like RTE and % Guaranteed Energy. Built for engineering-grade accuracy, it enables data parsing, visualization, and deterministic report generation for Samsung E4L, Tesla MegaPack, and Sungrow PowerTitan.

---

## 📌 Overview

**Author:** Zach (Muqing) Li  
**Title:** Performance Engineer  
**Division:** Engineering Solutions & Standard, EPC, The AES Corporation

This tool processes and analyzes SCADA trending data from commissioned BESS sites. It enables:
- File upload of raw capacity test data
- Parsing and preprocessing of SCADA time-series
- Filtering invalid readings and filling missing data using forward fill strategy
- Interactive visualization of key metrics (Energy, Power, SOC, Temperature)
- Automatic performance analysis with deterministic metric calculations (RTE, % Guaranteed Energy, etc.)
- Summary report generation per power block and full plant view
- Exportable Excel reports for warranty review and performance documentation

---

## 📊 Methodology

1. **Raw Data Structure**  
   Raw Excel file with multi-indexed BMS channel readings like `BMS.1.A.2.1.N1 Charge Amount of Energy (kWh)`

2. **Parsing and Grouping**  
   Automatically identifies AMPS and Power Blocks from column patterns

3. **Data Processing**  
   Forward fills missing data, selects only relevant columns (kWh, SOC, Temp, etc.)

4. **Summary Metric Calculation**  
   Calculates energy charged, discharged, % of guaranteed energy delivered, RTE, and PASS/FAIL logic

5. **Visualization and Export**  
   Streamlit HMI interface visualizes trends and enables Excel report download

---

## 🚀 Usage Instructions

1. Clone or download the repository  
2. Install dependencies with:
   ```
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```
   streamlit run app.py
   ```

---

## 📦 Requirements

- Python 3.8+
- `streamlit`
- `pandas`
- `openpyxl`
- `plotly`
- `xlsxwriter`

---

## 🖥️ HMI Interface Walkthrough

This section introduces the **Streamlit-based Human-Machine Interface (HMI)** of the BESS Capacity Analyzer. The app has a clean, professional layout and walks users through four stages:

---

### 📁 Stage 1: File Input & Project Setup

**Image:** `HMI/main_interface.png`

At the start of the application, users are presented with a configuration interface to specify:
- Project Name
- Battery Type (Samsung E4L Category, Tesla MegaPack, etc.)
- Measurement Source (BMS point, PCS DC Feed, PCS AC Busbar)
- SCADA Data Type (Bluence SCADA – Isotrol, or Vantage SCADA – Trimark)

After inputting project details, users upload a raw Excel file containing SCADA trend data.

---

### 🧠 Stage 2: Equipment Auto Detection

**Image:** `HMI/equipment_detection.png`

Upon file upload, the application parses the Excel sheet and detects:
- All AMPS IDs present in the dataset
- Number of data columns per AMPS
- Number of power blocks per AMPS enclosure

The interface displays a summary table and dropdowns to let users select a specific AMPS ID and Power Block for analysis.

---

### 📊 Stage 3: Interactive Visualization

**Image:** `HMI/integent visualization.png`

This is the core analytical dashboard. It features an **interactive, dual-axis Plotly graph** that:
- Shows **Energy (kWh)** on the left y-axis
- Shows **State of Charge (%)** and **Temperature (°C)** on the right y-axis
- Includes interactive features like zoom, pan, export, and data toggling

Available data curves include:
- Accumulated Charge Energy
- Accumulated Discharge Energy
- Cell Temperature (Average, Maximum, Max Difference)
- SOC Minimum and Service Values

Users can explore dynamic battery behavior over time and correlate SOC drop with energy flow and thermal conditions.

---

### 📥 Stage 4: Output Summary & Downloads

**Image:** `HMI/output_options.png`

Once visualization is complete, users can:
- Generate a **per-PCS summary table**
- Click a button to analyze the **entire BESS dataset**, power block by power block
- View metrics including:
  - Energy Charged / Discharged (MWh)
  - % of Guaranteed Energy Delivered
  - Round Trip Efficiency (RTE)
  - Pass/Fail status
- Export this data into a formatted Excel file for further review, documentation, or reporting
