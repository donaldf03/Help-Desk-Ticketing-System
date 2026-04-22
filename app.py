import streamlit as st
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="Help Desk System", page_icon="🛠️")
st.title("🛠️ Simple Help Desk Ticket System")

# CREATE STORAGE (keeps tickets)
if "tickets" not in st.session_state:
    st.session_state.tickets = pd.DataFrame(columns=[
        "ID", "Issue", "Priority", "Status", "Assigned To", "Date"
    ])

# FUNCTION TO MAKE NEW ID
def make_ticket_id():
    return f"TICKET-{len(st.session_state.tickets) + 1}"

# TABS (like your workflow)
tab1, tab2 = st.tabs(["Submit Ticket", "Manage Tickets"])

# TAB 1 - SUBMIT TICKET
with tab1:
    st.subheader("Submit a Ticket")

    issue = st.text_area("Describe your problem")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Submit Ticket"):
        new_ticket = {
            "ID": make_ticket_id(),
            "Issue": issue,
            "Priority": priority,
            "Status": "Open",
            "Assigned To": "Not Assigned",
            "Date": datetime.now().strftime("%m-%d-%Y")
        }

        st.session_state.tickets = pd.concat(
            [st.session_state.tickets, pd.DataFrame([new_ticket])],
            ignore_index=True
        )

        st.success("Ticket submitted!")

# TAB 2 - TECHNICIAN VIEW
with tab2:
    st.subheader("Manage Tickets")

    if len(st.session_state.tickets) == 0:
        st.warning("No tickets yet")
    else:
        edited = st.data_editor(
            st.session_state.tickets,
            use_container_width=True
        )

        # Save changes
        if st.button("Save Updates"):
            st.session_state.tickets = edited
            st.success("Updated!")

        # SIMPLE DASHBOARD
        st.subheader("Dashboard")

        open_count = len(edited[edited["Status"] == "Open"])
        progress_count = len(edited[edited["Status"] == "In Progress"])
        closed_count = len(edited[edited["Status"] == "Closed"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Open", open_count)
        col2.metric("In Progress", progress_count)
        col3.metric("Closed", closed_count)
