from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import time
from langdetect import detect
from transformers import BertTokenizer, BertModel

app = FastAPI(title="Text Processing API")

# Load models only once (at startup)
nlp = spacy.load("en_core_web_sm")
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')
model = BertModel.from_pretrained('bert-base-multilingual-uncased')

def process_text(text: str):
    # Detect language
    lang = detect(text)
    
    # Start timer
    start_time = time.time()
    
    # Process text with spaCy for NER and tokenization
    doc = nlp(text)
    tokens = [token.text for token in doc]
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # BERT embedding (showcasing the operation)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    
    # Calculate time taken
    end_time = time.time()
    time_taken = end_time - start_time

    return {
        "language": lang,
        "tokens": tokens,
        "named_entities": entities,
        "query_length": len(text),
        "time_taken": time_taken
    }

# Define request body model
class Query(BaseModel):
    text: str

# FastAPI endpoint to process text
@app.post("/process/")
async def process_query(query: Query):
    results = process_text(query.text)
    return results
