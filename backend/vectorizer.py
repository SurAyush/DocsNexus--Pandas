from transformers import AutoTokenizer, AutoModel

checkpoint = "sentence-transformers/multi-qa-mpnet-base-dot-v1" 

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModel.from_pretrained(checkpoint)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]    

def get_embeddings(text_list):

    encoded_input = tokenizer(
        text_list,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    model_output = model(**encoded_input)

    return cls_pooling(model_output)