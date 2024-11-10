import json
from dataclasses import dataclass
from typing import List, Optional
from dotenv import load_dotenv
import os
import streamlit as st
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
import json
from dataclasses import dataclass
from typing import List, Optional
from llama_index.core.llms import ChatMessage

load_dotenv()



# Define data classes for the JSON structure
@dataclass
class Amount:
    amount: float
    currency: str

@dataclass
class Transaction:
    transactionId: str
    endToEndId: str
    mandateId: str
    bookingDate: str
    valueDate: str
    transactionAmount: Amount
    creditorName: str
    remittanceInformationUnstructured: str

@dataclass
class Transactions:
    booked: List[Transaction]
    viewAccount: Optional[str] = None  # Link to view account (optional)

@dataclass
class TotalSalary:
    amount: float
    currency: str

@dataclass
class User:
    totalSalary: TotalSalary
    transactions: Transactions

@dataclass
class Root:
    user: User

# Function to parse JSON from a file into data classes
def parse_json_from_file(file_path: str) -> Root:
    def convert_transaction(trans: dict) -> Transaction:
        return Transaction(
            transactionId=trans["transactionId"],
            endToEndId=trans["endToEndId"],
            mandateId=trans["mandateId"],
            bookingDate=trans["bookingDate"],
            valueDate=trans["valueDate"],
            transactionAmount=Amount(**trans["transactionAmount"]),
            creditorName=trans["creditorName"],
            remittanceInformationUnstructured=trans["remittanceInformationUnstructured"]
        )

    def convert_transactions(transactions: dict) -> Transactions:
        booked = [convert_transaction(trans) for trans in transactions["booked"]]
        viewAccount = transactions["_links"]["viewAccount"]["href"] if "_links" in transactions and "viewAccount" in transactions["_links"] else None
        return Transactions(booked=booked, viewAccount=viewAccount)

    # Read JSON data from the file
    with open(file_path, 'r') as file:
        json_obj = json.load(file)

    # Extract the user data and construct the Root object
    user_data = json_obj["user"]
    return Root(
        user=User(
            totalSalary=TotalSalary(**user_data["totalSalary"]),
            transactions=convert_transactions(user_data["transactions"])
        )
    )



import os
from openai import AzureOpenAI
import re
from Spendings import Spendings



