#!/usr/bin/env python3

import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
# from main import *

def chart():
    labels = ['laptop', 'pahare', 'fifa', 'gantere', 'banane', 'mouse', 'masina', 'haine', 'spritz']
    values = [10, 10, 10, 10, 10, 10, 10, 10, 20]

    # Different shades of yellow for the pie chart
    yellow_shades = [
        "#FFFFE0",  # Light Yellow
        "#FFF700",  # Lemon Yellow
        "#FFD700",  # Gold
        "#FFAE42",  # Yellow Orange
        "#FFEF00",  # Canary Yellow
        "#F8D700",  # Daffodil Yellow
        "#DAA520",  # Goldenrod
        "#FAFAD2",  # Light Goldenrod Yellow
        "#FFDD00"   # Bright Yellow
    ]

    # Creating a Plotly pie chart with different shades of yellow
    fig = px.pie(
        names=labels,
        values=values,
        title='Fruit Distribution',
        color_discrete_sequence=yellow_shades,  # Apply the yellow shades
        hole=0.3  # To create a donut chart, set this between 0 and 1
    )

    # Update layout for legend and font style
    fig.update_layout(
        legend=dict(
            font=dict(
                family="yellow",  # You can change the font family here
                size=18,  # Set the font size
                color="white"  # Set the font color if needed
            ),
            title="Spendings",  # You can also set a title for the legend
            title_font=dict(
                size=20,  # Font size of the legend title
                family="yellow",  # Font family for the legend title
            )
        )
    )

    # Display the interactive pie chart
    st.plotly_chart(fig)




logging.basicConfig(level=logging.INFO)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def stream_chat(model, messages):
    try:
        # llm = Ollama(model=model, request_timeout=120.0)
        resp = ""#categorise()#llm.stream_chat(messages)
        response = ""
        response_placeholder = st.empty()
        response = resp
        response_placeholder.write(response)
        chart()
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
    st.title("Your money is lazy, let's put it to work")
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
    main()
