# DEP Meetup Dashboard

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import base64

# Setup credentials and load data
@st.cache_data
def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds/dep-participation-dashboard-0563febff8de.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1nhUmHPB2w45PCgehrsDuC0hscDc-hEPxyIlP6Sr1ndc/edit")
    sheet = spreadsheet.get_worksheet(0)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Clean and sanitize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace(" +", " ", regex=True)
    )

    # Drop personally identifiable info
    df.drop(columns=["Email Address", "First Name", "Last Name", "Contact Number"], inplace=True, errors="ignore")

    return df

# Load data
df = load_data()

# Header with centered logo and title using base64 encoding
file_path = "assets/dep_logo.png"
with open(file_path, "rb") as f:
    data = f.read()
logo = base64.b64encode(data).decode()


st.markdown(
    f"""
    <style>
        .header-container {{
            text-align: center;
            padding: 20px 10px 10px 10px;
        }}
        .header-logo {{
            width: 150px;
            margin-bottom: 10px;
        }}
        .header-title {{
            font-size: 2rem;
            font-weight: bold;
            color: #052f99;  /* Deep blue or your preferred theme color */
        }}
        hr {{
            border: none;
            border-top: 2px solid #e0e0e0;
            margin-top: 10px;
            margin-bottom: 20px;
            width: 100%;
        }}
    </style>

    <div class="header-container">
        <img src="data:image/png;base64,{logo}" class="header-logo">
        <div class="header-title">Data Engineering Pilipinas</div>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)



st.subheader("DEP Meeetup Summary")

st.markdown(
    f"""
    <style>
        .metric-wrapper {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
            margin-bottom: 5rem;
        }}
        .metric-card {{
            flex: 1 1 auto;
            max-width: 300px;
            background-color: #f1f3f6;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
        }}
        .metric-card h4 {{
            margin: 0 0 10px 0;
            font-size: 1rem;
        }}
        .metric-card h2 {{
            margin: 0;
            font-size: 2rem;
            color: #2b2b2b;
        }}
        @media (max-width: 600px) {{
            .metric-card {{
                flex: 1 1 100%;
            }}
        }}
    </style>

    <div class="metric-wrapper">
        <div class="metric-card">
            <p>Total Responses</p>
            <h2>{len(df)}</h2>
        </div>
        <div class="metric-card">
            <p>First-time Attendees</p>
            <h2>{df["Is this the first time you attended an on-site DEP event?"].str.lower().eq("yes").sum()}</h2>
        </div>
        <div class="metric-card">
            <p>Interested to be Humans of DEP</p>
            <h2>{df[df.filter(like="Interested in being part of Humans").columns[0]].str.lower().eq("yes").sum()}</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


    
# Sidebar filters
st.sidebar.header("🔍 Filter Options")
gender_filter = st.sidebar.multiselect("Gender", df["Gender"].dropna().unique())
role_filter = st.sidebar.multiselect("Role Description", df["What best describes what you do?"].dropna().unique())
province_filter = st.sidebar.multiselect("Province", df["Province of Residence"].dropna().unique())
city_filter = st.sidebar.multiselect("City", df["City of Residence"].dropna().unique())
participation_col = df.filter(like="participate or contribute").columns[0]
sort_option = st.sidebar.selectbox(
    "Sort Table & Charts By:",
    ["Timestamp", "Province of Residence", "City of Residence", "What best describes what you do?"]
)


filtered_df = df.copy()
if gender_filter:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]
if role_filter:
    filtered_df = filtered_df[filtered_df["What best describes what you do?"].isin(role_filter)]
if province_filter:
    filtered_df = filtered_df[filtered_df["Province of Residence"].isin(province_filter)]
if city_filter:
    filtered_df = filtered_df[filtered_df["City of Residence"].isin(city_filter)]



# Apply sorting to filtered_df
if sort_option in filtered_df.columns:
    filtered_df = filtered_df.sort_values(by=sort_option, ascending=True)



st.subheader("Filtered Table")
st.dataframe(filtered_df)

# Export Option
st.subheader("Export Filtered Data")
st.download_button(
    "Download Filtered Data as CSV",
    filtered_df.to_csv(index=False),
    file_name="filtered_responses.csv"
)

st.subheader("Current Filter Summary")

# Compute counts from filtered_df
gender_count = filtered_df["Gender"].nunique()
role_count = filtered_df["What best describes what you do?"].nunique()
province_count = filtered_df["Province of Residence"].nunique()
city_count = filtered_df["City of Residence"].nunique()
participation_count = filtered_df[participation_col].nunique()


