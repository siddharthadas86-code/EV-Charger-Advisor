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
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hi! Select your variant or click any topic in the sidebar."})

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
        st.session_state.messages.append({"role": "assistant", "content": "**✅ Wall Charger Requirements**\nOfficial Price: ₹75,215"})
        st.session_state.step = "done"
    elif "reset" in user:
        st.session_state.clear()
        st.rerun()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("Creta EV Tools")
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()

    st.divider()
    st.subheader("Official Hyundai Information")

    # FAQ buttons
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

    # Extended Warranty buttons
    if st.button("🛡️ Extended Warranty Price (0-90 days)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ Extended Warranty Prices – 0-90 Days (Slab 1)**\n\n**Creta EV**\n• 4th Yr / 80K km : ₹24,099\n• 5th Yr / 100K km : ₹27,399\n• 4th & 5th Yr / 100K : ₹34,899\n• 4th & 5th Yr / 140K : ₹41,299\n• 4th–7th Yr / 140K : ₹89,699\n• 5th–7th Yr / 140K : ₹83,099\n• 6th & 7th Yr / 140K : ₹74,599"})
        st.rerun()

    if st.button("🛡️ Extended Warranty Price (91-365 days)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ Extended Warranty Prices – 91-365 Days (Slab 2)**\n\n**Creta EV**\n• 4th Yr / 80K km : ₹25,399\n• 5th Yr / 100K km : ₹28,799\n• 4th & 5th Yr / 100K : ₹36,699\n• 4th & 5th Yr / 140K : ₹42,399\n• 4th–7th Yr / 140K : ₹94,799\n• 5th–7th Yr / 140K : ₹82,299\n• 6th & 7th Yr / 140K : ₹78,399"})
        st.rerun()

    if st.button("🛡️ Extended Warranty Price (>365 days / more than 1 year)"):
        st.session_state.messages.append({"role": "assistant", "content": "**🛡️ Extended Warranty Prices – >365 Days (Slab 3)**\n\n**Creta EV**\n• 4th Yr / 80K km : ₹33,599\n• 5th Yr / 100K km : ₹35,599\n• 4th & 5th Yr / 100K : ₹48,499\n• 4th & 5th Yr / 140K : ₹57,499\n• 4th–7th Yr / 140K : ₹1,27,099\n• 5th–7th Yr / 140K : ₹1,09,299\n• 6th & 7th Yr / 140K : ₹1,03,899"})
        st.rerun()

    # New iCare Package button (IONIQ 5 only)
    if st.button("🛡️ iCare Package (IONIQ 5 only)"):
        st.session_state.messages.append({"role": "assistant", "content": """**🛡️ iCare Package (IONIQ 5 only)**

Two "iCare" package options:
1) **3 Yr / 30k Km** – Rs 67,619
2) **5 Yr / 50k Km** – Rs 107,802

Customers can purchase within **1 year** of New Car purchase.

**Coverage**:
- Periodic Maintenance (Brake Fluid, EV Coolant, Climate Control Air Filter)
- 10 Running Repair items (Blade Wiper, Brake Disc/Pad, Bulbs & Fuses, etc.)
- Wheel alignment & Wheel Balancing

*Source: Official Hyundai iCare Package*"""})
        st.rerun()

    st.caption("Official Hyundai Data • Jan 2025")
