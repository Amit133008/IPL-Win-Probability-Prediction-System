import streamlit as st
import pickle
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="IPL Win Predictor", layout="centered")

# --- BACKGROUND IMAGE ---
bg_img = "https://wallpapers.com/images/hd/ipl-2021-teams-ix7zwgff29ylomuf.jpg"

st.markdown(f"""
<style>

.stApp {{
    background-image: url("{bg_img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    background: rgba(255,255,255,0.93);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.45);
    max-width: 900px;
    margin-top: 40px;
}}

.stSelectbox div[data-baseweb="select"] > div {{
    background-color: #f8f9fa;
    border-radius: 10px;
    border: 1px solid #ccc;
}}

.stNumberInput input {{
    background-color: #f8f9fa;
    border-radius: 10px;
    border: 1px solid #ccc;
}}

.stButton button {{
    background-color: #007BFF
    color: white;
    border-radius: 10px;
    padding: 8px 18px;
    border: none;
}}

.stButton button:hover {{
    background-color: #0056b3;
}}

h1, label, p, .stMarkdown {{
    color: #1a1a1a !important;
    font-family: 'Segoe UI', sans-serif !important;
}}

.result-card {{
    background-color: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    margin-top: 25px;
}}

.progress-container {{
    width:100%;
    height:40px;
    background:#e9ecef;
    border-radius:30px;
    overflow:hidden;
    display:flex;
}}

.progress-win, .progress-loss {{
    height:100%;
    width:0%;
    animation: fillBar 1.5s ease forwards;
}}

@keyframes fillBar {{
    from {{ width: 0%; }}
    to {{ width: var(--final-width); }}
}}

header {{visibility:hidden;}}

</style>
""", unsafe_allow_html=True)

# --- DATA ---
teams = ['Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bengaluru',
'Kolkata Knight Riders','Punjab Kings','Chennai Super Kings',
'Rajasthan Royals','Delhi Capitals','Lucknow Super Giants','Gujarat Titans']

cities = ['Hyderabad','Rajkot','Bangalore','Mumbai','Indore','Kolkata',
'Delhi','Chandigarh','Kanpur','Jaipur','Chennai','Cape Town',
'Port Elizabeth','Durban','Centurion','East London',
'Johannesburg','Kimberley','Bloemfontein','Ahmedabad',
'Cuttack','Nagpur','Dharamsala','Visakhapatnam','Pune',
'Raipur','Ranchi','Abu Dhabi','Sharjah','Mohali','Bengaluru']

team_logos = {
"Chennai Super Kings":"https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/1280px-Chennai_Super_Kings_Logo.svg.png",
"Mumbai Indians":"https://upload.wikimedia.org/wikipedia/en/c/cd/Mumbai_Indians_Logo.svg",
"Royal Challengers Bengaluru":"https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Royal_Challengers_Bengaluru_Logo.svg/960px-Royal_Challengers_Bengaluru_Logo.svg.png",
"Kolkata Knight Riders":"https://upload.wikimedia.org/wikipedia/en/4/4c/Kolkata_Knight_Riders_Logo.svg",
"Sunrisers Hyderabad":"https://upload.wikimedia.org/wikipedia/en/thumb/5/51/Sunrisers_Hyderabad_Logo.svg/1280px-Sunrisers_Hyderabad_Logo.svg.png",
"Punjab Kings":"https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
"Rajasthan Royals":"https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/This_is_the_logo_for_Rajasthan_Royals%2C_a_cricket_team_playing_in_the_Indian_Premier_League_%28IPL%29.svg/960px-This_is_the_logo_for_Rajasthan_Royals%2C_a_cricket_team_playing_in_the_Indian_Premier_League_%28IPL%29.svg.png",
"Delhi Capitals":"https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
"Lucknow Super Giants":"https://upload.wikimedia.org/wikipedia/en/thumb/3/34/Lucknow_Super_Giants_Logo.svg/500px-Lucknow_Super_Giants_Logo.svg.png",
"Gujarat Titans":"https://upload.wikimedia.org/wikipedia/en/0/09/Gujarat_Titans_Logo.svg"
}

team_colors = {
"Chennai Super Kings": "#F7D417",
"Mumbai Indians": "#004BA0",
"Royal Challengers Bengaluru": "#D71920",
"Kolkata Knight Riders": "#3A225D",
"Sunrisers Hyderabad": "#FF822A",
"Punjab Kings": "#ED1B24",
"Rajasthan Royals": "#EA1A85",
"Delhi Capitals": "#004C93",
"Lucknow Super Giants": "#C8102E",
"Gujarat Titans": "#1C1C1C"
}

# --- LOAD MODEL ---
pipe = pickle.load(open('pipe.pkl','rb'))

# --- UI ---
st.title("IPL Win Predictor")

col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("Select The Batting Team", sorted(teams))
with col2:
    bowling_team = st.selectbox("Select The Bowling Team", sorted(teams))

selected_city = st.selectbox("Select The Host City", sorted(cities))
target = st.number_input("Target", min_value=0)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input("Current Score", min_value=0)
with col4:
    overs = st.number_input("Overs Completed", min_value=0, max_value=20)
with col5:
    wickets = st.number_input("Wickets Out", min_value=0, max_value=10)

predict = st.button("Predict Probability")

# --- PREDICTION ---
if predict:

    if overs > 0:

        runs_left = max(0, target - score)
        balls_left = max(0, 120 - (overs * 6))
        wickets_left = 10 - wickets

        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        # ✅ FIXED LOGIC HERE
        if runs_left <= 0:
            win_pct = 100
            loss_pct = 0

        elif balls_left <= 0:
            win_pct = 0
            loss_pct = 100

        else:
            input_df = pd.DataFrame({
                'batting_team':[batting_team],
                'bowling_team':[bowling_team],
                'city':[selected_city],
                'runs_left':[runs_left],
                'balls_left':[balls_left],
                'wickets':[wickets_left],
                'target':[target],
                'crr':[crr],
                'rrr':[rrr]
            })

            result = pipe.predict_proba(input_df)
            win_prob = result[0][1]

            # Smooth extreme values
            if win_prob > 0.99:
                win_prob = 0.95
            elif win_prob < 0.01:
                win_prob = 0.05

            win_pct = round(win_prob * 100)
            loss_pct = 100 - win_pct

        # --- RESULT CARD ---
        result_html = f"""
        <div class="result-card">

        <h3 style="text-align:center;">Match Win Probability</h3>

        <div style="display:flex; align-items:center; justify-content:space-between; margin-top:20px;">

        <div style="text-align:left;">
        <img src="{team_logos[batting_team]}" width="70"><br>
        <b>{batting_team}</b>
        <h2 style="color:{team_colors[batting_team]};">{win_pct}%</h2>
        </div>

        <div style="flex:2; margin:0 25px;">
        <div class="progress-container">

        <div class="progress-win"
        style="--final-width:{win_pct}%; background:{team_colors[batting_team]};"></div>

        <div class="progress-loss"
        style="--final-width:{loss_pct}%; background:{team_colors[bowling_team]};"></div>

        </div>
        </div>

        <div style="text-align:right;">
        <img src="{team_logos[bowling_team]}" width="70"><br>
        <b>{bowling_team}</b>
        <h2 style="color:{team_colors[bowling_team]};">{loss_pct}%</h2>
        </div>

        </div>
        </div>
        """

        st.markdown(result_html, unsafe_allow_html=True)

    else:
        st.error("Please enter overs completed to get a prediction.")