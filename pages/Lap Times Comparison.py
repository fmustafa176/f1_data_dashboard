import fastf1
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

st.title("Lap Times Comparison")

year = st.selectbox(
    "Select season",
    options=list(range(2025, 2017, -1))  # 2025 to 2018
)
schedule = fastf1.get_event_schedule(year, include_testing=False)

# filter completed races
time_now = datetime.utcnow()
completed_races = schedule[schedule['Session5DateUtc'] < time_now]

# dropdown to select a completed round
round_number = st.selectbox(
    "Select Grand Prix",
    completed_races['RoundNumber'],
    format_func=lambda r: schedule.loc[schedule['RoundNumber'] == r, 'EventName'].values[0]
)

session = fastf1.get_session(year, round_number, 'R')
session.load()
laps = session.laps
if laps.empty:
    st.warning("No lap data available.")
    st.stop()

drivers = sorted(session.results['Abbreviation'].unique())
driver1 = st.selectbox("Select Driver 1", drivers)
driver2 = st.selectbox("Select Driver 2", drivers, index=1 if len(drivers) > 1 else 0)

laps_d1 = laps.pick_drivers(driver1)
laps_d2 = laps.pick_drivers(driver2)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(laps_d1['LapNumber'], laps_d1['LapTime'].dt.total_seconds(), label=driver1, linewidth=2)
ax.plot(laps_d2['LapNumber'], laps_d2['LapTime'].dt.total_seconds(), label=driver2, linewidth=2)

ax.set_xlabel("Lap")
ax.set_ylabel("Lap Time (s)")
ax.set_title(f"Lap Time Comparison — {driver1} vs {driver2}")
ax.legend()
ax.grid(True)

st.pyplot(fig)