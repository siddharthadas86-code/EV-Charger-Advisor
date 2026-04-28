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
    welcome = """👋 Hi! I'm your Hyundai Creta EV assistant.

Select your variant from the sidebar, then click any topic under **Official Hyundai Information** — the full official details from Hyundai's FAQ will appear here on the right."""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Simple chat flow for charger advisor
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
    elif st.session_state.step == "phase":
        phase = "3-phase" if "3" in user else "single-phase"
        st.session_state.data["phase"] = phase
        st.session_state.messages.append({"role": "assistant", "content": f"✅ **{phase}** noted.\n\nFinal: Approximate distance (in metres) from main DB to parking spot?"})
        st.session_state.step = "distance"
        st.rerun()
    elif st.session_state.step == "distance":
        report = f"**✅ Wall Charger Requirements**\nOfficial Price: ₹75,215\nSupply: {st.session_state.data.get('phase', 'single-phase').title()}"
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"
    elif "reset" in user:
        st.session_state.clear()
        st.rerun()

# ==================== SIDEBAR WITH BUTTONS ====================
with st.sidebar:
    st.header("Creta EV Tools")
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()

    st.divider()
    st.subheader("Official Hyundai Information")

    # All buttons - clicking sends exact PDF content to main chat area
    if st.button("🚗 Driving Range"):
        st.session_state.messages.append({"role": "assistant", "content": "**Driving Range (Official Hyundai FAQ)**\n\nDriving range of a full charged EV may vary depending on driving pattern, road condition.\n\n**ARAI certified:**\n• Creta 42 kWh → 390 km\n• Creta 51 kWh → 473 km\n• IONIQ5 → 631 km"})
        st.rerun()

    if st.button("🔌 Charging System"):
        st.session_state.messages.append({"role": "assistant", "content": "**Charging System (Official)**\n\n**11 kW AC Wall Box Charger for Creta EV**\n• Price: ₹75,215 (including installation, commissioning & GST)\n• Total with connected features ≈ ₹78,219"})
        st.rerun()

    if st.button("🔋 Charging Options Available"):
        st.session_state.messages.append({"role": "assistant", "content": "**Charging Options Available (Official)**\n\n3 types of charging options:\n• Portable AC charging - ICCB\n• Wall box charger - AC fast charging\n• DC fast charging - Charging station"})
        st.rerun()

    if st.button("⏱️ Charging Time for Creta & IONIQ 5"):
        st.session_state.messages.append({"role": "assistant", "content": "**Official Charging Times**\n\n**AC Wall Box (11 kW)**\n• 42 kWh: 4 hours\n• 51.4 kWh Long Range: 4 hrs 50 min\n• IONIQ5: 5 hrs 55 min (10–100%)\n\n**Portable ICCB**: 16 hrs 55 min – 24 hrs 40 min\n**50 kW DC Fast**: 58–63 min (10–80%)"})
        st.rerun()

    if st.button("⚡ V2L Features"):
        st.session_state.messages.append({"role": "assistant", "content": "**V2L Features (Official)**\n\nThe vehicle-to-load (V2L) feature allows the car's battery to power external devices and appliances (maximum load of 3.6 kW).\nYou can plug in laptops, camping equipment, or household appliances using the charging inlet."})
        st.rerun()

    if st.button("🛞 Tires Myth"):
        st.session_state.messages.append({"role": "assistant", "content": "**Tires Myth (Official)**\n\nTire wear in EV vs ICE depends only on driving pattern.\nEV has more torque, so aggressive acceleration can cause faster tire wear.\nWith the same driving style, tire wear is almost the same as ICE vehicles."})
        st.rerun()

    if st.button("🌡️ Driving Condition"):
        st.session_state.messages.append({"role": "assistant", "content": "**Driving Condition (Official)**\n\n• In extremely hot conditions: EV has Battery Chiller — battery is cooled to optimum temperature. No issue in Indian summer.\n• High Humidity: Hyundai EV is IP67 rated — safe to use."})
        st.rerun()

    if st.button("🌊 Can I drive in waterlogged situation?"):
        st.session_state.messages.append({"role": "assistant", "content": "**Waterlogged Situation (Official)**\n\nIt is **not suggested** to drive any vehicle in waterlogged conditions.\nHowever, all electronic couplers & HV equipment are IP67 rated (can take 1 bar pressure for 30 minutes)."})
        st.rerun()

    if st.button("🔋 What is SOH?"):
        st.session_state.messages.append({"role": "assistant", "content": "**What is SOH? (Official)**\n\nSOH = State of Health.\nIt is a measure of how much battery capacity has degraded compared to its original capacity.\nLower the SOH, lower will be the range."})
        st.rerun()

    if st.button("📉 Life of HV Battery"):
        st.session_state.messages.append({"role": "assistant", "content": "**Life of HV Battery (Official)**\n\nThere is **no fixed recommended life span** of Hyundai EV battery.\nActual lifespan varies based on driving habits, environmental conditions, and maintenance practices."})
        st.rerun()

    if st.button("⚠️ Symptoms of High Voltage Battery"):
        st.session_state.messages.append({"role": "assistant", "content": "**Symptoms of Defective HV Battery (Official)**\n\nIn most cases, an **Error** will pop up on the cluster / AVNT screen."})
        st.rerun()

    if st.button("🛡️ Warranty of HV Battery"):
        st.session_state.messages.append({"role": "assistant", "content": "**Warranty of HV Battery (Official)**\n\n**8 Years / 1,60,000 km** (whichever is earlier)\n\nAccident / Waterlogging damage is **not** covered under warranty."})
        st.rerun()

    st.caption("Official Hyundai Data • Jan 2025")
