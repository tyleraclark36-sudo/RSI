import streamlit as st
import time
import random

st.set_page_config(page_title="Approach Countdown", layout="centered")
st.title("✈️ Bomb Run Timing")

# --- User Inputs ---
speed = st.number_input("Speed (KTAS)", min_value=1.0, value=120.0, step=1.0)
ip_distance = st.number_input("Distance to IP (NM)", min_value=0.0, value=5.0, step=0.1)
tgt_distance = st.number_input("IP → TGT Distance (NM)", min_value=0.0, value=10.0, step=0.1)

# --- Display Placeholders ---
countdown_placeholder = st.empty()
wind_placeholder = st.empty()
slowdown_placeholder = st.empty()

stop_flag = st.session_state.get("stop_flag", False)


def start_countdown():
    st.session_state.stop_flag = False
    interval_sec = 360 / speed  # Seconds per 0.1 NM

    current = ip_distance
    restarted = False

    # Generate one random wind report for the first leg
    wind_type = random.choice(["Headwind", "Tailwind"])
    wind_speed = random.randint(10, 20)

    wind_displayed = False
    slowdown_displayed = False

    while True:
        if st.session_state.stop_flag:
            countdown_placeholder.markdown("## ⏹ Countdown Stopped")
            wind_placeholder.empty()
            slowdown_placeholder.empty()
            break

        # Display current distance
        countdown_placeholder.markdown(f"# {current:.1f} NM")

        # Wind call at 3 NM
        if not wind_displayed and round(current, 1) == 3.0:
            wind_placeholder.markdown(
                f"## 🌬️ {wind_type}: **{wind_speed} KT**"
            )
            wind_displayed = True

        # Slowdown call at 8 NM AFTER passing the IP
        if restarted and not slowdown_displayed and round(current, 1) == 8.0:
            slowdown_placeholder.markdown("## ⚠️ SLOW DOWN!")
            slowdown_displayed = True

        time.sleep(interval_sec)
        current = round(current - 0.1, 1)

        # Transition from IP countdown to Target countdown
        if current < 0:
            if not restarted:
                current = tgt_distance
                restarted = True

                # Reset displays for target run
                wind_placeholder.empty()
                slowdown_placeholder.empty()

                # Generate a new random wind call for the target run
                wind_type = random.choice(["Headwind", "Tailwind"])
                wind_speed = random.randint(10, 20)

                wind_displayed = False
                slowdown_displayed = False
            else:
                countdown_placeholder.markdown("# ✅ Complete")
                wind_placeholder.empty()
                slowdown_placeholder.empty()
                break


# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Countdown"):
        start_countdown()

with col2:
    if st.button("Stop Countdown"):
        st.session_state.stop_flag = True
