import streamlit as st
import streamlit.components.v1 as components

for card in st.session_state["cards"]:
        components.html(card.render(input=False), height=300)



