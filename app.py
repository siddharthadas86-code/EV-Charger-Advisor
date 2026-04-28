import streamlit as st

st.set_page_config(page_title="Hyundai EV Advisor", page_icon="🚗", layout="centered")

st.title("🚗 Hyundai EV Advisor")
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
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hi! Select your variant from the sidebar or type 42 kWh / 51.4 kWh."})

# ==================== QUICK TOGGLE BUTTONS ON MAIN SCREEN (RIGHT SIDE) ====================
st.subheader("Official Hyundai Information")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🚗 Driving Range", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "**Driving Range (Official)**\n• Creta 42 kWh → 390 km\n• Creta 51.4 kWh → 473 km"})
        st.rerun()
with col2:
    if st.button("🔌 Charging System", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "**Charging System (Official)**\n11 kW AC Wall Box Charger → **₹75,215** (incl. installation & GST)"})
        st.rerun()
with col3:
    if st.button("⏱️ Charging Time", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "**Official Charging Times**\nAC Wall Box (11 kW): 4 hrs (42 kWh) / 4 hrs 50 min (51.4 kWh)\nPortable: 17–24+ hrs\nDC 50 kW: 58–63 min"})
        st.rerun()
with col4:
    if st.button("🛡️ Extended Warranty", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "Click the full Extended Warranty buttons in the left sidebar for all slabs (0-90, 91-365, >365 days)."})
        st.rerun()

st.divider()

# Main chat logic (fixed distance input)
if prompt := st.chat_input
