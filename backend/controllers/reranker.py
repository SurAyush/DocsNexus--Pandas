from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')      

checkpoint = "cross-encoder/ms-marco-MiniLM-L-6-v2"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

# Move model to the appropriate device
model = model.to(device)

def rerank(query, documents, k):
    '''
        Rerank a list of documents based on their relevance to a query using a cross-encoder model.
    '''

    reranked = []
    for document in documents:
        inputs = tokenizer.encode_plus(query, document, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            score = logits[0][0].item()

        reranked.append((document, score))


    reranked.sort(key=lambda x: x[1], reverse=True)
    reranked = reranked[:k]
    print(reranked)
    reranked = [doc for doc, score in reranked]

    return reranked

