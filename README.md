# DEP Meetup Dashboard

DEP Meetup Dashboard is a **Streamlit web app** built for **Data Engineering Pilipinas (DEP)** to visualize and explore community event data collected from Google Forms.  

It provides organizers and volunteers with insights into:

- Attendance trends  
- Demographics (gender, role, location)  
- First-time attendees  
- Community participation preferences  
- "Humans of DEP" interest  

---

## Features

- **Interactive Dashboard** – Filter by gender, role, province, and city  
- **Summary Metrics** – View total responses, first-time attendees, and more  
- **Visual Analytics** – Pie charts and bar charts for demographics & preferences  
- **Export Option** – Download filtered data as CSV for deeper analysis  
- **Privacy First** – Automatically removes PII (emails, names, contact numbers)  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Web app framework  
- [Google Sheets API (gspread)](https://docs.gspread.org/) – Data source integration  
- [Pandas](https://pandas.pydata.org/) – Data cleaning & transformation  
- [Plotly Express](https://plotly.com/python/plotly-express/) – Interactive visualizations  
- [Google Cloud Service Account](https://cloud.google.com/iam/docs/service-accounts) – Authentication  

---

## 📂 Project Structure

DEP-Meetup-Dashboard/

│── assets/ # Static assets (e.g., dep_logo.png)

│── app.py # Main Streamlit app

│── requirements.txt # Python dependencies

│── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/DEP-Meetup-Dashboard.git
cd DEP-Meetup-Dashboard

2. Create & Activate Virtual Environment
# Mac/Linux
python -m venv .venv
source .venv/bin/activate  

# Windows
python -m venv .venv
.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Google Service Account

Create a Google Cloud Project and enable:
Google Sheets API
Google Drive API
Generate a Service Account Key (JSON file).
Share your Google Sheet with the service account email (Viewer access).
Add credentials to Streamlit secrets file:

# .streamlit/secrets.toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
client_id = "..."


Replace the Google Sheet URL in app.py with your own survey sheet.

5. Run the App
streamlit run app.py


Open the local app at http://localhost:8501
.

📸 Screenshots
![Dashboard Screenshot](assets/Dep_Meetup_Summary.png)

👥 About

This project is created by Katherine Bulac for the Data Engineering Pilipinas (DEP) community volunteers to support event management, reporting, and decision-making.

📜 License

MIT License – Free to use and modify.

