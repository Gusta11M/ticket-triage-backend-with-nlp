import torch
from app.nlp.model import NLPModel

class EmbeddingService:

    @staticmethod
    def embed(text: str) -> list[float]:
        tokenizer, model = NLPModel.load()

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_lenght=256
        )

        with torch.no_grad():
            outputs = model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1)

        return embeddings[0].tolist()