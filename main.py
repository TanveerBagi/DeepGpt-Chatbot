import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide")

if "selected_personality" not in st.session_state:
    st.session_state.selected_personality = None

st.title('DeepGPT Chatbot')
st.subheader('How would you like your chatbot to behave today? Choose a personality!')
Personality_of_Chatbot = ""
col1, col2, col3, col4 = st.columns(4)

def set_personality(personality):
    st.session_state.selected_personality = personality

with col1:
    if st.button("Professional Assistant"):
        set_personality("Professional Assistant")
    if st.button("Casual Friend"):
        set_personality("Casual Friend")

with col2:
    if st.button("Sarcastic Bot"):
        set_personality("Sarcastic Bot")
    if st.button("Tech Expert"):
        set_personality("Tech Expert")

with col3:
    if st.button("Storyteller"):
        set_personality("Storyteller")
    if st.button("Old Wise Sage"):
        set_personality("Old Wise Sage")

with col4:
    if st.button("Pirate Mode"):
        set_personality("Pirate Mode")
    if st.button("Evil Villain"):
        set_personality("Evil Villain")

# Shows selected personality
if st.session_state.selected_personality:
    st.success(f"Personality selected: {st.session_state.selected_personality}")

text = st.text_input(('Type here:'))


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=st.secrets["API_KEY"],
)
response_text = ""
output_text = st.empty()

if text:
  st.markdown(f"**You:** {text}")

  response_text = ""
  output_text = st.empty()

  completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-r1:free",
    messages=[
      {"role": "system", "content": f"You are a {st.session_state.selected_personality}"},
      {"role": "user","content": text}
    ],
    stream = True
  )

  for chunk in completion:
      if chunk.choices[0].delta.content:  # avoids empty chunks
          response_text += chunk.choices[0].delta.content  # Append new content
          output_text.markdown(f"**DeepGPT:** {response_text}")
