import openai
import streamlit as st

# Use Streamlit's dark theme
st.markdown(
    """
    <style>
        body {
            color: #FFFFFF;
            background-color: #1E1E1E;
        }
        .stChatInput {
            color: #FFFFFF !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Jarvis")
openai.api_key = st.secrets["API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

try:
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant message in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate stream of response with milliseconds delay
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                # will provide lively writing
                stream=True,
            ):
                # get content in response
                full_response += response.choices[0].delta.get("content", "")
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

except openai.error.OpenAIError as e:
    st.error(f"OpenAI API Error: {e}")
