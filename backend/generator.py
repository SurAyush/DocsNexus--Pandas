import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 

torch.random.manual_seed(42)

# For decent runtime use GPU for inference
checkpoint = "microsoft/Phi-3-mini-4k-instruct"

model = AutoModelForCausalLM.from_pretrained( 
    checkpoint,  
    attn_implementation="eager",
    torch_dtype="auto",  
    trust_remote_code=True,  
) 

tokenizer = AutoTokenizer.from_pretrained(checkpoint) 

pipe = pipeline( 
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
) 


def remake_query(user_query: str) -> str:
    """Given an input query to the model, it will return the query helpful for semantic search"""

    # Few shots to guide the model's behavior
    messages = [
        # system prompt to guide the model's behavior
        {"role": "system", "content": (
            "You rephrase vague or conversational user questions into clear, concise technical queries "
            "for retrieving relevant sections from the pandas library documentation. "
            "Do not generate answers or mention specific functions. Just improve the query to aid retrieval."
        )},

        # few examples to guide the model
        {"role": "user", "content": "How do I clean up a dataframe with missing stuff?"},
        {"role": "assistant", "content": "handling missing values in pandas DataFrame"},

        {"role": "user", "content": "Can I get some rows from a dataframe using labels?"},
        {"role": "assistant", "content": "selecting rows by label in pandas"},

        {"role": "user", "content": "How do I put stuff from a csv file into pandas?"},
        {"role": "assistant", "content": "reading CSV files into pandas DataFrame"},

        {"role": "user", "content": user_query}
    ]
    
    print(f"User query: {user_query}")

    generation_args = { 
        "max_new_tokens": 40, 
        "return_full_text": False, 
        "do_sample": False, 
    } 

    output = pipe(messages, **generation_args) 
    
    return output[0]['generated_text']

def generate(query: str, data_string: str) -> str:
    """Given a string of data, it will generate a response using the model"""

    messages = [
        {"role": "system", "content": (
            "You are an expert in the pandas library. "
            "You will be given relevant sections from the pandas documentation and you will generate a concise answer to the user's query."
        )},
        {"role": "user", "content": f"Query: {query} \n Information:\n{data_string}"}
    ]

    generation_args = { 
        "max_new_tokens": 200, 
        "return_full_text": False, 
        "do_sample": False, 
    } 

    output = pipe(messages, **generation_args) 
    
    return output[0]['generated_text']