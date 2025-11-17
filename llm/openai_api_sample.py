from openai import OpenAI
from sys import argv

#Below add your OpenAI API key
api_key = "" 

#The specific model you wish to use goes below
model_name=""

client = OpenAI.OpenAI(api_key="lm-studio")

#Function for submitting a prompt to a given model
def query_llm(prompt,model_name):
    try:
        response = client.chat.completions.create(
        model=model_name,
        messages=[
    {"role": "user", "content": prompt}
    ],
    temperature=0.8,
)
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Main script, assumes the text of the prompt is given in the command line, otherwise
#replace 'argv[1]' below with your prompt string

if __name__ == "__main__":
    user_query = argv[1]
    response = query_llm(user_query)
    if response:
        print("Response from LLM:")
        print(response)