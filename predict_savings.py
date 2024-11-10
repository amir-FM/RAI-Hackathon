import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = "https://rbro-openai-hackatlon.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview", # insert the provided endpoint here 
  api_key="6wg18MMZ9VmVnWH3lQB2ziSrmjiAFz1AndPuOOL7v2uzNNVzAXYgJQQJ99AKACfhMk5XJ3w3AAABACOGKhWf", # insert the provided api key here  
  api_version="2024-08-01-preview"
)


def products(advised_savings):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": """You are a helpful assistant that recommends saving accounts at Raiffaisen Romania or government bonds or treasury bonds Romania, displaying benefit."""},
            {"role": "user", "content": f"Give me the result of putting {advised_savings} every month for a year in saving accounts at Raiffaisen Romania or government bonds or treasury bonds Romania, display only final result and multiple options, also writing separtely benefit"}
        ],
    max_tokens=400,
    temperature=0.2,
)
    return response.choices[0].message.content

print(products(100))

def find

