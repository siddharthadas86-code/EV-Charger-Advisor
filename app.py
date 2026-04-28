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

# Official Variant Data (from Hyundai FAQ)
variants = {
    "42 kWh": {
        "name": "42 kWh",
        "range": "390 km (ARAI)",
        "power": "133–135 PS / 255 Nm",
        "ac_time": "4 hours (10–100% with 11 kW AC)",
        "dc_time": "58 min (10–80% with 50 kW DC)"
    },
    "51.4 kWh Long Range": {
        "name": "51.4 kWh Long Range",
        "range": "473 km (ARAI)",
        "power": "169–171 PS / 255 Nm",
        "ac_time": "4 hrs 50 min (10–100% with 11 kW AC)",
        "dc_time": "58 min (10–80% with 50 kW DC)"
    }
}

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome
if not st.session_state.messages:
    welcome = """👋 Hi! I'm your **Hyundai Creta EV** assistant.

**Step 1:** Select your variant:
- **42 kWh**
- **51.4 kWh Long Range**

I can also show you **Official Hyundai FAQ** data anytime."""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

def show_features(variant=None):
    text = "**Hyundai Creta EV Features (Official)**\n\n"
    if variant and variant in variants:
        v = variants[variant]
        text += f"**{v['name']}**\n- ARAI Range: {v['range']}\n- Power: {v['power']}\n- 11 kW AC Charging: {v['ac_time']}\n"
    text += "\nType **faq**, **features**, **charger**, **wall vs portable**, **variant**, or **reset**."
    return text

def show_wall_vs_portable():
    return """**Wall Charger vs Portable Charger (Official Recommendation)**

✅ **Dedicated 11 kW Wall Charger** = Best choice for daily use (fast, safe, convenient)
Portable ICCB charger = Only for emergency/travel (very slow: 17–20+ hours)"""

def show_official_faq():
    return """**📋 Official Hyundai EV FAQ (Jan 2025 Service Bulletin)**

**Driving Range (ARAI)**
- Creta EV 42 kWh → **390 km**
- Creta EV 51.4 kWh Long Range → **473 km**

**Wall Box Charger (Official Price)**
- Creta EV 11 kW AC Wall Box Charger → **₹75,215** (including installation, commissioning & GST)
- Total with connected features ≈ **₹78,219**

**Official Charging Times**
- 11 kW AC Wall Box: 4 hrs (42 kWh) / 4 hrs 50 min (51.4 kWh) → 10–100%
- Portable ICCB: 17–20+ hrs → 10–100%
- 50 kW DC Fast: 58 min → 10–80%

**Battery Health Tips (Official)**
- Daily charging to **80%** is recommended for best battery life
- Safe charging cycle: **20% → 80%**

**Other Official Points**
- **V2L (Vehicle-to-Load)**: Up to **3.6 kW** (powers laptops, appliances, etc.)
- **Battery Warranty**: **8 Years / 1,60,000 km** (whichever earlier)
- IP67 rated → safe in heavy rain (but avoid driving in deep waterlogging)

Type **charger** for your personalised installation requirements or **reset** to start over."""

# Chat input
if prompt := st.chat_input("Type: 42 kWh / 51.4 kWh / faq / features / charger / wall vs portable / reset"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user = prompt.lower().strip()

    # Variant selection
    if "42" in user:
        st.session_state.data["variant"] = "42 kWh"
        st.session_state.step = "phase"
        msg = f"✅ **42 kWh** selected.\n\n{show_features('42 kWh')}\n\nNext: Is your home supply **single-phase** or **3-phase**?"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()

    elif "51" in user or "long" in user:
        st.session_state.data["variant"] = "51.4 kWh Long Range"
        st.session_state.step = "phase"
        msg = f"✅ **51.4 kWh Long Range** selected.\n\n{show_features('51.4 kWh Long Range')}\n\nNext: Is your home supply **single-phase** or **3-phase**?"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()

    # Official FAQ
    elif any(word in user for word in ["faq", "official", "hyundai", "bulletin"]):
        st.session_state.messages.append({"role": "assistant", "content": show_official_faq()})

    # Features
    elif "feature" in user:
        st.session_state.messages.append({"role": "assistant", "content": show_features(st.session_state.data.get("variant"))})

    # Wall vs Portable
    elif "wall" in user or "portable" in user:
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})

    # Phase
    elif st.session_state.step == "phase" and st.session_state.data.get("variant"):
        if "3" in user or "three" in user:
            st.session_state.data["phase"] = "3-phase"
            msg = "✅ **3-phase** noted — Perfect for full 11 kW speed!"
        else:
            st.session_state.data["phase"] = "single-phase"
            msg = "✅ **Single-phase** noted."
        msg += "\n\nFinal: Approximate distance (in metres) from your main electrical DB to parking spot?"
        st.session_state.step = "distance"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()

    # Distance → Report (with official price)
    elif st.session_state.step == "distance" and st.session_state.data.get("variant"):
        st.session_state.data["distance"] = prompt
        variant = st.session_state.data["variant"]
        phase = st.session_state.data.get("phase", "single-phase")
        v = variants[variant]
        max_kw = "11 kW" if phase == "3-phase" else "7.4 kW"
        mcb = "63A 4-pole" if phase == "3-phase" else "40A 2-pole"
        cable = "16 mm²" if phase == "3-phase" else "10 mm²"

        report = f"""
**✅ Official Charger Requirements – {variant} Creta EV**

**Recommended**: {max_kw} Wall Charger  
**Official Price** (Hyundai): **₹75,215** (incl. installation & GST)

**Requirements**:
- Supply: {phase.title()}
- Max Speed: **{max_kw}**
- Protection: {mcb} MCB + 30mA RCCB
- Cable: {cable} copper
- Dedicated circuit + proper earthing

**Official Charging Time**: {v['ac_time']}

Type **faq** for more official Hyundai info or **reset** to start over."""
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.session_state.step = "done"

    else:
        if "reset" in user:
            st.session_state.clear()
            st.rerun()
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Type **42 kWh** or **51.4 kWh**, or use **faq** / sidebar buttons."})

# Sidebar
with st.sidebar:
    st.header("Creta EV Tools")
    if st.button("🔄 Select Variant"):
        st.session_state.step = "variant"
        st.rerun()
    if st.button("📋 Show Features"):
        st.session_state.messages.append({"role": "assistant", "content": show_features(st.session_state.data.get("variant"))})
        st.rerun()
    if st.button("📋 Official Hyundai FAQ"):
        st.session_state.messages.append({"role": "assistant", "content": show_official_faq()})
        st.rerun()
    if st.button("⚡ Wall vs Portable"):
        st.session_state.messages.append({"role": "assistant", "content": show_wall_vs_portable()})
        st.rerun()
    st.caption("Official Hyundai Data • Jan 2025")
