import pytest
import torch

from app.nlp.embeddings import EmbeddingService
from app.nlp.similarity import SimilarityService
from app.nlp.classifier import SemanticClassifier
from app.nlp.model import NLPModel


class _FakeTokenizer:
    def __call__(self, text, return_tensors=None, truncation=None, padding=None, max_lenght=None):
        # Return a minimal input dict that the fake model can accept.
        return {"input_ids": torch.tensor([[1, 2, 3]])}


class _FakeOutputs:
    def __init__(self, last_hidden_state: torch.Tensor):
        self.last_hidden_state = last_hidden_state


class _FakeModel:
    def __call__(self, **inputs):
        # Shape: (batch=1, tokens=2, hidden=3)
        last_hidden_state = torch.tensor(
            [[[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]]]
        )
        return _FakeOutputs(last_hidden_state)

    def eval(self):
        return self


@pytest.mark.asyncio
async def test_embedding_service_embed_returns_mean_vector(monkeypatch):
    def _fake_load():
        return _FakeTokenizer(), _FakeModel()

    monkeypatch.setattr(NLPModel, "load", _fake_load)

    vec = EmbeddingService.embed("qualquer texto")
    # Mean of [[1,2,3],[3,2,1]] = [2,2,2]
    assert vec == [2.0, 2.0, 2.0]


def test_similarity_service_cosine_similarity(monkeypatch):
    def _fake_embed(text: str):
        if text == "a":
            return [1.0, 0.0]
        return [1.0, 0.0]

    monkeypatch.setattr(EmbeddingService, "embed", _fake_embed)

    score = SimilarityService.cosine_similarity("a", "b")
    assert score == pytest.approx(1.0)


def test_semantic_classifier_best_match(monkeypatch):
    def _fake_embed(text: str):
        mapping = {
            "ticket": [1.0, 0.0],
            "Bug. Erros": [1.0, 0.0],
            "Feature. Novas funcionalidades": [0.0, 1.0],
        }
        return mapping[text]

    monkeypatch.setattr(EmbeddingService, "embed", _fake_embed)

    options = [
        {"id": 1, "name": "Bug", "description": "Erros"},
        {"id": 2, "name": "Feature", "description": "Novas funcionalidades"},
    ]

    result = SemanticClassifier.best_match("ticket", options)
    assert result["id"] == 1
    assert result["name"] == "Bug"
    assert result["confidence"] == 1.0
