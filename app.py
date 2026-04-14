import streamlit as st

st.set_page_config(page_title="Volley Tactical Pro v63", layout="centered")

# --- CSS v63: UI για Διαχείριση & Κινητά ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .block-container { max-width: 400px !important; padding: 1rem 0.5rem !important; margin: 0 auto; }
    
    .team-card {
        background-color: #1a1a1a;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 10px;
    }

    .court-title {
        width: 100%; text-align: center; font-weight: bold; padding: 12px 0;
        color: white; font-size: 14px; border-radius: 10px 10px 0 0;
        text-transform: uppercase;
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

    .net-divider { width: 100%; height: 22px; background-color: #333; margin: 12px 0; border: 2px solid #000; }

    /* Buttons Row Fix */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; width: 100% !important;
        gap: 5px !important;
    }
    div[data-testid="column"] { flex: 1 1 0% !important; min-width: 0 !important; }
</style>
""", unsafe_allow_html=True)

# --- ΛΟΓΙΚΗ ---
ROT_POSITIONS = [1, 6, 5, 4, 3, 2]

def get_mapping(roster, setter_pos):
    shift = ROT_POSITIONS.index(setter_pos)
    rotated_roster = roster[-shift:] + roster[:-shift]
    return {ROT_POSITIONS[i]: rotated_roster[i] for i in range(6)}

def get_next_pos(current_pos, step):
    idx = ROT_POSITIONS.index(current_pos)
    return ROT_POSITIONS[(idx + step) % 6]

# --- SESSION STATE ---
if 'teams_db' not in st.session_state:
    st.session_state.teams_db = {
        "Ολυμπιακός": [19, 22, 7, 14, 21, 8],
        "Αντίπαλος": [31, 6, 7, 8, 12, 77]
    }
if 'page' not in st.session_state: st.session_state.page = "database"
if 'edit_team' not in st.session_state: st.session_state.edit_team = None

# --- PAGE 1: DATABASE & MANAGEMENT ---
if st.session_state.page == "database":
    st.markdown("<h2 style='text-align: center; color: white;'>📂 Διαχείριση Ομάδων</h2>", unsafe_allow_html=True)
    
    # Φόρμα Εισαγωγής/Επεξεργασίας
    with st.expander("📝 Φόρμα Ομάδας", expanded=st.session_state.edit_team is not None):
        default_name = st.session_state.edit_team if st.session_state.edit_team else ""
        default_vals = st.session_state.teams_db.get(default_name, [0,0,0,0,0,0])
        
        name = st.text_input("Όνομα Ομάδας", value=default_name)
        c1, c2 = st.columns(2)
        p = c1.number_input("Π (Πασαδόρος)", value=default_vals[0])
        k1 = c2.number_input("Κ1 (Κεντρικός)", value=default_vals[1])
        a2 = c1.number_input("Α2 (Ακραίος)", value=default_vals[2])
        d = c2.number_input("Δ (Διαγώνιος)", value=default_vals[3])
        k2 = c1.number_input("Κ2 (Κεντρικός)", value=default_vals[4])
        a1 = c2.number_input("Α1 (Ακραίος)", value=default_vals[5])
        
        btn_label = "Ενημέρωση Ομάδας" if st.session_state.edit_team else "Αποθήκευση Νέας Ομάδας"
        if st.button(btn_label, use_container_width=True):
            if name:
                st.session_state.teams_db[name] = [p, k1, a2, d, k2, a1]
                st.session_state.edit_team = None # Reset edit mode
                st.success(f"✅ Η ομάδα '{name}' αποθηκεύτηκε επιτυχώς!")
                st.rerun()

    # Λίστα Ομάδων με Διαγραφή/Επεξεργασία
    st.markdown("### 📋 Λίστα Ομάδων")
    for t_name in list(st.session_state.teams_db.keys()):
        with st.container():
            st.markdown(f"""<div class='team-card'><b>{t_name}</b><br><small>{st.session_state.teams_db[t_name]}</small></div>""", unsafe_allow_html=True)
            col_edit, col_del = st.columns(2)
            if col_edit.button(f"✏️ Edit", key=f"edit_{t_name}"):
                st.session_state.edit_team = t_name
                st.rerun()
            if col_del.button(f"🗑️ Delete", key=f"del_{t_name}"):
                del st.session_state.teams_db[t_name]
                st.rerun()

    st.divider()

    # Επιλογή για Αγώνα
    st.markdown("### ⚔️ Έναρξη Match-up")
    all_teams = list(st.session_state.teams_db.keys())
    if len(all_teams) >= 2:
        t_a = st.selectbox("Ομάδα (Κάτω)", all_teams, index=0)
        t_b = st.selectbox("Αντίπαλος (Πάνω)", all_teams, index=1)
        
        c_side, c_pos = st.columns(2)
        opp_s_pos = c_pos.slider(f"Π στο:", 1, 6, 1)
        
        target_a = st.selectbox(f"Στόχος {t_a}", st.session_state.teams_db[t_a])
        target_b = st.selectbox(f"Στόχος {t_b}", st.session_state.teams_db[t_b])

        if st.button("🚀 ΕΝΑΡΞΗ ΑΝΑΛΥΣΗΣ", use_container_width=True):
            st.session_state.match_data = {
                "t_a": t_a, "r_a": st.session_state.teams_db[t_a],
                "t_b": t_b, "r_b": st.session_state.teams_db[t_b],
                "target_a": target_a, "target_b": target_b
            }
            st.session_state.oly_p = 1
            st.session_state.opp_p = opp_s_pos
            st.session_state.page = "analysis"
            st.rerun()

# --- PAGE 2: ANALYSIS ---
elif st.session_state.page == "analysis":
    md = st.session_state.match_data
    map_opp = get_mapping(md["r_b"], st.session_state.opp_p)
    map_oly = get_mapping(md["r_a"], st.session_state.oly_p)

    st.markdown('<div class="tactical-wrapper">', unsafe_allow_html=True)
    
    # Top Court
    st.markdown(f'<div class="court-title" style="background-color: #2980B9;">{md["t_b"]}: Π στο {st.session_state.opp_p}</div>', unsafe_allow_html=True)
    opp_html = '<div class="grid-layout">'
    for p in [1, 6, 5, 2, 3, 4]:
        val = map_opp[p]; cls = "player-cell opp-court-cell"
        if val == md["target_b"]: cls += " highlight-target"
        elif val == md["r_b"][0]: cls += " highlight-setter"
        opp_html += f'<div class="{cls}"><span class="label-p">P{p}</span>{val}</div>'
    st.markdown(opp_html + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="net-divider"></div>', unsafe_allow_html=True)

    # Bottom Court
    st.markdown(f'<div class="court-title" style="background-color: #C0392B;">{md["t_a"]}: Π στο {st.session_state.oly_p}</div>', unsafe_allow_html=True)
    oly_html = '<div class="grid-layout">'
    for p in [4, 3, 2, 5, 6, 1]:
        val = map_oly[p]; cls = "player-cell oly-court-cell"
        if val == md["target_a"]: cls += " highlight-target"
        elif val == md["r_a"][0]: cls += " highlight-setter"
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
