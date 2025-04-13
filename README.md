from pathlib import Path

# Load the existing README.txt template
readme_path = Path("/mnt/data/README.txt")
existing_readme = readme_path.read_text()

# New HMI section
hmi_section = """
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
"""

# Append the HMI section to the README content
updated_readme = existing_readme.strip() + "\n\n" + hmi_section.strip()

# Save the updated README
updated_readme_path = Path("/mnt/data/README_updated.txt")
updated_readme_path.write_text(updated_readme)

updated_readme_path.name
