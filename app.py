import streamlit as st

st.set_page_config(page_title="Hyundai Creta EV Advisor", page_icon="🚗", layout="centered")

st.title("🚗 Hyundai Creta EV Advisor")
st.markdown("**Exclusive for Hyundai Creta Electric (India)** — Official Hyundai FAQ + Charger Advisor")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = {"variant": None, "phase": None, "distance": None}
if "step" not in st.session_state:
    st.session_state.step = "variant"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hi! Select your variant or click any topic below — official details will appear here."})

# Simple chat flow
if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / reset"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    user = prompt.lower().strip()
    if "42" in user:
        st.session_state.data["variant"] = "42 kWh"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": "✅ **42 kWh** selected.\n\nNext: single-phase or 3-phase?"})
        st.rerun()
    elif "51" in user or "long" in user:
        st.session_state.data["variant"] = "51.4 kWh Long Range"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": "✅ **51.4 kWh Long Range** selected.\n\nNext: single-phase or 3-phase?"})
        st.rerun()
    elif st.session_state.step
