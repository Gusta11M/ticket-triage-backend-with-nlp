import torch
from app.nlp.embeddings import EmbeddingService

class SemanticClassifier:

    @staticmethod
    def best_match(text: str, options: list[dict]) -> dict:
        """
        options = [
            { "id": 1, "name": "Bug", "description": "Erros, crashes..." }
        ]
        """
        text_vec = torch.tensor(EmbeddingService.embed(text))

        best = None
        best_score = -1

        for opt in options:
            opt_text = f"{opt['name']}. {opt['description']}"
            opt_vec = torch.tensor(EmbeddingService.embed(opt_text))

            score = torch.nn.functional.cosine_similarity(
                text_vec, opt_vec, dim=0
            ).item()

            if score > best_score:
                best_score = score
                best = opt

        return {
            **best,
            "confidence": round(best_score, 3)
        }
