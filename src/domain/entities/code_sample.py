class CodeSample:
    """
    Domain entity для представлення коду.
    Інкапсулює нормалізацію, щоб не дублювати її в dataset/predict/gui.
    """

    def __init__(self, code: str):
        self.raw = code
        self.normalized = self._normalize(code)

    def _normalize(self, code: str) -> str:
        return "[CODE] " + code.lower().strip()

    def __repr__(self):
        return f"CodeSample(len={len(self.raw)})"