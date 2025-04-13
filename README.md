# 🔋 BESS Capacity Analyzer

A Streamlit-based diagnostic app for analyzing SCADA data from Battery Energy Storage Systems (BESS), automating performance metrics like RTE and % Guaranteed Energy. Built for engineering-grade accuracy, it enables data parsing, visualization, and deterministic report generation for Samsung E4L, Tesla MegaPack, and Sungrow PowerTitan.

---

## 📌 Overview

**Author:** Zach (Muqing) Li  

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

![main_interface](https://github.com/user-attachments/assets/ba3860e4-32b1-4884-81d8-256321459bba)


At the start of the application, users are presented with a configuration interface to specify:
- Project Name
- Battery Type (Samsung E4L Category, Tesla MegaPack, etc.)
- Measurement Source (BMS point, PCS DC Feed, PCS AC Busbar)
- SCADA Data Type (Bluence SCADA – Isotrol, or Vantage SCADA – Trimark)

After inputting project details, users upload a raw Excel file containing SCADA trend data.

---

### 🧠 Stage 2: Equipment Auto Detection

![equipment_detection](https://github.com/user-attachments/assets/eb976329-8da8-4a88-ba05-0df7cc34b428)


Upon file upload, the application parses the Excel sheet and detects:
- All AMPS IDs present in the dataset
- Number of data columns per AMPS
- Number of power blocks per AMPS enclosure

The interface displays a summary table and dropdowns to let users select a specific AMPS ID and Power Block for analysis.

---

### 📊 Stage 3: Interactive Visualization

![integent visualization](https://github.com/user-attachments/assets/9964f269-680e-43c4-a3c0-ec1848c6aa8f)


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

![output_options](https://github.com/user-attachments/assets/f13fcf70-efad-499b-88d2-1d6bb39a5560)


Once visualization is complete, users can:
- Generate a **per-PCS summary table**
- Click a button to analyze the **entire BESS dataset**, power block by power block
- View metrics including:
  - Energy Charged / Discharged (MWh)
  - % of Guaranteed Energy Delivered
  - Round Trip Efficiency (RTE)
  - Pass/Fail status
- Export this data into a formatted Excel file for further review, documentation, or reporting
