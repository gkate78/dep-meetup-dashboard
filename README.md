DEP Meetup Dashboard

DEP Meetup Dashboard is a Streamlit web app built for Data Engineering Pilipinas (DEP) to visualize and explore community event data collected from Google Forms.

It provides organizers and volunteers with insights into:

Attendance trends

Demographics (gender, role, location)

First-time attendees

Community participation preferences

"Humans of DEP" interest

Features

Interactive Dashboard: Filters by gender, role, province, and city.

Summary Metrics: Total responses, first-time attendees, and more.

Visual Analytics: Pie charts and bar charts for demographics and participation preferences.

Export Option: Download filtered data as CSV for further analysis.

Privacy First: Automatically removes personally identifiable information (PII) such as emails, names, and contact numbers.

Tech Stack

Streamlit
 – Web app framework

Google Sheets API (gspread)
 – Data source integration

Pandas
 – Data cleaning and transformation

Plotly Express
 – Interactive visualizations

Google Cloud Service Account
 – Authentication

📂 Project Structure
DEP-Meetup-Dashboard/
│── assets/               # Static assets (e.g., dep_logo.png)
│── app.py                # Main Streamlit app
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation

⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/<your-username>/DEP-Meetup-Dashboard.git
cd DEP-Meetup-Dashboard

2. Create & Activate Virtual Environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Google Service Account

Create a Google Cloud Project and enable Google Sheets API + Google Drive API.

Generate a Service Account Key (JSON file).

Add the service account email to your Google Sheet with Viewer access.

In Streamlit, add the key to your secrets file:

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


Then open the local URL (default: http://localhost:8501) in your browser.

📸 Screenshots

![alt text](image.png)


👥 About

This project is created by Katherine Bulac for the Data Engineering Pilipinas (DEP) community volunteers to support event management, reporting, and decision-making.

📜 License

MIT License – free to use and modify.