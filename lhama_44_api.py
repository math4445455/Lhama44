from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI(title="Lhama44")

# Carregando modelo e tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

class Prompt(BaseModel):
    texto: str
    max_tokens: int = 100

@app.post("/gerar/")
def gerar_texto(prompt: Prompt):
    inputs = tokenizer(prompt.texto, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=prompt.max_tokens,
            temperature=0.9,
            do_sample=True,
            top_k=50,
            top_p=0.95
        )
    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"resposta": resposta}
