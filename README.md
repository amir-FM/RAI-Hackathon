# AI Financial Advisor

An intelligent, Streamlit-based web application that acts as your personal financial assistant. It ingests your bank transactions, categorizes your spending using Large Language Models (LLMs), visualizes your financial habits, and provides actionable advice for saving and investing.

<img width="2307" height="1573" alt="Financial Advisor_page-0001" src="https://github.com/user-attachments/assets/5e4381ea-ac90-4db1-b977-e0b066e02637" />

## Features

Based on the core agent logic, the chatbot supports the following capabilities:

* **Transaction Categorization:** Automatically parses an `input.json` file of bank transactions and classifies them into categories like Healthcare, Education, Food, Bills, and Entertainment.


* **Financial Question Answering:** Capable of answering general financial questions (and rejecting non-financial ones).


* **Spending Analytics & Visualization:** Generates interactive Plotly pie charts to show exactly where your monthly income goes.


* **Goal Planning:** Looks up the average price of a desired item and calculates how many days, months, or years it will take to afford it based on your current surplus funds.


* **Budget Adjustments:** Allows you to specify a timeframe for a purchase (e.g., "I want to buy the bag in 4 years") and calculates exactly which spending categories you need to cut (and by how much) to meet that goal.


* **Investment Recommendations:** Suggests safe economy funds (e.g., government/treasury bonds, Raiffeisen Romania savings accounts) based on your monthly savings.



## Prerequisites

* **Python:** 3.8 or higher.
* **OpenAI API Key:** Required for the LLM routing and classification logic.



## Installation

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies:**
```bash
pip install streamlit plotly streamlit-lightweight-charts llama-index python-dotenv openai

```


3. **Prepare your data:** Ensure you have an `input.json` file in the root directory structured with your bank transactions and total salary data.


4. **Set up environment variables:** Create a `.env` file in the root directory and add your API key:


```env
OPENAI_API_KEY=your_api_key_here

```



## Project Structure

* **`website.py`**: The Streamlit frontend. It renders the sidebar (showing income, expenses, and surplus), manages the chat interface, and handles message streaming.


* **`main.py`**: The backend logic. Contains the `Agents` class for LLM API calls and prompt routing, and the `Main` class for data manipulation and chart generation.


* **`Spendings.py`**: A helper class (imported in `main.py`) that manages the mathematical tracking of category totals and percentages.


* **`input.json`**: The data source containing transaction history and salary information.



## Usage

Run the Streamlit application from your terminal:

```bash
streamlit run website.py

```

Once the application launches in your browser, you can use prompts like:

* *"Get my monthly spendings"* (to generate the pie chart)
* *"I want to buy a dior saddlebag"* (to get a price and timeline estimate)
* *"I want to buy the bag in 4 years"* (to get an adjusted budget plan)
