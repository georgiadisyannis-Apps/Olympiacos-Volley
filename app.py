import streamlit as st

# Ρύθμιση για αυτόματη προσαρμογή σε browsers συσκευών
st.set_page_config(page_title="Volley Tactical Board", layout="centered")

# --- CSS για Απόλυτη Συμβατότητα (PC, Tablet, Mobile) ---
st.markdown("""
<style>
    /* Κεντράρισμα του κεντρικού container του Streamlit */
    .stApp {
        display: flex;
        justify-content: center;
    }
    
    .block-container {
        max-width: 380px !important; /* Ιδανικό πλάτος για κινητά */
        padding-left: 10px !important;
        padding-right: 10px !important;
        margin: 0 auto;
    }

    /* Σύστημα Γηπέδων */
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
        margin: 0;
    }

    .grid-layout {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 3 ίσες στήλες που προσαρμόζονται */
        gap: 6px;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
        border: 4px solid #333;
        background-color: #f8f8f8;
    }

    .player-cell {
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 22px;
        border-radius: 6px;
        border: 1px solid rgba(0,0,0,0.1);
        position: relative;
        aspect-ratio: 1 / 0.8; /* Διατηρεί το σωστό σχήμα σε κάθε οθόνη */
    }

    .label-p { 
        position: absolute; 
        top: 2px; 
        left: 4px; 
        font-size: 9px; 
        opacity: 0.8; 
    }

    .net-divider {
        width: 100%;
        height: 20px;
        background-color: #222;
        background-image: linear-gradient(45deg, #444 25%, transparent 25%, transparent 50%, #444 50%, #444 75%, transparent 75%, transparent);
        background-size: 8px 8px;
        border: 2px solid #000;
        margin: 10px 0;
    }

    /* Χρώματα Ομάδων */
    .opp-court { background-color: #5DADE2 !important; color: #1B2631 !important; }
    .oly-court { background-color: #C0392B !important; color: #FFFFFF !important; }

    /* Highlights */
    .highlight-target { background-color: #F1C40F !important; color: #000 !important; border: 2px solid #333; }
    .highlight-setter { background-color: #E67E22 !important; color: #fff !important; border: 2px solid #D35400; }

    /* --- MOBILE BUTTONS FIX --- */
    /* Εμποδίζουμε το "σπάσιμο" των κουμπιών σε κινητά */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 5px !important;
        margin-top: 15px !important;
    }

    [data-testid="column"] {
        width: 33.33% !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    div.stButton > button {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3.5rem !important;
        font-weight: bold !important;
        font-size: 11px !important;
        width: 100% !important;
        border: none !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ΛΟΓΙΚΗ ΠΑΙΧΝΙΔΙΟΥ ---
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

# --- ΣΕΛΙΔΑ 1: SETUP (Responsive Form) ---
if not st.session_state.active:
    st.markdown("<h2 style='text-align: center;'>🏐 Tactical Setup</h2>", unsafe_allow_html=True)
    with st.form("setup_form"):
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
    # --- ΣΕΛΙΔΑ 2: ANALYSIS (Responsive Court) ---
    op, oa1, ok2, od, oa2, ok1, mt, ap, aa1, ak2, ad, aa2, ak1, at = st.session_state.data
    map_opp = get_mapping(ap, aa1, ak2, ad, aa2, ak1, st.session_state.opp_p)
    map_oly = get_mapping(op, oa1, ok2, od, oa2, ok1, st.session_state.oly_p)

    st.markdown('<div class="tactical-wrapper">', unsafe_allow_html=True)
    
    # Γήπεδο Αντιπάλου
    st.markdown(f'<div class="court-title" style="background-color: #1F618D;">ΑΝΤΙΠΑΛΟΣ: Π στο {st.session_state.opp_p}</div>', unsafe_allow_html=True)
    opp_html = '<div class="grid-layout opp-court">'
    for p in [1, 6, 5, 2, 3, 4]:
        val = map_opp[p]; cls = "player-cell"
        if val == at: cls += " highlight-target"
        elif val == ap: cls += " highlight-setter"
        opp_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(opp_html + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="net-divider"></div>', unsafe_allow_html=True)

    # Γήπεδο Ολυμπιακού
    st.markdown(f'<div class="court-title" style="background-color: #943126;">ΟΛΥΜΠΙΑΚΟΣ: Π στο {st.session_state.oly_p}</div>', unsafe_allow_html=True)
    oly_html = '<div class="grid-layout oly-court">'
    for p in [4, 3, 2, 5, 6, 1]:
        val = map_oly[p]; cls = "player-cell"
        if val == mt: cls += " highlight-target"
        elif val == op: cls += " highlight-setter"
        oly_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(oly_html + '</div>', unsafe_allow_html=True)

    # Μπάρα Κουμπιών
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