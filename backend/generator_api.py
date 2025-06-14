import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=API_KEY,
)

def remake_query(user_query: str) -> str:
    """Given an input query to the model, it will return the query helpful for semantic search"""

    chat_completion = client.chat.completions.create(
    messages=[
            {
                "role": "system",
                "content": ("You rephrase vague or conversational user questions into clear, concise technical queries "
                "for retrieving relevant sections from the pandas library documentation. "
                "Do not generate answers or mention specific functions. Just improve the query to aid retrieval."),
            },
            {"role": "user", "content": "How do I clean up a dataframe with missing stuff?"},
            {"role": "assistant", "content": "handling missing values in pandas DataFrame"},

            {"role": "user", "content": "Can I get some rows from a dataframe using labels?"},
            {"role": "assistant", "content": "selecting rows by label in pandas"},

            {"role": "user", "content": "How do I put stuff from a csv file into pandas?"},
            {"role": "assistant", "content": "reading CSV files into pandas DataFrame"},

            {"role": "user", "content": user_query}
        ],
        model="gemma2-9b-it",
    )

    return chat_completion.choices[0].message.content
    


def generate(query: str, data_string: str) -> str:
    """Given a string of data, it will generate a response using the model"""

    chat_completion = client.chat.completions.create(
    messages=[
            {"role": "system", "content": (
                "You are an expert in the pandas library. You are supposed to answer the user's query and not engage in conversation."
                "You will be given relevant sections from the pandas documentation and you will generate a descriptive answer to the user's query."
            )},
            {"role": "user", "content": f"Query: {query} \n Information:\n{data_string}"}
        ],
        model="gemma2-9b-it",
    )

    return chat_completion.choices[0].message.content
    
