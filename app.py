import streamlit as st

st.set_page_config(page_title="EV Charger Advisor", page_icon="🚗", layout="centered")
st.title("🚗 EV Charger Installation Advisor (India)")
st.markdown("**Tell me your vehicle specs → I’ll give you exact home installation requirements** (Bharat standards + 2026 guidelines)")

# Known popular EVs in India (2025-2026 models) with onboard AC charger rating
known_vehicles = {
    "Tata Nexon EV": 7.4,
    "Tata Punch EV": 7.4,
    "Tata Curvv EV": 7.4,
    "MG ZS EV": 7.4,
    "MG Windsor EV": 7.4,
    "BYD Atto 3": 7.0,
    "Hyundai Creta Electric": 11.0,
    "Mahindra XEV 9e / BE 6e": 11.0,
    "Maruti Suzuki e Vitara": 11.0,
    "Other / Custom": None
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = "vehicle"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# First welcome message
if not st.session_state.messages:
    welcome = """Hi! 👋 I'm your EV Charger Installation Advisor for India.

To get accurate requirements, I need:
1. Your EV make & model (or max AC charging power in kW)
2. A bit about your home electrical supply

**Type your vehicle make and model** (e.g. "Tata Nexon EV" or "Hyundai Creta Electric")"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

if prompt := st.chat_input("Type your answer here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ==================== STEP 1: Vehicle ====================
    if st.session_state.current_question == "vehicle":
        vehicle_input = prompt.strip().title()
        st.session_state.data["vehicle"] = vehicle_input

        # Check if known
        matched = False
        for name, kw in known_vehicles.items():
            if name.lower() in vehicle_input.lower() or vehicle_input.lower() in name.lower():
                st.session_state.data["max_ac_kw"] = kw
                matched = True
                response = f"✅ Great! **{name}** has a **{kw} kW** onboard AC charger (CCS2). Perfect for home Level-2 charging.\n\nNext question: Is your home supply **single-phase** (most common in India) or **3-phase**? Just reply with the word."
                st.session_state.current_question = "phase"
                break

        if not matched:
            try:
                # User gave a number directly
                kw = float(prompt)
                st.session_state.data["max_ac_kw"] = kw
                response = f"✅ Noted! Your vehicle supports **{kw} kW** AC charging.\n\nNext: Is your home supply **single-phase** or **3-phase**?"
                st.session_state.current_question = "phase"
            except:
                response = f"Got **{vehicle_input}**. I don't have exact data for this model yet. Please tell me the **maximum AC charging power** of your onboard charger (usually 3.3, 7.2, 7.4 or 11 kW). You can find it in your vehicle manual or spec sheet."
                st.session_state.current_question = "custom_kw"

        st.session_state.messages.append({"role": "assistant", "content": response})

    # ==================== STEP 2: Phase ====================
    elif st.session_state.current_question == "phase":
        phase = prompt.lower()
        st.session_state.data["phase"] = "3-phase" if "3" in phase else "single-phase"
        response = f"✅ **{st.session_state.data['phase'].title()}** noted.\n\nFinal details (optional but helpful): What is the approximate distance from your electrical DB (distribution board) to the parking spot where you want to install the charger? (e.g. 5 metres, 15 metres)"
        st.session_state.current_question = "distance"
        st.session_state.messages.append({"role": "assistant", "content": response})

    # ==================== STEP 3: Distance & Generate Report ====================
    elif st.session_state.current_question == "distance":
        st.session_state.data["distance"] = prompt
        max_kw = st.session_state.data.get("max_ac_kw", 7.4)

        # Generate recommendation
        if max_kw <= 3.5:
            charger_type = "3.3 kW Level-1 (16A)"
            mcb = "20A 2-pole MCB + 30mA RCCB"
            cable = "4 mm² copper (or existing 15A socket with dedicated line)"
        elif max_kw <= 7.5:
            charger_type = "7.2–7.4 kW Level-2 (32A)"
            mcb = "40A 2-pole MCB + 30mA RCCB"
            cable = "6 mm² copper (if <10m) or 10 mm² copper (if >10m)"
        else:
            charger_type = f"{max_kw} kW Level-2 (or 11 kW if 3-phase)"
            mcb = "40–63A 2-pole/4-pole MCB + 30mA RCCB"
            cable = "10–16 mm² copper (recommended for safety)"

        phase_note = "✅ You can use single-phase 230V (most homes)" if st.session_state.data["phase"] == "single-phase" else "✅ Excellent! 3-phase allows faster 11 kW+ charging."

        report = f"""
**✅ Your EV Charger Installation Requirements**

**Vehicle**: {st.session_state.data['vehicle']}  
**Recommended Charger**: {charger_type} AC (Type-2 / CCS2 compatible)

**Electrical Requirements (India 2026 standards)**  
{phase_note}
- **Voltage**: 230V single-phase (or 415V 3-phase)
- **Circuit**: Dedicated circuit only (no sharing with other appliances)
- **Protection**: {mcb}
- **Cable Size**: {cable}
- **Earthing**: < 1 ohm (mandatory)
- **Charger Location**: Wall-mounted, IP54 weatherproof, within cable reach of parking

**Additional Advice**
- Total installation cost ≈ ₹8,000 – ₹18,000 (cable + labour) + charger price
- No separate electricity connection needed for home use (Ministry of Power guidelines)
- If your sanctioned load is < 5–8 kW, apply for load enhancement with your DISCOM (free/easy in Karnataka)
- Hire a **certified electrician** who knows EV chargers (ask for Bharat EV / IEC 61851 compliance)

Would you like me to adjust anything (different model, longer cable, 3-phase upgrade, cost estimate, etc.)? Just reply!
"""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.current_question = "done"

    # After first report, allow free chat / reset
    else:
        if "reset" in prompt.lower() or "start over" in prompt.lower():
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        else:
            response = "✅ Got it! If you want to change any detail or start fresh, just type **'reset'** or tell me the new info."
            st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar info
with st.sidebar:
    st.header("Popular EVs (quick select)")
    for v in known_vehicles:
        if st.button(v):
            st.session_state.messages = []
            st.session_state.data = {"vehicle": v, "max_ac_kw": known_vehicles[v]}
            st.session_state.current_question = "phase"
            st.rerun()
    st.caption("Built for India • Single-phase 230V • 2026 standards")
    st.caption("Data from official EV specs & Ministry of Power guidelines")
