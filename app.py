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
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hi! Select your variant from the sidebar or type 42 kWh / 51.4 kWh."})

# Main chat logic
if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / reset"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user = prompt.lower().strip()

    # Variant selection
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

    # Phase step
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

    # Distance step → Final report
    elif st.session_state.step == "distance" and st.session_state.data.get("variant"):
        st.session_state.data["distance"] = prompt
        variant = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        max_kw = "11 kW" if phase == "3-phase" else "7.4 kW"
        mcb = "63A 4-pole MCB + 30mA RCCB" if phase == "3-phase" else "40A 2-pole MCB + 30mA RCCB"
        cable = "16 mm² copper" if phase == "3-phase" else "10 mm² copper"

        report = f"""
**✅ Wall Charger Requirements – {variant} Creta EV**

**Official Price**: ₹75,215 (incl. installation, commissioning & GST)

**Recommended Charger**: {max_kw} AC Wall Charger

**Electrical Requirements**:
- Supply: {phase.title()}
- Max Speed: **{max_kw}**
- Protection: {mcb}
- Cable Size: {cable}
- Dedicated circuit only
- Proper earthing (< 1 ohm) mandatory

**Charging Time**: 4 hours (42 kWh) / 4 hrs 50 min (51.4 kWh) on 11 kW wall charger

Type **reset** to start over."""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"
        st.rerun()

    elif "reset" in user:
        st.session_state.clear()
        st.rerun()

    else:
        st.session_state.messages.append({"role": "assistant", "content": "Type **42 kWh** or **51.4 kWh** to begin, or use the sidebar buttons."})

# Sidebar with all toggles
with st.sidebar:
    st.header("Creta EV Tools")
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()

    st.divider()
    st.subheader("Official Hyundai Information")

    if st.button("🚗 Driving Range"):
        st.session_state.messages.append({"role": "assistant", "content": "**Driving Range (Official)**\n• Creta 42 kWh → 390 km\n• Creta 51.4 kWh → 473 km"})
        st.rerun()

    if st.button("🔌 Charging System"):
        st.session_state.messages.append({"role": "assistant", "content": "**Charging System (Official)**\n11 kW AC Wall Box Charger → **₹75,215** (incl. installation & GST)"})
        st.rerun()

    if st.button("🔋 Charging Options Available"):
        st.session_state.messages.append({"role": "assistant", "content": "**Charging Options Available (Official)**\n• Portable AC (ICCB)\n• Wall box (AC fast)\n• DC fast charging"})
        st.rerun()

    if st.button("⏱️ Charging Time for Creta & IONIQ 5"):
        st.session_state.messages.append({"role": "assistant", "content": "**Official Charging Times**\nAC Wall Box (11 kW): 4 hrs (42 kWh) / 4 hrs 50 min (51.4 kWh)\nPortable: 17–24+ hrs\nDC 50 kW: 58–63 min"})
        st.rerun()

    if st.button("⚡ V2L Features"):
        st.session_state.messages.append({"role": "assistant", "content": "**V2L Features (Official)**\nUp to **3.6 kW** – powers laptops, appliances, etc."})
        st.rerun()

    if st.button("🛞 Tires Myth"):
        st.session_state.messages.append({"role": "assistant", "content": "**Tires Myth (Official)**\nTire wear depends on driving pattern. Same style = same wear as ICE."})
        st.rerun()

    if st.button("🌡️ Driving Condition"):
        st.session_state.messages.append({"role": "assistant", "content": "**Driving Condition (Official)**\n• Hot weather: Battery chiller – safe\n• High humidity: IP67 rated"})
        st.rerun()

    if st.button("🌊 Can I drive in waterlogged situation?"):
        st.session_state.messages.append({"role": "assistant", "content": "**Waterlogged Situation (Official)**\nNot recommended. HV parts are IP67 rated."})
        st.rerun()

    if st.button("🔋 What is SOH?"):
        st.session_state.messages.append({"role": "assistant", "content": "**SOH = State of Health (Official)**\nMeasures battery degradation. Lower SOH = lower range."})
        st.rerun()

    if st.button("📉 Life of HV Battery"):
        st.session_state.messages.append({"role": "assistant", "content": "**Life of HV Battery (Official)**\nNo fixed lifespan. Depends on usage & maintenance."})
        st.rerun()

    if st.button("⚠️ Symptoms of High Voltage Battery"):
        st.session_state.messages.append({"role": "assistant", "content": "**Symptoms of Defective HV Battery (Official)**\nError message appears on cluster / AVNT."})
        st.rerun()

    if st.button("🛡️ Warranty of HV Battery"):
        st.session_state.messages.append({"role": "assistant", "content": "**HV Battery Warranty (Official)**\n**8 Years / 1,60,000 km** (whichever earlier)"})
        st.rerun()

    # Extended Warranty buttons (all three)
    if st.button("🛡️ Extended Warranty Price (0-90 days)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ Extended Warranty Prices – 0-90 Days (Slab 1)**\n\n**Creta EV**\n• 4th Yr / 80K km : ₹24,099\n• 5th Yr / 100K km : ₹27,399\n• 4th & 5th Yr / 100K : ₹34,899\n• 4th & 5th Yr / 140K : ₹41,299\n• 4th–7th Yr / 140K : ₹89,699\n• 5th–7th Yr / 140K : ₹83,099\n• 6th & 7th Yr / 140K : ₹74,599"})
        st.rerun()

    if st.button("🛡️ Extended Warranty Price (91-365 days)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ Extended Warranty Prices – 91-365 Days (Slab 2)**\n\n**Creta EV**\n• 4th Yr / 80K km : ₹25,399\n• 5th Yr / 100K km : ₹28,799\n• 4th & 5th Yr / 100K : ₹36,699\n• 4th & 5th Yr / 140K : ₹42,399\n• 4th–7th Yr / 140K : ₹94,799\n• 5th–7th Yr / 140K : ₹82,299\n• 6th & 7th Yr / 140K : ₹78,399"})
        st.rerun()

    if st.button("🛡️ Extended Warranty Price (>365 days / more than 1 year)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ Extended Warranty Prices – >365 Days (Slab 3)**\n\n**Creta EV**\n• 4th Yr / 80K km : ₹33,599\n• 5th Yr / 100K km : ₹35,599\n• 4th & 5th Yr / 100K : ₹48,499\n• 4th & 5th Yr / 140K : ₹57,499\n• 4th–7th Yr / 140K : ₹1,27,099\n• 5th–7th Yr / 140K : ₹1,09,299\n• 6th & 7th Yr / 140K : ₹1,03,899"})
        st.rerun()

    if st.button("🛡️ iCare Package (IONIQ 5 only)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ iCare Package (IONIQ 5 only)**\n\n1) 3 Yr / 30k Km – Rs 67,619\n2) 5 Yr / 50k Km – Rs 107,802\n\nCan be purchased within 1 year of new car purchase."})
        st.rerun()

    st.caption("Official Hyundai Data • Jan 2025")
