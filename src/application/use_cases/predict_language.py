from src.domain.entities.code_sample import CodeSample
from src.domain.services.language_detector import LanguageDetector


def run(code: str, model, tokenizer, device):
    sample = CodeSample(code)
    detector = LanguageDetector(model, tokenizer, device)
    return detector.detect(sample)