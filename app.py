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

# Official data from Hyundai FAQ PDF
variants = {
    "42 kWh": {"name": "42 kWh", "range": "390 km (ARAI)", "power": "133–135 PS", "ac_time": "4 hours", "dc_time": "58 min"},
    "51.4 kWh Long Range": {"name": "51.4 kWh Long Range", "range": "473 km (ARAI)", "power": "169–171 PS", "ac_time": "4 hrs 50 min", "dc_time": "58 min"}
}

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hi! Select your variant from the sidebar and explore the official Hyundai information below."})

# Chat logic (kept simple and working)
if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / faq / reset"):
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
    elif st.session_state.step == "phase":
        if "3" in user:
            st.session_state.data["phase"] = "3-phase"
            st.session_state.messages.append({"role": "assistant", "content": "✅ **3-phase** noted.\n\nFinal: Distance (metres) from DB to parking?"})
        else:
            st.session_state.data["phase"] = "single-phase"
            st.session_state.messages.append({"role": "assistant", "content": "✅ **Single-phase** noted.\n\nFinal: Distance (metres) from DB to parking?"})
        st.session_state.step = "distance"
        st.rerun()
    elif st.session_state.step == "distance":
        variant = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        v = variants[variant]
        report = f"**✅ Charger Requirements – {variant}**\n\nOfficial Wall Charger Price: ₹75,215\nCharging Time: {v['ac_time']}\nSupply: {phase.title()}"
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"
    elif "reset" in user:
        st.session_state.clear()
        st.rerun()

# ==================== SIDEBAR WITH ALL TOGGLES ====================
with st.sidebar:
    st.header("Creta EV Tools")
    
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()
    
    if st.button("📋 Official Hyundai FAQ"):
        st.session_state.messages.append({"role": "assistant", "content": "Check the expanders below for all official info!"})
        st.rerun()

    st.divider()

    # === ALL REQUESTED TOGGLES (EXPANDERS) ===
    st.subheader("Official Hyundai Information")

    with st.expander("🚗 Driving Range"):
        st.write("**Creta EV (ARAI certified)**\n• 42 kWh → 390 km\n• 51.4 kWh Long Range → 473 km\n• IONIQ 5 → 631 km\n\nActual range depends on driving conditions.")

    with st.expander("🔌 Charging System"):
        st.write("**11 kW AC Wall Box Charger for Creta EV**\n• Price: **₹75,215** (including installation, commissioning & GST)\n• Total with connected features ≈ **₹78,219**")

    with st.expander("🔋 Charging Options Available"):
        st.write("3 types of charging options:\n• Portable AC charging (ICCB)\n• Wall box charger (AC fast charging)\n• DC fast charging (Charging station)")

    with st.expander("⏱️ Charging Time for Creta & IONIQ 5"):
        st.write("**AC Wall Box (11 kW)**\n• 42 kWh: 4 hours\n• 51.4 kWh: 4 hrs 50 min\n• IONIQ 5: 5 hrs 55 min (10–100%)\n\n**Portable ICCB**: 17–24+ hrs\n**50 kW DC Fast**: 58–63 min (10–80%)")

    with st.expander("⚡ V2L Features"):
        st.write("**Vehicle-to-Load (V2L)**\nThe Creta EV can supply power to external devices up to **3.6 kW**.\nYou can power laptops, camping equipment, or household appliances using the charging inlet.")

    with st.expander("🛞 Tires Myth"):
        st.write("Tire wear in EV vs ICE depends only on driving pattern.\nEV has more torque, so aggressive acceleration can cause faster wear.\nWith the same driving style, tire wear is almost the same as ICE vehicles.")

    with st.expander("🌡️ Driving Condition"):
        st.write("• **Hot weather / deserts**: Battery has a chiller — no issue in Indian summer.\n• **High humidity**: Hyundai EV is IP67 rated — safe to use.")

    with st.expander("🌊 Can I drive in waterlogged situation?"):
        st.write("**Not recommended** to drive any vehicle in waterlogged conditions.\nHowever, all electronic couplers & HV equipment are **IP67 rated** (can withstand 1 bar pressure for 30 minutes).")

    with st.expander("🔋 What is SOH?"):
        st.write("**SOH = State of Health**\nIt shows how much the battery capacity has degraded compared to its original capacity.\nLower SOH = lower range.")

    with st.expander("📉 Life of HV Battery"):
        st.write("There is **no fixed lifespan** for the HV battery.\nIt depends on driving habits, environmental conditions, and maintenance.\nWarranty: 8 Years / 1,60,000 km (whichever earlier).")

    with st.expander("⚠️ Symptoms of Defective High Voltage Battery"):
        st.write("In most cases, an **error message** will pop up on the cluster / AVNT screen.")

    with st.expander("🛡️ Warranty of HV Battery"):
        st.write("**8 Years / 1,60,000 km** (whichever is earlier)\n\nNote: Accident / waterlogging damage is **not** covered under warranty.")

    st.caption("Official Hyundai Data • Jan 2025 Service Bulletin")

    # Current variant features (kept for convenience)
    if st.session_state.data.get("variant"):
        st.divider()
        st.subheader("Selected Variant Features")
        v = variants[st.session_state.data["variant"]]
        st.write(f"**{v['name']}**\n• Range: {v['range']}\n• 11 kW AC: {v['ac_time']}")