class Agents:
# Path to your JSON file
    def __init__(self):

        self.file_path = 'input.json'

        # Parse the JSON file
        self.parsed_data = parse_json_from_file(self.file_path)

        self.client = AzureOpenAI(
        azure_endpoint = "https://rbro-openai-hackatlon.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview", # insert the provided endpoint here
        api_key = os.getenv("OPENAI_API_KEY"), # insert the provided api key here
        api_version="2024-08-01-preview"
        )


    def get_string_between_quotes(self, text):
        # Use regex to find content between single quotes
        match = re.search(r"'(.*?)'", text)
        if match:
            return match.group(1)  # Return the content between the quotes
        return None  # Return None if no match is found

    def classify_transaction(self, transaction_description, client):
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies transactions."},
                {"role": "user", "content": f"""Classify the following transaction into one
                of these categories: 'Healthcare', 'Education','FoodAndDrinks',
                'RestaurantsOrCoffeShops 'Shopping', 'Transport', 'Bills', 'Transfer',
                'Entertainment'.\n\nTransaction: {transaction_description}"""}
            ],
            max_tokens=400,
            temperature=0.2,
    )
        return response.choices[0].message.content


    def mockWhereCanISave(self):
        print("haiddeeeeeee")

    def Master(self, text_input):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": """You are a helpful assistant that will analyze
                a prompt from the user and compare it to the following options: 1. Get my monthly spendings/ finances (the user wants an analysys of his spending habbits)
                 , 3. I want to buy something / i have a material wish
                 4. None of the above., 5. I want to buy the object in "x" years, 6. I want to put my money in an economy account
                 Return just the prompt with the index included."""},
                {"role": "user", "content": f"""To which option does the prompt belong {text_input}"""}
            ],
            max_tokens=1000,
            temperature=0.2,
    )
        return response.choices[0].message.content


    def wishes(self, obiect):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": """You are a helpful assistant that searches for the medium price of an given object, paying attetion to the details given by the user."""},
                {"role": "user", "content": f"Give me just the medium price of {obiect}, one number in euros and the number should be like this: 1000.0"}
            ],
        max_tokens=400,
        temperature=0.2,
    )
        return response.choices[0].message.content


    def invest(self, advised_savings):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": """You are a helpful assistant that recommends saving accounts at Raiffaisen Romania or government bonds or treasury bonds Romania, displaying benefit."""},
                {"role": "user", "content": f"Give me the result of putting {advised_savings} every month for a year in saving accounts at Raiffaisen Romania or government bonds or treasury bonds Romania, display only final result and multiple options, also writing separtely benefit"}
            ],
        max_tokens=400,
        temperature=0.2,
)
        return response.choices[0].message.content



    def general(self, question):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": """You are a helpful assistant that can answer financial related questions.
                  if any other type of question is asked you must respond : "This question is out of my field of expertise" """},
                {"role": "user", "content": f"Answer this question: {question}"}
            ],
        max_tokens=400,
        temperature=0.2,
)
        return response.choices[0].message.content

    def timeUntillPurchase(self, needed, monthly_savings):
        if((needed /( 12 * monthly_savings)) < 1):
            if(needed / monthly_savings < 1):
                if(needed / 30 * monthly_savings < 1):
                    self.exists_object = False
                    return "Your wishist item does not need financial planning\n"
                return "{:.2f}".format(needed / 30 * monthly_savings) + " days"
            return "{:.2f}".format(needed / monthly_savings) + " months"
        return "{:.2f}".format(needed/(12 * monthly_savings)) + " years"
    # se poate expanda pe luni (telefoane )

    def timeUntillPurchase_floatRet(self, needed, monthly_savings):
        if((needed /( 12 * monthly_savings)) < 1):
            return (needed / monthly_savings)
        return needed/(12 * monthly_savings)

import streamlit as st
import plotly.express as px

class Main:
    def __init__(self):
        self.agents = Agents()
        self.price = 0
        self.cheltuieli = Spendings()
        self.exists_obiect = False

        self.cheltuieli.salary = self.agents.parsed_data.user.totalSalary.amount
        pass

    def chart(self, labels, values):
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


    # @staticmethod
    def initCategs(self):
        for tx in self.agents.parsed_data.user.transactions.booked:
                category = None
                while True:
                    category = self.agents.classify_transaction(tx.creditorName, self.agents.client)
                    if(self.agents.get_string_between_quotes(category) != None):
                        break
                print(f"Transaction: {tx.creditorName} -> Category: {self.agents.get_string_between_quotes(category)}")

                self.cheltuieli.add_to_field(self.agents.get_string_between_quotes(category), (float)(tx.transactionAmount.amount))
        self.cheltuieli.free = self.cheltuieli.salary - self.cheltuieli.totalSpent
        print("done categorizing")
        self.cheltuieli.update_percentages()
        print(self.cheltuieli.str())


    def percentageParser(self):
        field_names = [
            'Healthcare',
            'Education',
            'Food',
            'Restaurant',
            'Bills',
            'Entertainment',
            'Shopping',
            'Transport',
            'Free'
        ]

        # Create a list of corresponding values
        field_values = [
            self.cheltuieli.HealthcarePercentage,
            self.cheltuieli.EducationPercentage,
            self.cheltuieli.FoodAndDrinksPercentage,
            self.cheltuieli.RestaurantsOrCoffeShopsPercentage,
            self.cheltuieli.BillsPercentage,
            self.cheltuieli.EntertainmentPercentage,
            self.cheltuieli.ShoppingPercentage,
            self.cheltuieli.TransportPercentage,
            self.cheltuieli.freePercentage
        ]

        self.chart(field_names, field_values)
        return "piechart"

# print(percentagesParser(cheltuieli))

    # def


    def cutFromSpendings(self, cheltuieli_percentages, perc_total):
        response = self.agents.client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": """You are a helpful assistant that will analyze
                the spending habits of a person and based on them you will give advice on
                where they can cut spendings."""},
                {"role": "user", "content": f"""Where can
                the following user save another {perc_total} percent of his income. Give the output in the following format as a list from at least 2 elements:
                index.Field : percentage that can be saved in order to add to that percentage\n\Spendings: {cheltuieli_percentages}. DO NOT INCLUDE A TOTAL"""}
            ],
            max_tokens=1000,
            temperature=0.2,
    )
        return response.choices[0].message.content

    # print(whereCanISave(cheltuieli.percentages_str(), client))

    def run(self, input_text):
        print(input_text, type(input_text))
        # # input_text = input_text.__str__
        # input_text = input_text.content
        prompt = input_text
        option = self.agents.Master(prompt)
        print(option)

        if option[0] == "1":
            return self.percentageParser()
            pass
        # elif option[0] == "2":
        #     self.agents.mockWhereCanISave()
        elif option[0] == "3":
            output = self.agents.wishes(prompt)
            self.price = (float)(output)
            # print(output)
            # print(f"free = {self.cheltuieli.free}")
            self.exists_obiect = True
            return f"The price for the object is: {int(self.price)} euro. " + f"Given you current finance plan you will be able to afford it in {self.agents.timeUntillPurchase(self.price, self.cheltuieli.free)}"
            # print(self.price)

        elif option[0] == "4":
            # print("I could not make any sense of your input")
            return self.agents.general(input_text)
            pass
        elif option[0] == "5":
            try:
                if self.exists_obiect == False:
                    print("Plese reffer to an object that you want to buy")
                else:
                    match = re.search(r'\d+(?:\.\d+)?', input_text.content[1:])
                    print(option)
                    if match:
                        timp_vrut = float(match.group()) if '.' in match.group() else int(match.group())
                        print(timp_vrut)
                        print(self.cheltuieli.percentages_str())
                        print(f"cat de mai mult perc ne trb {self.getHowMuchMorePercentage(timp_vrut)}")
                        output = self.cutFromSpendings(self.cheltuieli.percentages_str(), self.getHowMuchMorePercentage(timp_vrut))
                        print("Given your current spending habbits you could cut these ")
                        print(output)

                        # print(self.format_cutting(output))
                        return str(f"Given your current spending habbits you could cut these\n\n" + str(self.format_cutting(output)))
                        # //return aici
            except:
                return self.run(input_text)
        elif option[0] == "6":
            return (self.agents.invest(self.cheltuieli.free)) + "\n\nNote: The data provided is not generated; it is based on the actual rates available on the site."


    def format_cutting(self, output):
        ret = ""
        total = 0
        parts = output.split('\n')
        for x in parts:

            subParts = x.split(":")
            left_part = subParts[0]
            if(self.can_convert_to_int(left_part[0]) == False):
                break
            perc = subParts[1]
            perc = perc[1:-1]
            ret = ret + (f"{left_part} : {((float)(perc) / 100 * (self.cheltuieli.salary)):.2f} Euro  ({perc}%)\n")
            total = total + (float)(perc) / 100 * (self.cheltuieli.salary)
        ret = ret + f"\n\nTotal = {total:.2f} Euro"
        return ret



    def can_convert_to_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def getHowMuchMorePercentage(self, timp_vrut):
        economii_luna_old = self.cheltuieli.free
        timp_initial = self.agents.timeUntillPurchase_floatRet(self.price, self.cheltuieli.free)
        economii_luna_new = (timp_initial * economii_luna_old) / timp_vrut
        percentage_economii_luna_old = economii_luna_old / self.cheltuieli.salary * 100
        percentage_economii_luna_new = economii_luna_new / self.cheltuieli.salary * 100
        return percentage_economii_luna_new - percentage_economii_luna_old



# main = Main()
# # main.initCategs()

# main.cheltuieli.debug()
# main.cheltuieli.update_percentages()

# print(main.cheltuieli.percentages_str())
# print(main.run("what does interest mean"))
# print(main.run("how much potassium do bananas have"))
# main.run("What s a good economy account")
# main.run("i want to buy a dior saddlebag")
# main.run("i want to buy the bag in 4 years")
