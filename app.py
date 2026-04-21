import streamlit as st

st.set_page_config(page_title="Hyundai Creta EV Advisor", page_icon="🚗", layout="centered")

st.title("🚗 Hyundai Creta EV Advisor")
st.markdown("**Exclusive for Hyundai Creta Electric (India)** — Variant selector + Charger advice + Features + Wall vs Portable")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = {"variant": None}
if "step" not in st.session_state:
    st.session_state.step = "variant"

# Variant data
variants = {
    "42 kWh": {
        "name": "42 kWh",
        "range": "390–420 km (ARAI)",
        "power": "135 PS / 255 Nm",
        "ac_charge_time": "≈ 4 hours (10–100% with 11 kW AC)",
        "dc_charge": "≈ 58 min (10–80% with 50 kW DC)",
        "max_ac_kw": 11.0
    },
    "51.4 kWh Long Range": {
        "name": "51.4 kWh Long Range",
        "range": "473–510 km (ARAI)",
        "power": "171 PS / 255 Nm",
        "ac_charge_time": "≈ 4 hrs 50 min (10–100% with 11 kW AC)",
        "dc_charge": "≈ 58 min (10–80% with 50 kW DC)",
        "max_ac_kw": 11.0
    }
}

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome
if not st.session_state.messages:
    welcome = """👋 Hi! I'm your **Hyundai Creta EV** assistant.

Please select your variant first:

**42 kWh** — Good for daily use  
**51.4 kWh Long Range** — Best range & performance

Reply with **"42 kWh"** or **"51.4 kWh Long Range"**.

I can help with:
- Home charger installation
- Car features
- **Wall Charger vs Portable Charger** benefits"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

def show_features(variant=None):
    base = """
**Hyundai Creta Electric – Key Features (India 2026)**

**Common Features**
- Dual 10.25-inch screens, panoramic sunroof (higher trims)
- Ventilated seats, Bose audio, V2L, Bluelink connected car
- Level 2 ADAS, 360° camera, 6 airbags, CCS2 port

"""
    if variant and variant in variants:
        v = variants[variant]
        base += f"""
**{v['name']} Details**
- Range: {v['range']}
- Power: {v['power']}
- 11 kW AC Home Charging: {v['ac_charge_time']}
"""
    base += "\nType **'charger'**, **'features'**, **'wall vs portable'**, or **'variant'** anytime."
    return base

def show_wall_vs_portable():
    comparison = """
**Wall Charger vs Portable Charger – Benefits for Hyundai Creta EV**

**Dedicated Wall Charger (Recommended for daily home use)**
- **Faster & Consistent Charging**: Utilises full 11 kW (or 7.4 kW on single-phase) reliably. Full charge in \~4–5 hours vs much longer on portable.
- **Convenience**: Always mounted near parking — just plug & go. No dragging cables every day.
- **Safety**: Dedicated circuit, proper MCB/RCCB, better earthing protection. Reduces risk of overheating or tripping house circuits.
- **Smart Features**: Many support app scheduling, load management, and future-proof for higher power.
- **Long-term Savings**: Faster charging = better battery health management; looks professional and neat.
- **Best for**: Fixed parking spot (apartments or independent houses in Bengaluru).

**Portable Charger (Good as backup or for travel)**
- **Flexibility**: Plug into any 15A/16A socket, easy to carry for trips or office.
- **Lower Initial Cost**: Cheaper upfront, no installation needed.
- **Limitations for Creta EV**: Often limited to 3.3 kW (very slow — 15+ hours for full charge), higher risk of overheating if used daily on standard sockets, less safe for high-power use.

**My Recommendation for Creta EV Owners**:
- Go for a **dedicated 7.4 kW or 11 kW wall charger** if you park at home daily — it makes EV ownership truly convenient and fast.
- Use the portable charger (that comes with the car or a basic one) as emergency/travel backup.
- In Karnataka, a proper wall charger installation with load enhancement is straightforward and worth it for daily comfort & safety.

Would you like installation requirements for a wall charger? Just tell me your variant + home supply (single-phase / 3-phase)."""
    return comparison

if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / features / charger / wall vs portable / reset..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user_input = prompt.lower().strip()

    # Variant selection
    if "42" in user_input:
        st.session_state.data["variant"] = "42 kWh"
        response = f"✅ Selected **42 kWh** variant.\n\n{show_features('42 kWh')}"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": response})

    elif "51" in user_input or "long range" in user_input:
        st.session_state.data["variant"] = "51.4 kWh Long Range"
        response = f"✅ Selected **51.4 kWh Long Range** variant.\n\n{show_features('51.4 kWh Long Range')}"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Features
    elif any(word in user_input for word in ["feature", "spec", "learn", "about car"]):
        variant = st.session_state.data.get("variant")
        response = show_features(variant)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Wall vs Portable
    elif any(word in user_input for word in ["wall", "portable", "vs", "benefit", "comparison"]):
        response = show_wall_vs_portable()
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Charger installation flow
    elif st.session_state.step in ["phase", "welcome"] and st.session_state.data.get("variant"):
        if "3" in user_input:
            st.session_state.data["phase"] = "3-phase"
            response = "✅ **3-phase** — Best for full 11 kW speed on your Creta EV!"
        else:
            st.session_state.data["phase"] = "single-phase"
            response = "✅ **Single-phase** noted."
        
        st.session_state.step = "distance"
        response += "\n\nNext: Distance (metres) from main DB to parking spot?"
        st.session_state.messages.append({"role": "assistant", "content": response})

    elif st.session_state.step == "distance" and st.session_state.data.get("variant"):
        st.session_state.data["distance"] = prompt
        variant_key = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        v = variants[variant_key]
        max_kw = 11.0 if phase == "3-phase" else 7.4

        if phase == "3-phase":
            charger_type = f"11 kW Wall Charger (recommended)"
            mcb = "63A 4-pole MCB + 30mA RCCB"
            cable = "16 mm² copper"
        else:
            charger_type = "7.4 kW Wall Charger"
            mcb = "40A 2-pole MCB + 30mA RCCB"
            cable = "10 mm² copper"

        report = f"""
**✅ Wall Charger Requirements for your {variant_key} Creta EV**

**Recommended**: {charger_type}

**Details**:
- Supply: {phase.title()}
- Max Speed: **{max_kw} kW**
- Protection: {mcb}
- Cable: {cable}
- Dedicated circuit + good earthing mandatory

**Charging Time**: {v['ac_charge_time']}

Type **'wall vs portable'** to compare, **'features'**, or **'reset'**.
"""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"

    else:
        if "reset" in user_input:
            for key in list(st.session_state.keys()):
                if key != "messages":
                    del st.session_state[key]
            st.rerun()
        else:
            response = "✅ Got it! Type **variant**, **features**, **charger**, **wall vs portable**, or **reset**."
            st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar quick actions
with st.sidebar:
    st.header("Creta EV Tools")
    
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        msg = "Please select:\n• 42 kWh\n• 51.4 kWh Long Range"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()
    
    if st.button("📋 Show Features"):
        variant = st.session_state.data.get("variant")
        st.session_state.messages.append({"role": "assistant", "content": show_features(variant)})
        st.rerun()
    
    if st.button("⚡ Wall vs Portable Charger"):
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})
        st.rerun()
    
    st.caption("11 kW AC supported • Made for India (Bengaluru)")
