from src.domain.entities.code_sample import CodeSample


class LanguageDetector:
    """
    Domain service для визначення мови програмування.
    Обгортка над існуючим predict.py (нічого не ламає).
    """

    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def detect(self, code_sample: CodeSample):
        from src.inference.predict import predict_code

        return predict_code(
            code_sample.raw,
            self.model,
            self.tokenizer,
            self.device
        )