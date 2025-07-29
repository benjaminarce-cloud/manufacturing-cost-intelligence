# Manufacturing Cost Intelligence System

This project is an intelligent simulation platform for manufacturers to forecast product costs, predict margin impacts, and perform what-if scenario analysis.

---

##  How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd manufacturing-cost-intelligence
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app/main.py
    ```

5.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

---

##  Project Structure

*   `app/`: Contains the main application source code.
    *   `core/`: Core logic for data fetching, forecasting, and simulation.
    *   `components/`: UI-related modules for generating charts and dashboards.
    *   `main.py`: The main Streamlit application file.
*   `data/`: Holds input data like Bill of Materials (BOMs) and manual cost rates.
*   `models/`: Stores serialized forecasting models.
*   `reports/`: Default output directory for exported PDF reports and charts.
*   `requirements.txt`: A list of all Python packages required for the project.

---

##  How to Customize

1.  **Update Bill of Materials:** Modify `data/bom_products.csv` to match your products.
2.  **Update Manual Costs:** Edit `data/manual_cost_drivers.csv` with your specific regional costs for labor, materials, etc.
3.  **Adjust Forecasting:** The `app/core/forecasting.py` file can be updated to use different models (e.g., ARIMA) or data sources.