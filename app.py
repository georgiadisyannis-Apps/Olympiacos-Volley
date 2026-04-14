import streamlit as st

st.set_page_config(page_title="Volley Tactical Pro v56", layout="centered")

# --- CSS για Dual Orientation (Portrait & Landscape) ---
st.markdown("""
<style>
    /* Γενικό Layout που προσαρμόζεται στο πλάτος */
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100% !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Το wrapper ακολουθεί το πλάτος της συσκευής */
    .tactical-wrapper {
        width: 100%;
        max-width: 500px; /* Μέγιστο πλάτος για να μην "απλώνει" υπερβολικά σε tablet */
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .court-title {
        width: 100%;
        text-align: center;
        font-weight: bold;
        padding: 10px 0;
        color: white;
        font-size: clamp(12px, 4vw, 16px); /* Δυναμικό μέγεθος γραμματοσειράς */
        border-radius: 8px 8px 0 0;
        text-transform: uppercase;
    }

    .grid-layout {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1vw;
        padding: 2vw;
        width: 100%;
        box-sizing: border-box;
        border: 4px solid #333;
        background-color: #f4f4f4;
    }

    .player-cell {
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: clamp(18px, 6vw, 28px);
        border-radius: 6px;
        border: 1px solid rgba(0,0,0,0.1);
        position: relative;
        aspect-ratio: 1.2 / 1;
    }

    .label-p { position: absolute; top: 2px; left: 4px; font-size: clamp(8px, 2vw, 10px); opacity: 0.7; }

    .net-divider {
        width: 100%;
        height: 20px;
        background-color: #222;
        background-image: linear-gradient(45deg, #444 25%, transparent 25%, transparent 50%, #444 50%, #444 75%, transparent 75%, transparent);
        background-size: 8px 8px;
        margin: 10px 0;
        border: 1px solid #000;
    }

    .opp-court { background-color: #5DADE2 !important; color: #1B2631 !important; }
    .oly-court { background-color: #C0392B !important; color: #FFFFFF !important; }

    .highlight-target { background-color: #F1C40F !important; color: #000 !important; border: 2px solid #333; }
    .highlight-setter { background-color: #E67E22 !important; color: #fff !important; border: 2px solid #D35400; }

    /* --- ΔΥΝΑΜΙΚΑ ΚΟΥΜΠΙΑ ΓΙΑ ΟΡΙΖΟΝΤΙΑ/ΚΑΘΕΤΗ ΠΡΟΒΟΛΗ --- */
    [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 500px !important;
        gap: 8px !important;
        margin: 15px auto !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }

    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0 !important;
    }

    div.stButton > button {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
        height: clamp(3rem, 10vw, 4rem) !important;
        font-weight: bold !important;
        font-size: clamp(10px, 3vw, 14px) !important;
        width: 100% !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
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

# --- UI ---
if not st.session_state.active:
    st.markdown("<h2 style='text-align: center;'>🏐 Tactical Setup</h2>", unsafe_allow_html=True)
    with st.form("setup"):
        c1, c2 = st.columns(2)
        side = c1.radio("Σερβίς:", ["Ολυμπιακός", "Αντίπαλος"], horizontal=True)
        opp_s_pos = c2.slider("Πασαδόρος Αντιπάλου", 1, 6, 1)
        st.divider()
        l, r = st.columns(2)
        with l:
            st.subheader("🔴 OLY")
            op = st.number_input("Π", value=19); oa1 = st.number_input("Α1", value=8)
            ok2 = st.number_input("Κ2", value=21); od = st.number_input("Δ", value=14)
            oa2 = st.number_input("Α2", value=7); ok1 = st.number_input("Κ1", value=22)
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
    op, oa1, ok2, od, oa2, ok1, mt, ap, aa1, ak2, ad, aa2, ak1, at = st.session_state.data
    map_opp = get_mapping(ap, aa1, ak2, ad, aa2, ak1, st.session_state.opp_p)
    map_oly = get_mapping(op, oa1, ok2, od, oa2, ok1, st.session_state.oly_p)

    st.markdown('<div class="tactical-wrapper">', unsafe_allow_html=True)
    
    # Αντίπαλος
    st.markdown(f'<div class="court-title" style="background-color: #1F618D;">ΑΝΤΙΠΑΛΟΣ: Π στο {st.session_state.opp_p}</div>', unsafe_allow_html=True)
    opp_html = '<div class="grid-layout opp-court">'
    for p in [1, 6, 5, 2, 3, 4]:
        val = map_opp[p]; cls = "player-cell"
        if val == at: cls += " highlight-target"
        elif val == ap: cls += " highlight-setter"
        opp_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(opp_html + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="net-divider"></div>', unsafe_allow_html=True)

    # Ολυμπιακός
    st.markdown(f'<div class="court-title" style="background-color: #943126;">ΟΛΥΜΠΙΑΚΟΣ: Π στο {st.session_state.oly_p}</div>', unsafe_allow_html=True)
    oly_html = '<div class="grid-layout oly-court">'
    for p in [4, 3, 2, 5, 6, 1]:
        val = map_oly[p]; cls = "player-cell"
        if val == mt: cls += " highlight-target"
        elif val == op: cls += " highlight-setter"
        oly_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(oly_html + '</div>', unsafe_allow_html=True)

    # Responsive Buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Περιστρ. (-)"):
            st.session_state.oly_p = get_next_pos(st.session_state.oly_p, -1)
            st.session_state.opp_p = get_next_pos(st.session_state.opp_p, -1)
            st.rerun()
    with c2:
        if st.button("Νέα Εργασία"):
            st.session_state.active = False
            st.rerun()
    with c3:
        if st.button("Περιστρ. (+)"):
            st.session_state.oly_p = get_next_pos(st.session_state.oly_p, 1)
            st.session_state.opp_p = get_next_pos(st.session_state.opp_p, 1)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
