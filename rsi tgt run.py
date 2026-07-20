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
speed_placeholder = st.empty()
countdown_placeholder = st.empty()
wind_placeholder = st.empty()
slowdown_placeholder = st.empty()

stop_flag = st.session_state.get("stop_flag", False)


def start_countdown():
    st.session_state.stop_flag = False

    current = ip_distance
    restarted = False

    current_speed = speed
    interval_sec = 360 / current_speed

    wind_type = random.choice(["Headwind", "Tailwind"])
    wind_speed = random.randint(10, 20)

    wind_displayed = False
    slowdown_displayed = False

    while True:

        if st.session_state.stop_flag:
            countdown_placeholder.markdown("## ⏹ Countdown Stopped")
            wind_placeholder.empty()
            slowdown_placeholder.empty()
            speed_placeholder.empty()
            break

        # Display current speed
        speed_placeholder.markdown(f"### Airspeed: **{current_speed:.0f} KTAS**")

        # Display distance
        countdown_placeholder.markdown(f"# {current:.1f} NM")

        # Wind call at 3 NM
        if not wind_displayed and round(current, 1) == 3.0:
            wind_placeholder.markdown(
                f"## 🌬️ {wind_type}: **{wind_speed} KT**"
            )
            wind_displayed = True

        # Slowdown at 8 NM after IP
        if restarted and not slowdown_displayed and round(current, 1) == 8.0:
            slowdown_placeholder.markdown("## ⚠️ SLOW DOWN!")

            # Automatically change speed to 140 KTAS
            current_speed = 140
            interval_sec = 360 / current_speed

            slowdown_displayed = True

        time.sleep(interval_sec)
        current = round(current - 0.1, 1)

        # Switch from IP leg to target leg
        if not restarted and current < 0:
            current = tgt_distance
            restarted = True

            wind_placeholder.empty()
            slowdown_placeholder.empty()

            wind_type = random.choice(["Headwind", "Tailwind"])
            wind_speed = random.randint(10, 20)

            wind_displayed = False
            slowdown_displayed = False

        # End only after reaching -3 NM on target run
        elif restarted and current < -3.0:
            countdown_placeholder.markdown("# ✅ Complete")
            wind_placeholder.empty()
            slowdown_placeholder.empty()
            speed_placeholder.empty()
            break


# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Countdown"):
        start_countdown()

with col2:
    if st.button("Stop Countdown"):
        st.session_state.stop_flag = True
