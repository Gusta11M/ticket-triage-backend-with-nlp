import torch
from app.nlp.embeddings import EmbeddingService

class SimilarityService:

    @staticmethod
    def cosine_similarity(text1: str, text2: str) -> float:
        v1 = torch.tensor(EmbeddingService.embed(text1))
        v2 = torch.tensor(EmbeddingService.embed(text2))

        return torch.nn.functional.cosine_similarity(v1,v2,dim=0).item()