st.markdown(
    f"""
    <style>
        .filter-metric-wrapper {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
            margin-bottom: 5rem;
        }}
        .filter-metric-card {{
            flex: 1 1 auto;
            max-width: 120px;
            background-color: #ffffff;
            border-radius: 12px;
            padding: 15px;
            text-align: left;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        }}
        .filter-metric-card h4 {{
            margin: 0 0 5px 0;
            font-size: 0.9rem;
        }}
        .filter-metric-card h2 {{
            margin: 0;
            font-size: 1.8rem;
            color: #333;
        }}
        @media (max-width: auto) {{
            .filter-metric-card {{
                flex: 1 1 100%;
            }}
        }}
    </style>

    <div class="filter-metric-wrapper">
        <div class="filter-metric-card">
            <h4>Genders Selected</h4>
            <h2>{gender_count}</h2>
        </div>
        <div class="filter-metric-card">
            <h4>Roles Selected</h4>
            <h2>{role_count}</h2>
        </div>
        <div class="filter-metric-card">
            <h4>Provinces Selected</h4>
            <h2>{province_count}</h2>
        </div>
        <div class="filter-metric-card">
            <h4>Cities Selected</h4>
            <h2>{city_count}</h2>
        </div>
        <div class="filter-metric-card">
            <h4>Participation Types</h4>
            <h2>{participation_count}</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

display_mode = st.radio("Display Mode:", ["Count", "Percentage"], horizontal=True)

if "Gender" in filtered_df.columns:
    gender_counts = filtered_df["Gender"].value_counts(normalize=(display_mode == "Percentage")).reset_index()
    gender_counts.columns = ["Gender", "Value"]
    fig_gender = px.pie(
        gender_counts,
        names="Gender",
        values="Value",
        title=f"Gender Distribution ({display_mode})",
        color_discrete_sequence=['#0075a4']
    )
    fig_gender.update_traces(textposition='inside', textinfo='percent+label' if display_mode == "Percentage" else 'label+value')
    st.plotly_chart(fig_gender, use_container_width=True)


# 2️⃣ Role Description Bar Chart
if "What best describes what you do?" in filtered_df.columns:
    role_counts = filtered_df["What best describes what you do?"].value_counts(normalize=(display_mode == "Percentage")).reset_index()
    role_counts.columns = ["Role", "Value"]
    fig_role = px.bar(
        role_counts.sort_values(by="Value", ascending=True),
        y="Role",
        x="Value",
        orientation="h",
        title=f"Roles in the Community ({display_mode})",
        color_discrete_sequence=['#008bad']
    )
    fig_role.update_layout(margin=dict(t=40, b=40), height=400)
    st.plotly_chart(fig_role, use_container_width=True)


if "Province of Residence" in filtered_df.columns:
    province_counts = filtered_df["Province of Residence"].value_counts(normalize=(display_mode == "Percentage")).reset_index()
    province_counts.columns = ["Province", "Value"]
    fig_province = px.bar(
        province_counts.sort_values(by="Value", ascending=True),
        y="Province",
        x="Value",
        orientation="h",
        title=f"Respondents by Province ({display_mode})",
        color_discrete_sequence=['#009fa1']
    )
    fig_province.update_layout(margin=dict(t=40, b=40), height=300)
    st.plotly_chart(fig_province, use_container_width=True)



# Province by City breakdown
if "City of Residence" in filtered_df.columns:
    city_counts = filtered_df["City of Residence"].value_counts(normalize=(display_mode == "Percentage")).reset_index()
    city_counts.columns = ["City", "Value"]
    fig_city = px.bar(
        city_counts.sort_values(by="Value", ascending=True),
        y="City",
        x="Value",
        orientation="h",
        title=f"Respondents by City ({display_mode})",
        color_discrete_sequence=['#00af82']
    )
    fig_city.update_layout(margin=dict(t=40, b=40), height=600)
    st.plotly_chart(fig_city, use_container_width=True)


if participation_col in filtered_df.columns:
    exploded = (
        filtered_df[participation_col]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )

    valid_preferences = [
        "Volunteer for group initiatives",
        "Mentor or guide fellow community members",
        "Answer community surveys",
        "Speak in community events and meetups",
        "Connect with sponsors",
        "Share expertise through workshops and trainings",
        "Help build and grow the community through partnerships",
        "Organize or host community events",
        "Regularly post content and/or resources (i.e., articles, books, and tools)",
        "Serve as resource for a specific topic",
        "Lead a study group",
        "Offer internship or job opportunities to students",
        "Network with people in this industry"
    ]

    counts = exploded[exploded.isin(valid_preferences)].value_counts(normalize=(display_mode == "Percentage")).reset_index()
    counts.columns = ["Preference", "Value"]
    counts = counts.sort_values(by="Value", ascending=True)

    fig_participation = px.bar(
        counts,
        y="Preference",
        x="Value",
        orientation="h",
        title=f"Participation Preferences ({display_mode})",
        color_discrete_sequence=["#51bb57"]
    )
    fig_participation.update_layout(margin=dict(t=20, b=20), height=400)
    st.plotly_chart(fig_participation, use_container_width=True)







