import fastf1
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from datetime import datetime

# create cache directory
fastf1.Cache.enable_cache('cache')

time_now = datetime.utcnow()
date_now = time_now.date()
year_now = time_now.year

schedule = fastf1.get_event_schedule(year_now, include_testing=False)

for _, row in schedule.iterrows():
    if row[21] > time_now:
        next_round = row['RoundNumber']
        break

event = fastf1.get_event(year_now, next_round)

st.title(f"{event['OfficialEventName']}")
st.subheader(f"{event['Location']}, {event['Country']} - Round {event['RoundNumber']}")

# timezone selection
tz_offsets = [f"{'+' if i >= 0 else ''}{i:02}:{m:02}" for i in range(-12, 15) for m in (0, 30)]
tz_offset_str = st.selectbox(
    "Timezone", 
    options=tz_offsets,
    index=tz_offsets.index("+00:00"),
    format_func=lambda x: f"UTC{x}",
)
offset_hours, offset_minutes = map(int, tz_offset_str.split(":"))
offset = pd.Timedelta(hours=offset_hours, minutes=offset_minutes)

# create a schedule table
schedule_data = []

for i in range(1, 6):
    session = event.get(f'Session{i}')
    session_time = event.get(f'Session{i}DateUtc')
    if pd.notnull(session_time):
        local_time = pd.to_datetime(session_time) + offset

    if pd.notnull(session) and pd.notnull(session_time):
        schedule_data.append({
            "Session": session,
            "Local Time": local_time.strftime("%A, %d %B %Y — %H:%M")
        })

# convert to DataFrame for display
schedule_df = pd.DataFrame(schedule_data)
st.markdown("### 🕒 Session Schedule")
st.dataframe(schedule_df, use_container_width=True)


