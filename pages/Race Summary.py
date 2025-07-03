import streamlit as st
import pandas as pd
import fastf1
import fastf1.plotting
from datetime import datetime
import matplotlib.pyplot as plt

st.title("Race Summary")

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
    "Select Grand Prix",
    completed_races['RoundNumber'],
    format_func=lambda r: schedule.loc[schedule['RoundNumber'] == r, 'EventName'].values[0]
)

race = fastf1.get_session(year, round_selected, 'R')
race.load()

# Get the race results as a DataFrame
results = race.results.copy()  # treat it like a standard DataFrame

# Safely select and rename relevant columns
summary = results.loc[:, [
    'Abbreviation',
    'FullName',
    'TeamName',
    'ClassifiedPosition',
    'GridPosition',
    'Status'
]].rename(columns={
    'Abbreviation': 'Code',
    'FullName': 'Driver',
    'TeamName': 'Team',
    'ClassifiedPosition': 'Finished',
    'GridPosition': 'Started',
    'Status': 'Status'
})

st.markdown("###  Race Summary")
st.dataframe(summary, use_container_width=True)

fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

fig, ax = plt.subplots(figsize=(8.0, 4.9))

for drv in race.drivers:
    drv_laps = race.laps.pick_drivers(drv)
    if drv_laps.empty:
        continue  # skip drivers with no lap data

    abb = drv_laps['Driver'].iloc[0]
    style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=race)
    ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)


ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize='small')
ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')
st.pyplot(fig)