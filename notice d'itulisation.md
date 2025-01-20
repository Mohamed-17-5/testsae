**User Guide for Python Program and Excel File**

---

### **Overview**
This document provides a step-by-step guide on how to use the Python program and the accompanying Excel file. The program is designed to process network activity data, extract relevant information, and generate reports. The Excel file stores processed data and allows for further analysis.

### **Requirements**
To run the Python program and work with the Excel file, ensure you have the following:

- **Python**: Version 3.8 or higher.
- **Required Python Libraries**:
  - `pandas`
  - `matplotlib`
  - `tabulate`
  - `openpyxl`

  Install missing libraries using:
  ```bash
  pip install pandas matplotlib tabulate openpyxl
  ```

- **Excel Software**: Any application compatible with `.xlsx` files (e.g., Microsoft Excel, LibreOffice, or Google Sheets).

---

### **File Structure**
1. **Python Program**: `extraction.py`
   - This script processes network activity data from a CSV file.
   - Generates visualizations and markdown reports.

2. **Input File**: `network_data.csv`
   - Contains raw network activity data to be processed by the program.

3. **Output Files**:
   - `extracted_data.xlsx`: Processed data saved in an Excel format.
   - `report.md`: A markdown report summarizing the analysis.

---

### **How to Use the Program**

#### Step 1: Prepare Input File
- Ensure the `network_data.csv` file is located in the same directory as `extraction.py`.
- The input file should follow this structure:
  ```
  DATE,SOURCE,PORT,DESTINATION,FLAG,SEQ,ACK,WIN,OPTIONS,LENGTH
  11:42:04.766656,BP-Linux8.ssh,ssh,192.168.190.130.50019,P,2243505564:2243505764,...
  ```

#### Step 2: Run the Python Script
- Open a terminal or command prompt.
- Navigate to the directory containing `extraction.py`.
- Execute the script:
  ```bash
  python extraction.py
  ```

#### Step 3: View Outputs
- **Excel File**:
  - Locate `extracted_data.xlsx` in the same directory.
  - Open the file to review the processed data.
- **Markdown Report**:
  - Open `report.md` with a text editor or markdown viewer.
  - The report includes summaries such as:
    - Suspicious activity.
    - Number of connections per source.
    - Packets with unusual lengths.

#### Step 4: Analyze Graphs
- The program generates visualizations displayed during execution.
- Common graphs include:
  - Number of connections over time.
  - Distribution of packet lengths.
- If you need to save a graph, use the save button in the plot window or add code to save it programmatically.

---

### **Troubleshooting**
1. **ModuleNotFoundError**:
   - Ensure all required libraries are installed using `pip install`.

2. **FileNotFoundError**:
   - Verify that `network_data.csv` is in the correct directory.

3. **Empty or Incorrect Outputs**:
   - Check the format of `network_data.csv`. Ensure columns and data are properly aligned.

---

### **Customizing the Program**
- Modify thresholds for suspicious activity detection in the script (e.g., packet length criteria).
- Customize visualization styles by editing the `matplotlib` settings in `extraction.py`.

---

### **Contact Information**
For any issues or questions, please contact the developer or refer to the documentation within the script.

