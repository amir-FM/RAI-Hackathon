#!/usr/bin/env python3

import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


logging.basicConfig(level=logging.INFO)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def stream_chat(model, messages):
    try:
        llm = Ollama(model=model, request_timeout=120.0)
        resp = llm.stream_chat(messages)
        response = ""
        response_placeholder = st.empty()
        for r in resp:
            response += r.delta
            response_placeholder.write(response)
        logging.info(f"Model: {model}, Messages: {messages}, Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        raise e

def main():
    st.title("Chat with LLMs Models")
    logging.info("App started")

    # Streamlit app title
    st.title("Pie Chart Example")

    st.title("Interactive Pie Chart Example")

    

    # Sample data
labels = ['laptop', 'pahare', 'fifa', 'gantere', 'banane', 'mouse', 'masina', 'haine', 'spritz']
values = [10, 10, 10, 10, 10, 10, 10, 10, 20]

# Different shades of yellow for the pie chart
other_colors = [
    "#FF6347",  # Tomato Red
    "#40E0D0",  # Turquoise
    "#8A2BE2",  # Blue Violet
    "#7FFF00",  # Chartreuse
    "#DC143C",  # Crimson
    "#00BFFF",  # Deep Sky Blue
    "#32CD32",  # Lime Green
    "#FFD700",  # Gold
    "#FF1493",  # Deep Pink
    "#00FF00"   # Lime
]

# Creating a Plotly pie chart with different shades of yellow
fig = px.pie(
    names=labels,
    values=values,
    title='Fruit Distribution',
    color_discrete_sequence=other_colors,  # Apply the yellow shades
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


    # Chat functionality
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

# Section for displaying the chart
st.subheader("Overlaid Series with Markers")

# Define the chart options
overlaidAreaSeriesOptions = {
    "height": 400,
    "rightPriceScale": {
        "scaleMargins": {
            "top": 0.5,
            "bottom": 0.5,
        },
        "mode": 2,
        "borderColor": 'rgba(197, 203, 206, 0.4)',
    },
    "timeScale": {
        "borderColor": 'rgba(197, 203, 206, 0.4)',
    },
    "layout": {
        "background": {
            "type": 'solid',
            "color": '#100841'
        },
        "textColor": '#ffffff',
    },
    "grid": {
        "vertLines": {
            "color": 'rgba(197, 203, 206, 0.4)',
            "style": 1,
        },
        "horzLines": {
            "color": 'rgba(197, 203, 206, 0.4)',
            "style": 1,
        }
    }
}

seriesOverlaidChart = [
    {
        "type": 'Area',
        "data": data.seriesMultipleChartArea01,
        "options": {
            "topColor": 'rgba(255, 192, 0, 0.7)',
            "bottomColor": 'rgba(255, 192, 0, 0.3)',
            "lineColor": 'rgba(255, 192, 0, 1)',
            "lineWidth": 2,
        },
        "markers": [
            {
                "time": '2019-04-08',
                "position": 'aboveBar',
                "color": 'rgba(255, 192, 0, 1)',
                "shape": 'arrowDown',
                "text": 'H',
                "size": 3
            },
            {
                "time": '2019-05-13',
                "position": 'belowBar',
                "color": 'rgba(255, 192, 0, 1)',
                "shape": 'arrowUp',
                "text": 'L',
                "size": 3
            },
        ]
    },
    {
        "type": 'Area',
        "data": data.seriesMultipleChartArea02,
        "options": {
            "topColor": 'rgba(67, 83, 254, 0.7)',
            "bottomColor": 'rgba(67, 83, 254, 0.3)',
            "lineColor": 'rgba(67, 83, 254, 1)',
            "lineWidth": 2,
        },
        "markers": [
            {
                "time": '2019-05-03',
                "position": 'aboveBar',
                "color": 'rgba(67, 83, 254, 1)',
                "shape": 'arrowDown',
                "text": 'PEAK',
                "size": 3
            },
        ]
    }
]

# Render the chart using Streamlit Lightweight Charts
renderLightweightCharts([{
    "chart": overlaidAreaSeriesOptions,
    "series": seriesOverlaidChart
}], 'overlaid')

if __name__ == "__main__":
    main()
