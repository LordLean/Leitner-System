import streamlit as st

import sys
sys.path.append('..')

from card import Card

with st.form("form_submit"):
    question = st.text_input("Question")
    answer = st.text_input("Answer")

    submitted = st.form_submit_button("Submit Card")

if submitted:
    if not len(question) or not len(answer):
        st.warning("Empty strings are not permitted")
        st.stop()
    card = Card(question, answer)
    st.session_state["cards"].append(card)