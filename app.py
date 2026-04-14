import streamlit as st

st.set_page_config(page_title="Volley Tactical Database v61", layout="centered")

# --- CSS v61: Pro UI & Responsive Design ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .block-container { max-width: 400px !important; padding: 1rem 0.5rem !important; margin: 0 auto; }
    
    .database-card {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 15px;
    }

    .court-title {
        width: 100%; text-align: center; font-weight: bold; padding: 12px 0;
        color: white; font-size: 14px; border-radius: 10px 10px 0 0;
        text-transform: uppercase; letter-spacing: 1px;
    }

    .grid-layout {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
        padding: 10px; width: 100%; box-sizing: border-box;
        border: 4px solid #333; background-color: #1a1a1a;
    }

    .player-cell {
        display: flex; justify-content: center; align-items: center;
        font-weight: bold; font-size: 24px; border-radius: 6px;
        position: relative; aspect-ratio: 1.1 / 1;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .label-p { position: absolute; top: 3px; left: 5px; font-size: 9px; color: rgba(255,255,255,0.6); }
    .opp-court-cell { background-color: #3498DB !important; color: white !important; }
    .oly-court-cell { background-color: #C0392B !important; color: white !important; }
    .highlight-target { background-color: #F1C40F !important; color: #000 !important; border: 2px solid #333 !important; }
    .highlight-setter { background-color: #E67E22 !important; color: #fff !important; border: 2px solid #D35400 !important; }

    .net-divider {
        width: 100%; height: 22px; background-color: #333;
        margin: 12px 0; border: 2px solid #000;
    }

    /* Κουμπιά σε σειρά για κινητά */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; width: 100% !important;
        gap: 5px !important; margin-top: 15px !important;
    }
    div[data-testid="column"] { flex: 1 1 0% !important; min-width: 0 !important; }
    div.stButton > button {
        background-color: #1E88E5 !important; color: white !important;
        border-radius: 8px !important; height: 3.5rem !important;
        font-weight: bold !important; font-size: 11px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'teams_db' not in st.session_state:
    # Προεπιλεγμένες ομάδες για ευκολία
    st.session_state.teams_db = {
        "Ολυμπιακός": [19, 8, 21, 14, 7, 22],
        "Αντίπαλος": [31, 77, 12, 8, 7, 6]
    }
if 'page' not in st.session_state: st.session_state.page = "database"

# --- LOGIC FUNCTIONS ---
ROT_POSITIONS = [1, 6, 5, 4, 3, 2]

def get_mapping(roster, setter_pos):
    # roster: [P, A1, K2, D, A2, K1]
    shift = ROT_POSITIONS.index(setter_pos)
    rotated_roster = roster[-shift:] + roster[:-shift]
    return {ROT_POSITIONS[i]: rotated_roster[i] for i in range(6)}

def get_next_pos(current_pos, step):
    idx = ROT_POSITIONS.index(current_pos)
    return ROT_POSITIONS[(idx + step) % 6]

# --- PAGE 1: TEAM DATABASE & MATCHUP SELECTION ---
if st.session_state.page == "database":
    st.markdown("<h2 style='text-align: center; color: white;'>📂 Διαχείριση Ομάδων</h2>", unsafe_allow_html=True)
    
    # 1. Προσθήκη Νέας Ομάδας
    with st.expander("➕ Προσθήκη Νέας Ομάδας"):
        new_name = st.text_input("Όνομα Ομάδας")
        c1, c2 = st.columns(2)
        p = c1.number_input("Πασαδόρος (Π)", value=0)
        a1 = c1.number_input("Ακραίος 1 (Α1)", value=0)
        k2 = c1.number_input("Κεντρικός 2 (Κ2)", value=0)
        d = c2.number_input("Διαγώνιος (Δ)", value=0)
        a2 = c2.number_input("Ακραίος 2 (Α2)", value=0)
        k1 = c2.number_input("Κεντρικός 1 (Κ1)", value=0)
        
        if st.button("Αποθήκευση Ομάδας"):
            if new_name:
                st.session_state.teams_db[new_name] = [p, a1, k2, d, a2, k1]
                st.success(f"Η ομάδα {new_name} αποθηκεύτηκε!")
                st.rerun()

    st.divider()

    # 2. Επιλογή Match-up
    st.markdown("### ⚔️ Επιλογή Match-up")
    if len(st.session_state.teams_db) >= 2:
        team_a_name = st.selectbox("Επιλογή Ομάδας (Κάτω Γήπεδο)", list(st.session_state.teams_db.keys()), index=0)
        team_b_name = st.selectbox("Επιλογή Αντιπάλου (Πάνω Γήπεδο)", list(st.session_state.teams_db.keys()), index=1)
        
        st.divider()
        
        # Ρυθμίσεις Σερβίς/Πασαδόρου
        c_setup1, c_setup2 = st.columns(2)
        side = c_setup1.radio("Σερβίς:", [team_a_name, team_b_name], horizontal=True)
        opp_s_pos = c_setup2.slider(f"Θέση Πασαδόρου {team_b_name}", 1, 6, 1)

        # Επιλογή Στόχων
        target_a = st.selectbox(f"Στόχος {team_a_name}", st.session_state.teams_db[team_a_name])
        target_b = st.selectbox(f"Στόχος {team_b_name}", st.session_state.teams_db[team_b_name])

        if st.button("🚀 ΕΝΑΡΞΗ ΑΝΑΛΥΣΗΣ", use_container_width=True):
            st.session_state.match_data = {
                "team_a_name": team_a_name, "team_a_roster": st.session_state.teams_db[team_a_name],
                "team_b_name": team_b_name, "team_b_roster": st.session_state.teams_db[team_b_name],
                "target_a": target_a, "target_b": target_b,
                "opp_start_p": opp_s_pos
            }
            st.session_state.oly_p = 1
            st.session_state.opp_p = opp_s_pos
            st.session_state.page = "analysis"
            st.rerun()
    else:
        st.info("Προσθέστε τουλάχιστον 2 ομάδες για να ξεκινήσετε.")

# --- PAGE 2: ANALYSIS ---
elif st.session_state.page == "analysis":
    d = st.session_state.match_data
    map_opp = get_mapping(d["team_b_roster"], st.session_state.opp_p)
    map_oly = get_mapping(d["team_a_roster"], st.session_state.oly_p)

    st.markdown('<div class="tactical-wrapper">', unsafe_allow_html=True)
    
    # Αντίπαλος (Πάνω)
    st.markdown(f'<div class="court-title" style="background-color: #2980B9;">{d["team_b_name"]}: Π στο {st.session_state.opp_p}</div>', unsafe_allow_html=True)
    opp_html = '<div class="grid-layout">'
    for p in [1, 6, 5, 2, 3, 4]:
        val = map_opp[p]; cls = "player-cell opp-court-cell"
        if val == d["target_b"]: cls += " highlight-target"
        elif val == d["team_b_roster"][0]: cls += " highlight-setter"
        opp_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(opp_html + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="net-divider"></div>', unsafe_allow_html=True)

    # Ομάδα Α (Κάτω)
    st.markdown(f'<div class="court-title" style="background-color: #C0392B;">{d["team_a_name"]}: Π στο {st.session_state.oly_p}</div>', unsafe_allow_html=True)
    oly_html = '<div class="grid-layout">'
    for p in [4, 3, 2, 5, 6, 1]:
        val = map_oly[p]; cls = "player-cell oly-court-cell"
        if val == d["target_a"]: cls += " highlight-target"
        elif val == d["team_a_roster"][0]: cls += " highlight-setter"
        oly_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(oly_html + '</div>', unsafe_allow_html=True)

    # Controls
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Περιστρ. (-)"):
            st.session_state.oly_p = get_next_pos(st.session_state.oly_p, -1)
            st.session_state.opp_p = get_next_pos(st.session_state.opp_p, -1)
            st.rerun()
    with c2:
        if st.button("Πίσω"):
            st.session_state.page = "database"
            st.rerun()
    with c3:
        if st.button("Περιστρ. (+)"):
            st.session_state.oly_p = get_next_pos(st.session_state.oly_p, 1)
            st.session_state.opp_p = get_next_pos(st.session_state.opp_p, 1)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
