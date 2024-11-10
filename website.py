#!/usr/bin/env python3

import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
import main as lama
import os
from dotenv import load_dotenv

load_dotenv()

if 'ok' not in st.session_state:
    st.session_state.ok = 0
if 'bots' not in st.session_state:
    st.session_state.bots = lama.Main()

#     # Display the interactive pie chart
#     st.plotly_chart(fig)




logging.basicConfig(level=logging.INFO)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def stream_chat(model, messages):
    try:
        # llm = Ollama(model=model, request_timeout=120.0)
        resp = st.session_state.bots.run(messages[-1])
        response = ""
        response_placeholder = st.empty()
        response = resp
        response_placeholder.write(response)
        # chart()
        st.session_state.bots.percentageParser()
        # for r in resp:
        #     print(r)
        #     response += r#.delta
        #     response_placeholder.write(response)
        # logging.info(f"Model: {model}, Messages: {messages}, Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        raise e

def main():
    logging.info("App started")

    st.markdown(
    """
    <style>
    .st-emotion-cache-6qob1r{

        background-color: white;  /* Change this to your desired color */
    }
    .st-emotion-cache-1dp5vir{
        background-color: yellow;
        background-image: none;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.sidebar.image("logo.svg")
    model = st.sidebar.selectbox("Choose a model", ["mymodel", "llama3.2", "phi3", "mistral"])
    logging.info(f"Model selected: {model}")


    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User input: {prompt}")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                start_time = time.time()
                logging.info("Generating response")

                with st.spinner("Writing..."):
                    try:
                        messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
                        response_message = stream_chat(model, messages)
                        duration = time.time() - start_time
                        response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
                        st.session_state.messages.append({"role": "assistant", "content": response_message_with_duration})
                        st.write(f"Duration: {duration:.2f} seconds")
                        logging.info(f"Response: {response_message}, Duration: {duration:.2f} s")

                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": str(e)})
                        st.error("An error occurred while generating the response.")
                        logging.error(f"Error: {str(e)}")


if __name__ == "__main__":
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n\n\n\n")
    if st.session_state.ok == 0:
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n\n\n\n\n")
        st.session_state.bots.initCategs()
        st.session_state.ok = 1
    main()
