import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime

from card import Card

st.set_page_config(
    page_title="Leitner System",
    page_icon=":book:",
)

x = st.button("Reset")
if x:
    del st.session_state["cards"]

if "cards" not in st.session_state:
    st.session_state["cards"] = [Card("When was the Battle of Hastings?", "1066")]

for card in st.session_state["cards"]:
    if card.due_date.date() <= datetime.now().date():
        components.html(card.render(), height=300)