import pandas as pd
import requests
import json
import streamlit as st
import secrets
from streamlit_chat import message as st_message

st.title("Expense Tracker Assistant")

st.markdown(
        """
         <style>
            div[role=radiogroup] label:first-of-type {
            visibility: hidden;
            height: 0px;
            }
         </style>
        """,
        unsafe_allow_html=True,
   )


if "history" not in st.session_state:
    st.session_state.history = []

def generate_session_id():
    return secrets.token_hex(16)

def get_bot_response(message):
    url = 'http://localhost:5005/webhooks/rest/webhook'
    payload = {"sender": "user", "message": message}
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def generate_response():

    if st.session_state.history != [] and "is_radio" in st.session_state.history[-1]:
        for key in st.session_state:
            if key.startswith("selected_option_"):
                option = st.session_state[key]
                if option == "default":
                    continue
                print(key, option)
                print("end")
                user_message = option
                break
    else:
        user_message = st.session_state.input_text
        
    bot_response = get_bot_response(user_message)
    st.session_state.history.append({"is_user": True, "message": user_message, "key" : generate_session_id()})
    for i in range(len(bot_response)):
        if "text" in bot_response[i]:
            message = bot_response[i]['text']
            st.session_state.history.append({"is_user": False, "message": message, "key" : generate_session_id()})
        if "buttons" in bot_response[i]:
            button_options = bot_response[i].get("buttons", [])
            options_list = [option["title"] for option in button_options]
            radio_session_id = generate_session_id()
            print("radio_session_id", radio_session_id)
            st.session_state.history.append({"is_user": False, "message": options_list, "key" : radio_session_id, "is_radio": True})
        if "image" in bot_response[i]:
            st.session_state.history.append({"is_user": False, "message": bot_response[i]["image"], "key" : generate_session_id(), "is_image": True})

for chat in st.session_state.history:
    if "is_radio" in chat:
        key = generate_session_id()
        st.radio("Select one of them", chat["message"], key=f"selected_option_{key}", on_change=generate_response)
    elif "is_image" in chat:
        data_file_path = chat["message"]
        df = pd.read_csv(data_file_path)
        x_axis_label = df.columns[0]
        st.bar_chart(df.set_index(x_axis_label))
    else:
        st_message(**chat)
st.text_input("Talk to the bot:", key="input_text", on_change=generate_response)

