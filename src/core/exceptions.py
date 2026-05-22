class AnalyzerException(Exception):
    pass


class ModelNotLoadedError(
    AnalyzerException
):
    pass


class InvalidCodeError(
    AnalyzerException
):
    pass


class TokenizerError(
    AnalyzerException
):
    pass