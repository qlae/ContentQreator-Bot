import streamlit as st
import json
import random

st.set_page_config(page_title="ContentQreator Bot", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ---- THEME FUNCTION ----
def set_theme():
    if st.session_state.theme == "dark":
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #0e1117 !important;
                    color: #FAFAFA !important;
                }
                .css-1cpxqw2, .css-ffhzg2, .css-q8sbsg, .css-1d391kg {
                    color: #FAFAFA !important;
                }
                input, textarea, .stSelectbox div, .stTextInput input {
                    background-color: #262730 !important;
                    color: #FAFAFA !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #FFFFFF !important;
                    color: #000000 !important;
                }
                .css-1cpxqw2, .css-ffhzg2, .css-q8sbsg, .css-1d391kg {
                    color: #000000 !important;
                }
                input, textarea, .stSelectbox div, .stTextInput input {
                    background-color: #F5F5F5 !important;
                    color: #000000 !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

# fixeddd 
set_theme()


# ---- Create Tabs ----
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Setup", "My Schedule", "This Week", "Rewards", "Settings"])

# ---- Setup Tab ----
with tab1:
    st.title("🛠️ Setup")

    if 'setup_step' not in st.session_state:
        st.session_state.setup_step = 0

    questions = [
        {"key": "name", "question": "What's your name?", "type": "text"},
        {"key": "niche", "question": "What's your niche? (Choose all that apply)", "type": "multi", "options": [
            "Fitness / Gym 🏋🏽‍♀️", "Fashion 👗👟", "Hair / Beauty 💇🏽‍♀️💅🏽", "Skincare ✨", "Makeup 💄",
            "College Life / Study Tips 📚🎓", "Travel ✈️🌍", "Food / Cooking 🍳🍔", "Lifestyle (daily vlogs, routines) 🛋️🛍️",
            "Family / Motherhood 👶🏽👩🏽‍🍼", "Entrepreneurship / Business 💼📈", "Gaming 🎮", "Tech / Gadgets 📱🖥️",
            "Cars / Car Culture 🚗", "Music 🎵🎤", "Art / Drawing 🎨", "Dance 🕺🏽💃🏽", "Mental Health 🧠🫶🏽",
            "Motivational / Inspirational 🚀🌟", "Comedy / Skits 😂", "Yapper / Talking Content 🎤",
            "Sports / Athlete Life 🏈🏀⚽", "Pets / Animals 🐶🐱", "Relationship Advice 💘"
        ]},
        {"key": "platforms", "question": "Which platforms are you posting on? (Choose all that apply)", "type": "multi", "options": ["Instagram", "TikTok", "Twitter/X", "YouTube Shorts", "CapCut"]},
        {"key": "content_intensity", "question": "How intense do you want your posting schedule?", "type": "single", "options": ["Light", "Medium", "Heavy"]},
        {"key": "goal", "question": "What's your main goal?", "type": "multi", "options": ["Grow followers", "Get more shares", "Build loyal community", "Land brand deals"]}
    ]

    if st.session_state.setup_step < len(questions):
        q = questions[st.session_state.setup_step]
        st.subheader(q["question"])

        if q["type"] == "text":
            answer = st.text_input("Your answer:")
        elif q["type"] == "multi":
            answer = st.multiselect("Select all that apply:", q["options"])
        elif q["type"] == "single":
            answer = st.radio("Select one:", q["options"])

        next_button = st.button("Next", key=f"next_button_{st.session_state.setup_step}")
        if next_button:
            if answer:
                if "user_data" not in st.session_state:
                    st.session_state.user_data = {}
                st.session_state.user_data[q["key"]] = answer
                st.session_state.setup_step += 1
            else:
                st.warning("Please answer before continuing.")
    else:
        st.success("🎉 Setup complete! You're ready to move to your Schedule!")
        if st.button("Save Profile"):
            with open("data/user_profile.json", "w") as f:
                json.dump(st.session_state.user_data, f, indent=4)
            st.success("Profile saved!")

# ---- My Schedule Tab ----
with tab2:
    st.title("🗓️ My Weekly Schedule (Work, School, Gym, etc.)")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    times = [f"{h}AM" for h in range(6, 12)] + ["12PM"] + [f"{h}PM" for h in range(1, 12)]
    activities = ["Work", "School", "Gym", "Other"]

    if "busy_schedule" not in st.session_state:
        st.session_state.busy_schedule = {day: [] for day in days}

    selected_day = st.selectbox("Pick a day:", days)
    start_time = st.selectbox("Start time:", times)
    end_time = st.selectbox("End time:", times)
    activity_type = st.selectbox("Activity type:", activities)

    custom_activity = ""
    if activity_type == "Other":
        custom_activity = st.text_input("Type your custom activity:")

    if st.button("Add Busy Time"):
        if activity_type == "Other" and custom_activity.strip() == "":
            st.warning("Please type your custom activity name!")
        else:
            activity_final = custom_activity if activity_type == "Other" else activity_type
            st.session_state.busy_schedule[selected_day].append({
                "start": start_time,
                "end": end_time,
                "activity": activity_final
            })
            st.success(f"Added {activity_final} from {start_time} to {end_time} on {selected_day}! ✅")
            st.rerun()

    st.markdown("### 📋 Your Current Busy Times")
    for day, busy_list in st.session_state.busy_schedule.items():
        if busy_list:
            st.write(f"**{day} 📅**")
            for busy in busy_list:
                st.write(f"- {busy['start']} to {busy['end']}: {busy['activity']}")
# ---- This Week Tab ----
with tab3:
    st.title("📆 Your Smart Weekly Plan")

    if "user_data" not in st.session_state or "goal" not in st.session_state.user_data or "content_intensity" not in st.session_state.user_data:
        st.warning("⚡ Please complete Setup and My Schedule first!")
    else:
        st.header(f"Plan for {st.session_state.user_data.get('name', 'User')}")

        task_bank = {
            "Grow followers": ["Post a Reel 📸", "Record a trending TikTok 🎥", "Post on Story 🧵", "Engage with other creators 🔄", "Post a carousel 📚", "Join a trending hashtag challenge 🔥"],
            "Get more shares": ["Post a saveable infographic 📊", "Create a relatable meme 😂", "Write a motivational post 🚀", "Ask a poll question on Story 📈", "Create a funny skit 🎭"],
            "Build loyal community": ["Reply to DMs 💬", "Reply to all post comments ✍🏽", "Host a live Q&A 🎙️", "Post a vulnerable story 🧠", "Create a 'get to know me' post 🤝"],
            "Land brand deals": ["Post a high-quality photo 📷", "Create a mini-ad (UGC style) 🎥", "Post product review 📦", "Show 'day in life' with product ☕️", "Post a polished Story Set 🧼"]
        }

        goals = st.session_state.user_data.get("goal", [])
        intensity_list = st.session_state.user_data.get("content_intensity", [])
        intensity = intensity_list[0] if intensity_list else "Light"
        tasks_per_day = {"Light": 1, "Medium": 2, "Heavy": 3}.get(intensity, 1)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        default_times = ["9AM", "11AM", "1PM", "3PM", "5PM", "7PM"]

        def is_time_busy(time, busy_slots):
            def to_24h(t):
                h = int(t[:-2])
                am_pm = t[-2:]
                if am_pm == "PM" and h != 12:
                    h += 12
                if am_pm == "AM" and h == 12:
                    h = 0
                return h
            time_h = to_24h(time)
            for slot in busy_slots:
                start_h = to_24h(slot['start'])
                end_h = to_24h(slot['end'])
                if start_h <= time_h <= end_h:
                    return True
            return False

        if "weekly_plan" not in st.session_state:
            st.session_state.weekly_plan = {}
            for day in days:
                st.session_state.weekly_plan[day] = []
                for _ in range(tasks_per_day):
                    goal = random.choice(goals) if goals else "Grow followers"
                    task = random.choice(task_bank.get(goal, []))
                    st.session_state.weekly_plan[day].append(task)

        st.write("### 🗓️ Merged Full Agenda (Life + Content)")

        for day in days:
            st.subheader(f"{day} 📅")
            full_agenda = []
            busy_list = st.session_state.busy_schedule.get(day, [])

            for busy in busy_list:
                full_agenda.append((busy['start'], f"{busy['start']}–{busy['end']}: {busy['activity']}"))

            available_times = [t for t in default_times if not is_time_busy(t, busy_list)]

            for idx, task in enumerate(st.session_state.weekly_plan[day]):
                if idx < len(available_times):
                    time_assigned = available_times[idx]
                    full_agenda.append((time_assigned, f"{time_assigned}: {task}"))

            def sort_time_key(item):
                time_str = item[0]
                hour = int(time_str[:-2])
                am_pm = time_str[-2:]
                if am_pm == "PM" and hour != 12:
                    hour += 12
                if am_pm == "AM" and hour == 12:
                    hour = 0
                return hour

            full_agenda = sorted(full_agenda, key=sort_time_key)

            for idx, (time, entry) in enumerate(full_agenda):
                st.checkbox(f"{entry}", key=f"{day}_{time}_{idx}")

# ---- Rewards Tab ----
with tab4:
    st.title("🏆 Rewards")
    st.header("🎯 Your Achievements")

    st.success("✅ Setup completed! You created your profile. 🎉")

    if "weekly_plan" in st.session_state:
        st.success("✅ Weekly Plan generated! Ready to crush your week. 💥")

        total_tasks = 0
        completed_tasks = 0

        for key in st.session_state:
            if isinstance(key, str) and key.count("_") == 2:
                if isinstance(st.session_state[key], bool):
                    total_tasks += 1
                    if st.session_state[key]:
                        completed_tasks += 1

        if total_tasks > 0:
            percent_complete = int((completed_tasks / total_tasks) * 100)
            st.progress(percent_complete / 100)
            st.info(f"✅ {completed_tasks} of {total_tasks} tasks completed ({percent_complete}%)")

            # 🏅 Real Badge Unlocks
            if completed_tasks == total_tasks:
                st.balloons()
                st.success("🏅 Badge Unlocked: **Weekly Champion!** – You completed every task this week! 💪")
            elif completed_tasks >= total_tasks * 0.5:
                st.success("🥈 Badge Unlocked: **Momentum Builder** – You’ve completed over 50% of your tasks! 🔥")
            elif completed_tasks > 0:
                st.info("🥉 Badge Unlocked: **Starter Streak** – You’re off to a great start! Keep it going 💫")
            else:
                st.warning("📌 No badges yet. Start checking off tasks in 'This Week'!")
        else:
            st.warning("📌 No tasks tracked yet. Check off some boxes in 'This Week'!")

    else:
        st.info("⚠️ Generate your weekly plan first to begin tracking your progress.")


# ---- Settings Tab ----
with tab5:
    st.title("⚙️ Settings")
    st.header("Change your Content Plan")

    st.subheader("🎨 App Theme")
    theme_choice = st.radio("Choose theme:", ["dark", "light"], index=["dark", "light"].index(st.session_state.theme))
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    if "user_data" in st.session_state:
        new_goal = st.multiselect(
            "Update your goals:",
            ["Grow followers", "Get more shares", "Build loyal community", "Land brand deals"],
            default=st.session_state.user_data.get("goal", [])
        )

        intensity_options = ["Light", "Medium", "Heavy"]
        current_intensity = st.session_state.user_data.get("content_intensity", ["Light"])[0]
        if current_intensity not in intensity_options:
            current_intensity = "Light"

        new_intensity = st.radio(
            "Update your posting intensity:",
            intensity_options,
            index=intensity_options.index(current_intensity)
        )

        if st.button("Save Changes"):
            st.session_state.user_data["goal"] = new_goal
            st.session_state.user_data["content_intensity"] = [new_intensity]
            st.success("✅ Changes saved! Your new plan will update next time you build a week.")

    if st.button("Clear Weekly Plan"):
        if "weekly_plan" in st.session_state:
            del st.session_state.weekly_plan
            st.success("✅ Weekly plan cleared! You can generate a fresh one anytime.")
