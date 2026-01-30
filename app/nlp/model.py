from transformers import AutoTokenizer, AutoModel
import torch

MODEL_NAME = "distilbert/distilbert-base-multilingual-cased"

class NLPModel:
    _tokenizer = None
    _model = None

    @classmethod
    def load(cls):
        if cls._model is None or cls._tokenizer is None:
            cls._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            cls._model = AutoModel.from_pretrained(MODEL_NAME)
            cls._model.eval()
        return cls._tokenizer, cls._model