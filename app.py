import streamlit as st

st.set_page_config(page_title="Hyundai EV Advisor", page_icon="🚗", layout="centered")

st.title("🚗 Hyundai EV Advisor")
st.markdown("**Exclusive for Hyundai Creta Electric (India)** — Official Hyundai FAQ + Charger Advisor")

# ==================== SESSION STATE INITIALIZATION (VERY IMPORTANT) ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = {"variant": None, "phase": None, "distance": None}
if "step" not in st.session_state:
    st.session_state.step = "variant"

# ==================== QUICK BUTTONS ON THE RIGHT SIDE ====================
st.subheader("Official Hyundai Information")
col1, col2, col3, col4, col5 = st.columns(5)
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
    if st.button("⚡ V2L Features", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "**V2L Features (Official)**\nUp to **3.6 kW** – powers laptops, appliances, etc."})
        st.rerun()
with col5:
    if st.button("🛡️ Extended Warranty", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "See full Extended Warranty prices in the left sidebar."})
        st.rerun()

st.divider()

# ==================== DISPLAY CHAT HISTORY ====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hi! Select your variant from the sidebar or type 42 kWh / 51.4 kWh."})

# ==================== MAIN CHAT INPUT ====================
if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / reset"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user = prompt.lower().strip()

    if "42" in user:
        st.session_state.data["variant"] = "42 kWh"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": "✅ **42 kWh** selected.\n\nNext: Is your home supply **single-phase** or **3-phase**?"})
        st.rerun()

    elif "51" in user or "long" in user:
        st.session_state.data["variant"] = "51.4 kWh Long Range"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": "✅ **51.4 kWh Long Range** selected.\n\nNext: Is your home supply **single-phase** or **3-phase**?"})
        st.rerun()

    elif st.session_state.step == "phase" and st.session_state.data.get("variant"):
        if "3" in user or "three" in user:
            st.session_state.data["phase"] = "3-phase"
            msg = "✅ **3-phase** noted — Perfect for full 11 kW speed!"
        else:
            st.session_state.data["phase"] = "single-phase"
            msg = "✅ **Single-phase** noted."
        msg += "\n\nFinal: Approximate distance (in metres) from your main electrical DB to the parking spot? (e.g. 5, 10, 15)"
        st.session_state.step = "distance"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()

    elif st.session_state.step == "distance" and st.session_state.data.get("variant"):
        st.session_state.data["distance"] = prompt
        variant = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        max_kw = "11 kW" if phase == "3-phase" else "7.4 kW"
        mcb = "63A 4-pole MCB + 30mA RCCB" if phase == "3-phase" else "40A 2-pole MCB + 30mA RCCB"
        cable = "16 mm² copper" if phase == "3-phase" else "10 mm² copper"

        report = f"""
**✅ Wall Charger Requirements – {variant}**

**Official Price**: ₹75,215 (incl. installation, commissioning & GST)

**Recommended Charger**: {max_kw} AC Wall Charger

**Electrical Requirements**:
- Supply: {phase.title()}
- Max Speed: **{max_kw}**
- Protection: {mcb}
- Cable Size: {cable}
- Dedicated circuit only
- Proper earthing (< 1 ohm) mandatory

Type **reset** to start over."""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"
        st.rerun()

    elif "reset" in user:
        st.session_state.clear()
        st.rerun()

# ==================== LEFT SIDEBAR ====================
with st.sidebar
