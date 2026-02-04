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


def test_semantic_classifier_accuracy_on_examples(monkeypatch):
    options = [
        {"id": 1, "name": "Bug", "description": "Erros e crashes"},
        {"id": 2, "name": "Feature", "description": "Novas funcionalidades"},
        {"id": 3, "name": "Support", "description": "Ajuda e duvidas"},
    ]

    cases = [
        ("A app crasha ao abrir o menu", 1),
        ("Preciso de ajuda para configurar o acesso", 3),
        ("Gostava de uma nova funcionalidade de exportar", 2),
        ("Erro 500 ao guardar", 1),
        ("Como posso recuperar a minha password?", 3),
        ("Adicionar filtro por data nos relatórios", 2),
    ]

    mapping = {
        "Bug. Erros e crashes": [1.0, 0.0],
        "Feature. Novas funcionalidades": [0.0, 1.0],
        "Support. Ajuda e duvidas": [0.0, -1.0],
        "A app crasha ao abrir o menu": [1.0, 0.0],
        "Preciso de ajuda para configurar o acesso": [0.0, -1.0],
        "Gostava de uma nova funcionalidade de exportar": [0.0, 1.0],
        "Erro 500 ao guardar": [1.0, 0.0],
        "Como posso recuperar a minha password?": [0.0, -1.0],
        "Adicionar filtro por data nos relatórios": [0.0, 1.0],
    }

    def _fake_embed(text: str):
        return mapping[text]

    monkeypatch.setattr(EmbeddingService, "embed", _fake_embed)

    correct = 0
    errors = []
    for text, expected_id in cases:
        result = SemanticClassifier.best_match(text, options)
        if result["id"] == expected_id:
            correct += 1
        else:
            errors.append((text, expected_id, result["id"]))

    accuracy = correct / len(cases)
    print("\n[Category Accuracy]")
    print(f"Correct: {correct}/{len(cases)} | Accuracy: {accuracy:.2%}")
    if errors:
        print("Errors:")
        for text, expected_id, got_id in errors:
            print(f"- '{text}' | expected={expected_id} got={got_id}")
    assert accuracy >= 0.8


def test_semantic_classifier_accuracy_on_priority_examples(monkeypatch):
    options = [
        {"id": 1, "name": "Low", "description": "impacto minimo"},
        {"id": 2, "name": "Medium", "description": "impacto moderado"},
        {"id": 3, "name": "High", "description": "impacto elevado"},
    ]

    cases = [
        ("Problema pequeno, posso esperar", 1),
        ("Bloqueia uma parte do fluxo", 2),
        ("Sistema fora do ar em producao", 3),
        ("Nao e urgente", 1),
        ("Afeta varios utilizadores", 2),
        ("Perda total de acesso", 3),
    ]

    mapping = {
        "Low. impacto minimo": [1.0, 0.0],
        "Medium. impacto moderado": [0.0, 1.0],
        "High. impacto elevado": [-1.0, 0.0],
        "Problema pequeno, posso esperar": [1.0, 0.0],
        "Bloqueia uma parte do fluxo": [0.0, 1.0],
        "Sistema fora do ar em producao": [-1.0, 0.0],
        "Nao e urgente": [1.0, 0.0],
        "Afeta varios utilizadores": [0.0, 1.0],
        "Perda total de acesso": [-1.0, 0.0],
    }

    def _fake_embed(text: str):
        return mapping[text]

    monkeypatch.setattr(EmbeddingService, "embed", _fake_embed)

    correct = 0
    errors = []
    for text, expected_id in cases:
        result = SemanticClassifier.best_match(text, options)
        if result["id"] == expected_id:
            correct += 1
        else:
            errors.append((text, expected_id, result["id"]))

    accuracy = correct / len(cases)
    print("\n[Priority Accuracy]")
    print(f"Correct: {correct}/{len(cases)} | Accuracy: {accuracy:.2%}")
    if errors:
        print("Errors:")
        for text, expected_id, got_id in errors:
            print(f"- '{text}' | expected={expected_id} got={got_id}")
    assert accuracy >= 0.8


@pytest.mark.slow
def test_semantic_classifier_real_model_accuracy():
    options = [
        {"id": 1, "name": "Bug", "description": "Erros e crashes"},
        {"id": 2, "name": "Feature", "description": "Novas funcionalidades"},
        {"id": 3, "name": "Support", "description": "Ajuda e duvidas"},
    ]

    cases = [
        ("A app crasha ao abrir o menu", 1),
        ("Erro 500 ao guardar o ticket", 1),
        ("Gostava de uma nova funcionalidade de exportar", 2),
        ("Adicionar filtro por data nos relatorios", 2),
        ("Preciso de ajuda para recuperar a password", 3),
        ("Nao consigo configurar o acesso", 3),
    ]

    try:
        NLPModel.load()
    except Exception as exc:
        pytest.skip(f"Modelo real indisponivel: {exc}")

    correct = 0
    errors = []
    for text, expected_id in cases:
        result = SemanticClassifier.best_match(text, options)
        if result["id"] == expected_id:
            correct += 1
        else:
            errors.append((text, expected_id, result["id"], result.get("confidence")))

    accuracy = correct / len(cases)
    print("\n[Real Model Accuracy]")
    print(f"Correct: {correct}/{len(cases)} | Accuracy: {accuracy:.2%}")
    if errors:
        print("Errors:")
        for text, expected_id, got_id, conf in errors:
            print(f"- '{text}' | expected={expected_id} got={got_id} conf={conf}")

    assert accuracy >= 0.5
