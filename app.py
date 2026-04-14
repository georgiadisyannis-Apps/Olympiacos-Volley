import streamlit as st

st.set_page_config(page_title="Volley Tactical Pro v60", layout="centered")

# --- CSS v60: Επαναφορά Χρωμάτων & Hard-Locked Layout ---
st.markdown("""
<style>
    /* 1. Γενικές Ρυθμίσεις */
    .stApp { background-color: #0E1117; }
    .block-container {
        max-width: 380px !important;
        padding: 1rem 0.5rem !important;
        margin: 0 auto;
    }

    /* 2. Τακτικό Wrapper */
    .tactical-wrapper {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .court-title {
        width: 100%;
        text-align: center;
        font-weight: bold;
        padding: 12px 0;
        color: white;
        font-size: 14px;
        border-radius: 10px 10px 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 3. Γήπεδο & Κελιά (Επαναφορά Χρωμάτων) */
    .grid-layout {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
        border: 4px solid #333;
        background-color: #1a1a1a; /* Σκούρο φόντο γηπέδου */
    }

    .player-cell {
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 24px;
        border-radius: 6px;
        position: relative;
        aspect-ratio: 1.1 / 1;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .label-p { position: absolute; top: 3px; left: 5px; font-size: 9px; color: rgba(255,255,255,0.6); }

    /* Χρώματα Ομάδων (Επαναφορά) */
    .opp-court-cell { background-color: #3498DB !important; color: #FFFFFF !important; }
    .oly-court-cell { background-color: #C0392B !important; color: #FFFFFF !important; }

    /* Highlights (Επαναφορά) */
    .highlight-target { background-color: #F1C40F !important; color: #000 !important; border: 2px solid #333 !important; }
    .highlight-setter { background-color: #E67E22 !important; color: #fff !important; border: 2px solid #D35400 !important; }

    .net-divider {
        width: 100%; height: 22px;
        background-color: #333;
        background-image: linear-gradient(45deg, #444 25%, transparent 25%, transparent 50%, #444 50%, #444 75%, transparent 75%, transparent);
        background-size: 10px 10px;
        border: 2px solid #000;
        margin: 12px 0;
    }

    /* 4. ΚΟΥΜΠΙΑ: ΟΡΙΣΤΙΚΗ ΔΙΟΡΘΩΣΗ ΓΙΑ ΚΑΘΕΤΗ ΠΡΟΒΟΛΗ */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 5px !important;
        margin-top: 15px !important;
    }

    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }

    div.stButton > button {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3.8rem !important;
        font-weight: bold !important;
        font-size: 11px !important;
        width: 100% !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ΛΟΓΙΚΗ ---
ROT_POSITIONS = [1, 6, 5, 4, 3, 2]

def get_mapping(p, a1, k2, d, a2, k1, setter_pos):
    roster = [p, k1, a2, d, k2, a1]
    shift = ROT_POSITIONS.index(setter_pos)
    rotated_roster = roster[-shift:] + roster[:-shift]
    return {ROT_POSITIONS[i]: rotated_roster[i] for i in range(6)}

def get_next_pos(current_pos, step):
    idx = ROT_POSITIONS.index(current_pos)
    return ROT_POSITIONS[(idx + step) % 6]

if 'active' not in st.session_state: st.session_state.active = False

# --- UI ΕΝΑΡΞΗΣ ---
if not st.session_state.active:
    st.markdown("<h2 style='text-align: center; color: white;'>🏐 Tactical Setup</h2>", unsafe_allow_html=True)
    with st.form("setup"):
        side = st.radio("Σερβίς:", ["Ολυμπιακός", "Αντίπαλος"], horizontal=True)
        opp_s_pos = st.slider("Πασαδόρος Αντιπάλου", 1, 6, 1)
        st.divider()
        l, r = st.columns(2)
        with l:
            st.subheader("🔴 OLY")
            op = st.number_input("Π", value=19); ok1 = st.number_input("Κ1", value=22)
            oa1 = st.number_input("Α1", value=8); oa2 = st.number_input("Α2", value=7)
            ok2 = st.number_input("Κ2", value=21); od = st.number_input("Δ", value=14)
            mt = st.selectbox("Στόχος OLY", [op, oa1, ok2, od, oa2, ok1], index=1)
        with r:
            st.subheader("🚀 ANT")
            ap = st.number_input("Π Αντ.", value=31); aa1 = st.number_input("Α1 Αντ.", value=77)
            ak2 = st.number_input("Κ2 Αντ.", value=12); ad = st.number_input("Δ Αντ.", value=8)
            aa2 = st.number_input("Α2 Αντ.", value=7); ak1 = st.number_input("Κ1 Αντ.", value=6)
            at = st.selectbox("Στόχος ANT", [ap, aa1, ak2, ad, aa2, ak1], index=1)
        if st.form_submit_button("✅ ΕΝΑΡΞΗ"):
            st.session_state.active = True
            st.session_state.oly_p = 1
            st.session_state.opp_p = opp_s_pos
            st.session_state.data = (op, oa1, ok2, od, oa2, ok1, mt, ap, aa1, ak2, ad, aa2, ak1, at)
            st.rerun()

else:
    # --- UI ΑΝΑΛΥΣΗΣ ---
    op, oa1, ok2, od, oa2, ok1, mt, ap, aa1, ak2, ad, aa2, ak1, at = st.session_state.data
    map_opp = get_mapping(ap, aa1, ak2, ad, aa2, ak1, st.session_state.opp_p)
    map_oly = get_mapping(op, oa1, ok2, od, oa2, ok1, st.session_state.oly_p)

    st.markdown('<div class="tactical-wrapper">', unsafe_allow_html=True)
    
    # Αντίπαλος
    st.markdown(f'<div class="court-title" style="background-color: #2980B9;">ΑΝΤΙΠΑΛΟΣ: Π στο {st.session_state.opp_p}</div>', unsafe_allow_html=True)
    opp_html = '<div class="grid-layout">'
    for p in [1, 6, 5, 2, 3, 4]:
        val = map_opp[p]; cls = "player-cell opp-court-cell"
        if val == at: cls += " highlight-target"
        elif val == ap: cls += " highlight-setter"
        opp_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(opp_html + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="net-divider"></div>', unsafe_allow_html=True)

    # Ολυμπιακός
    st.markdown(f'<div class="court-title" style="background-color: #C0392B;">ΟΛΥΜΠΙΑΚΟΣ: Π στο {st.session_state.oly_p}</div>', unsafe_allow_html=True)
    oly_html = '<div class="grid-layout">'
    for p in [4, 3, 2, 5, 6, 1]:
        val = map_oly[p]; cls = "player-cell oly-court-cell"
        if val == mt: cls += " highlight-target"
        elif val == op: cls += " highlight-setter"
        oly_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(oly_html + '</div>', unsafe_allow_html=True)

    # Κουμπιά (Responsive & Hard-Locked)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Περιστρ. (-)", key="rot_minus"):
            st.session_state.oly_p = get_next_pos(st.session_state.oly_p, -1)
            st.session_state.opp_p = get_next_pos(st.session_state.opp_p, -1)
            st.rerun()
    with c2:
        if st.button("Νέα Εργασία", key="new_task"):
            st.session_state.active = False
            st.rerun()
    with c3:
        if st.button("Περιστρ. (+)", key="rot_plus"):
            st.session_state.oly_p = get_next_pos(st.session_state.oly_p, 1)
            st.session_state.opp_p = get_next_pos(st.session_state.opp_p, 1)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
