import streamlit as st
import pandas as pd
import fastf1
from datetime import datetime

year = st.selectbox(
    "Select season",
    options=list(range(2025, 2017, -1))  # 2025 to 2018
)
schedule = fastf1.get_event_schedule(year, include_testing=False)

# filter completed races
time_now = datetime.utcnow()
completed_races = schedule[schedule['Session5DateUtc'] < time_now]

# dropdown to select a completed round
round_selected = st.selectbox(
    "Select a completed Grand Prix",
    completed_races['RoundNumber'],
    format_func=lambda r: schedule.loc[schedule['RoundNumber'] == r, 'EventName'].values[0]
)

race = fastf1.get_session(year, round_selected, 'R')
race.load()

results = race.SessionResults()

summary = results[[
    'Abbreviation', 
    'FullName', 
    'TeamName', 
    'GridPosition', 
    'ClassifiedPosition', 
    'FastestLapTime', 
    'Status'
]].rename(columns={
    'Abbreviation': 'Code',
    'FullName': 'Driver',
    'TeamName': 'Team',
    'GridPosition': 'Started',
    'ClassifiedPosition': 'Finished',
    'FastestLapTime': 'Fastest Lap',
    'Status': 'Status'
})

print(summary)
