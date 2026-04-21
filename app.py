import streamlit as st

st.set_page_config(page_title="Hyundai Creta EV Advisor", page_icon="🚗", layout="centered")

st.title("🚗 Hyundai Creta EV Advisor")
st.markdown("**Exclusive for Hyundai Creta Electric (India)** — Variant + Charger + Features + Wall vs Portable")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = {"variant": None, "phase": None}
if "step" not in st.session_state:
    st.session_state.step = "variant"

# Variant data (updated with latest 2026 specs)
variants = {
    "42 kWh": {
        "name": "42 kWh",
        "range": "390–420 km (ARAI)",
        "power": "133–135 PS / 255 Nm",
        "ac_charge_time": "≈ 4 hours (10–100% with 11 kW AC)",
        "dc_charge": "≈ 39–58 min (10–80% with 50 kW DC)"
    },
    "51.4 kWh Long Range": {
        "name": "51.4 kWh Long Range",
        "range": "473–510 km (ARAI)",
        "power": "169–171 PS / 255 Nm",
        "ac_charge_time": "≈ 4 hrs 50 min (10–100% with 11 kW AC)",
        "dc_charge": "≈ 39–58 min (10–80% with 50 kW DC)"
    }
}

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Initial welcome
if not st.session_state.messages:
    welcome = """👋 Hi! I'm your **Hyundai Creta EV** assistant.

**First step:** Please select your variant.

Reply with:
- **42 kWh**
- **51.4 kWh** or **Long Range**

After that I can help with:
- Home wall charger installation requirements
- Car features
- Wall Charger vs Portable Charger benefits"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

def show_features(variant=None):
    base = """**Hyundai Creta Electric Features (India 2026)**

**Common Highlights**
- Dual 10.25" screens, panoramic sunroof (higher trims)
- Ventilated seats, Bose audio, V2L, Bluelink connected features
- Level 2 ADAS, 360° camera, 6 airbags, CCS2 port

"""
    if variant and variant in variants:
        v = variants[variant]
        base += f"""
**{v['name']}**
- Range: {v['range']}
- Power: {v['power']}
- 11 kW AC Charging: {v['ac_charge_time']}
- DC Fast: {v['dc_charge']}
"""
    return base + "\n\nType **features**, **charger**, **wall vs portable**, **variant**, or **reset** anytime."

def show_wall_vs_portable():
    return """**Wall Charger vs Portable Charger – For Creta EV**

**✅ Recommended: Dedicated Wall Charger**
- Uses full 11 kW (or 7.4 kW safely)
- Full charge in 4–5 hours vs 12–20+ hours on portable
- Safer (dedicated MCB/RCCB + proper earthing)
- Convenient (wall-mounted, no daily plugging hassle)
- Better for battery health & daily use in Bengaluru

**Portable Charger (included with car)**
- Useful for travel or emergency
- Limited to \~3.3 kW → very slow for daily use
- Higher risk if used on non-dedicated sockets

**My Advice**: Install a proper **7.4 kW or 11 kW wall charger** at home for the best Creta EV experience.

Want installation requirements? Tell me your variant + supply type (single-phase / 3-phase)."""

# Main chat logic
if prompt := st.chat_input("Type here (e.g. 42 kWh, 51.4, features, charger, wall vs portable, reset)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user = prompt.lower().strip()

    # === Variant Selection (improved detection) ===
    if any(x in user for x in ["42", "kwh", "42kwh"]):
        st.session_state.data["variant"] = "42 kWh"
        response = f"✅ **42 kWh** variant selected.\n\n{show_features('42 kWh')}\n\nNext: Is your home supply **single-phase** or **3-phase**?"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": response})

    elif any(x in user for x in ["51", "51.4", "long range", "lr", "longrange"]):
        st.session_state.data["variant"] = "51.4 kWh Long Range"
        response = f"✅ **51.4 kWh Long Range** variant selected.\n\n{show_features('51.4 kWh Long Range')}\n\nNext: Is your home supply **single-phase** or **3-phase**?"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": response})

    # === Features ===
    elif any(x in user for x in ["feature", "spec", "learn", "about car"]):
        variant = st.session_state.data.get("variant")
        st.session_state.messages.append({"role": "assistant", "content": show_features(variant)})

    # === Wall vs Portable ===
    elif any(x in user for x in ["wall", "portable", "vs", "benefit", "comparison"]):
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})

    # === Charger flow ===
    elif st.session_state.step == "phase" and st.session_state.data.get("variant"):
        if "3" in user or "three" in user:
            st.session_state.data["phase"] = "3-phase"
            response = "✅ **3-phase** noted — Perfect for full 11 kW charging!"
        else:
            st.session_state.data["phase"] = "single-phase"
            response = "✅ **Single-phase** noted."
        response += "\n\nFinal: Approximate distance (in metres) from your main electrical DB to the parking spot? (e.g. 5, 10, 15)"
        st.session_state.step = "distance"
        st.session_state.messages.append({"role": "assistant", "content": response})

    elif st.session_state.step == "distance" and st.session_state.data.get("variant"):
        st.session_state.data["distance"] = prompt
        variant_key = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        v = variants[variant_key]
        max_kw = 11.0 if phase == "3-phase" else 7.4

        charger_type = "11 kW Wall Charger" if phase == "3-phase" else "7.4 kW Wall Charger"
        mcb = "63A 4-pole MCB + 30mA RCCB" if phase == "3-phase" else "40A 2-pole MCB + 30mA RCCB"
        cable = "16 mm² copper" if phase == "3-phase" else "10 mm² copper"

        report = f"""
**✅ Wall Charger Requirements – {variant_key} Creta EV**

**Recommended Charger**: {charger_type}

**Details**:
- Supply: {phase.title()}
- Max Speed: **{max_kw} kW**
- Protection: {mcb}
- Cable: {cable}
- Dedicated circuit + proper earthing (<1 ohm) required

**Charging Time**: {v['ac_charge_time']}

Type **wall vs portable**, **features**, or **reset** to start over.
"""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"

    else:
        if "reset" in user:
            for key in list(st.session_state.keys()):
                if key != "messages":
                    del st.session_state[key]
            st.rerun()
        else:
            help_msg = "✅ Got it! Try typing:\n• **42 kWh** or **51.4 kWh**\n• **features**\n• **charger**\n• **wall vs portable**\n• **reset**"
            st.session_state.messages.append({"role": "assistant", "content": help_msg})

# Sidebar
with st.sidebar:
    st.header("Creta EV Tools")
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()
    if st.button("📋 Show Features"):
        variant = st.session_state.data.get("variant")
        st.session_state.messages.append({"role": "assistant", "content": show_features(variant)})
        st.rerun()
    if st.button("⚡ Wall vs Portable"):
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})
        st.rerun()
    st.caption("11 kW AC supported • Bengaluru friendly")
