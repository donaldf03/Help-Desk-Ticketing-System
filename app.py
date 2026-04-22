import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page setup
st.set_page_config(page_title="Help Desk System", page_icon="🛠️")
st.title("🛠️ Simple Help Desk Ticket System")

# FILE STORAGE
FILE = "tickets.csv"

# LOAD DATA
if os.path.exists(FILE):
    tickets_df = pd.read_csv(FILE)
else:
    tickets_df = pd.DataFrame(columns=[
        "ID", "Issue", "Priority", "Status", "Assigned To", "Date"
    ])

# SESSION STATE
if "tickets" not in st.session_state:
    st.session_state.tickets = tickets_df


# MAKE TICKET ID (always increments correctly)
def make_ticket_id():
    if st.session_state.tickets.empty:
        return "TICKET-1"

    ids = st.session_state.tickets["ID"].astype(str)
    nums = ids.str.extract(r"(\d+)")[0].astype(float)

    next_id = int(nums.max() + 1) if not nums.isna().all() else 1
    return f"TICKET-{next_id}"


# TABS
tab1, tab2 = st.tabs(["Submit Ticket", "Manage Tickets"])

# TAB 1 - SUBMIT
with tab1:
    st.subheader("Submit a Ticket")

    issue = st.text_area("Describe your problem")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Submit Ticket"):
        if issue.strip() == "":
            st.error("Please enter an issue description")
        else:
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

            # SAVE
            st.session_state.tickets.to_csv(FILE, index=False)

            st.success("Ticket submitted!")


# TAB 2 - MANAGE
with tab2:
    st.subheader("Manage Tickets")

    if st.session_state.tickets.empty:
        st.warning("No tickets yet")
    else:
        edited = st.data_editor(
            st.session_state.tickets,
            use_container_width=True
        )

        if st.button("Save Updates"):
            st.session_state.tickets = edited
            st.session_state.tickets.to_csv(FILE, index=False)
            st.success("Updated!")

        # DASHBOARD
        st.subheader("Dashboard")

        open_count = len(edited[edited["Status"] == "Open"])
        progress_count = len(edited[edited["Status"] == "In Progress"])
        closed_count = len(edited[edited["Status"] == "Closed"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Open", open_count)
        col2.metric("In Progress", progress_count)
        col3.metric("Closed", closed_count)
