import streamlit as st

st.set_page_config(page_title="Hyundai Creta EV Advisor", page_icon="🚗", layout="centered")

st.title("🚗 Hyundai Creta EV Advisor")
st.markdown("**Exclusive for Hyundai Creta Electric (India)**")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data" not in st.session_state:
    st.session_state.data = {"variant": None, "phase": None, "distance": None}
if "step" not in st.session_state:
    st.session_state.step = "variant"

variants = {
    "42 kWh": {"name": "42 kWh", "range": "390–420 km", "power": "133–135 PS", "ac_time": "≈ 4 hours (11 kW)", "dc_time": "39–58 min"},
    "51.4 kWh Long Range": {"name": "51.4 kWh Long Range", "range": "473–510 km", "power": "169–171 PS", "ac_time": "≈ 4 hrs 50 min (11 kW)", "dc_time": "39–58 min"}
}

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome message
if not st.session_state.messages:
    welcome = """👋 Hi! I'm your **Hyundai Creta EV** assistant.

Please select your variant first:

• **42 kWh**  
• **51.4 kWh Long Range**

After selecting, I'll guide you through charger installation, features, or wall vs portable comparison."""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

def show_features(variant=None):
    text = "**Hyundai Creta EV Features**\n\n"
    if variant and variant in variants:
        v = variants[variant]
        text += f"**{v['name']}**\n- Range: {v['range']}\n- Power: {v['power']}\n- 11 kW AC: {v['ac_time']}\n"
    text += "\nType **features**, **charger**, **wall vs portable**, **variant**, or **reset**."
    return text

def show_wall_vs_portable():
    return """**Wall Charger vs Portable Charger (Creta EV)**

**✅ Wall Charger (Recommended)**
- Full 11 kW speed → 4–5 hr full charge
- Safer, dedicated circuit, no daily hassle
- Better for battery health & daily Bengaluru use

**Portable Charger**
- Good for travel/emergency only
- Slow (\~3.3 kW) → 12–20+ hours

**Recommendation**: Install a dedicated wall charger at home."""

# Chat input handling
if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / features / charger / wall vs portable / reset"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user = prompt.lower().strip()

    # Variant selection
    if "42" in user:
        st.session_state.data["variant"] = "42 kWh"
        msg = f"✅ **42 kWh** selected.\n\n{show_features('42 kWh')}\n\nNext: Is your home supply **single-phase** or **3-phase**?"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": msg})

    elif "51" in user or "long" in user:
        st.session_state.data["variant"] = "51.4 kWh Long Range"
        msg = f"✅ **51.4 kWh Long Range** selected.\n\n{show_features('51.4 kWh Long Range')}\n\nNext: Is your home supply **single-phase** or **3-phase**?"
        st.session_state.step = "phase"
        st.session_state.messages.append({"role": "assistant", "content": msg})

    # Features
    elif "feature" in user:
        variant = st.session_state.data.get("variant")
        st.session_state.messages.append({"role": "assistant", "content": show_features(variant)})

    # Wall vs Portable
    elif "wall" in user or "portable" in user:
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})

    # Phase (single/3-phase)
    elif st.session_state.step == "phase" and st.session_state.data.get("variant"):
        if "3" in user or "three" in user or "three phase" in user:
            st.session_state.data["phase"] = "3-phase"
            msg = "✅ **3-phase** noted — Great for full 11 kW speed!"
        else:
            st.session_state.data["phase"] = "single-phase"
            msg = "✅ **Single-phase** noted."
        msg += "\n\nFinal step: Approximate distance (in metres) from your main electrical DB to the parking spot? (e.g. 5, 10, 15)"
        st.session_state.step = "distance"
        st.session_state.messages.append({"role": "assistant", "content": msg})

    # Distance → Final Report
    elif st.session_state.step == "distance" and st.session_state.data.get("variant"):
        st.session_state.data["distance"] = prompt
        variant = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        v = variants[variant]
        max_kw = "11 kW" if phase == "3-phase" else "7.4 kW"
        mcb = "63A 4-pole" if phase == "3-phase" else "40A 2-pole"
        cable = "16 mm²" if phase == "3-phase" else "10 mm²"

        report = f"""
**✅ Charger Installation for your {variant} Creta EV**

**Recommended**: {max_kw} Wall Charger

**Requirements**:
- Supply: {phase.title()}
- Max Speed: **{max_kw}**
- Protection: {mcb} MCB + 30mA RCCB
- Cable: {cable} copper
- Dedicated circuit + good earthing

**Charging Time**: {v['ac_time']}

**Tip**: In Bengaluru, a proper wall charger installation makes daily charging fast and safe.

Type **reset** to start over or **wall vs portable** to compare."""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"

    else:
        if "reset" in user:
            st.session_state.clear()
            st.rerun()
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Please select variant first (42 kWh or 51.4 kWh Long Range), or type **features**, **charger**, **wall vs portable**, or **reset**."})

# Sidebar
with st.sidebar:
    st.header("Creta EV Tools")
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()
    if st.button("📋 Show Features"):
        st.session_state.messages.append({"role": "assistant", "content": show_features(st.session_state.data.get("variant"))})
        st.rerun()
    if st.button("⚡ Wall vs Portable"):
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})
        st.rerun()
    st.caption("11 kW AC supported • Bengaluru friendly")
