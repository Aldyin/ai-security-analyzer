import os

from tokenizers import Tokenizer

TOKENIZER_PATH = "artifacts/hf_tokenizer.json"


def save_tokenizer(tokenizer):

    os.makedirs("artifacts", exist_ok=True)

    tokenizer.save(TOKENIZER_PATH)

    print(f"✅ Tokenizer saved: {TOKENIZER_PATH}")


def load_tokenizer():

    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(
            f"Tokenizer not found: {TOKENIZER_PATH}"
        )

    tokenizer = Tokenizer.from_file(TOKENIZER_PATH)

    validate_tokenizer(tokenizer)

    return tokenizer


def validate_tokenizer(tokenizer):

    vocab_size = tokenizer.get_vocab_size()

    if vocab_size < 100:
        raise ValueError(
            "Tokenizer vocab слишком маленький"
        )

    required_tokens = [
        "[PAD]",
        "[UNK]"
    ]

    vocab = tokenizer.get_vocab()

    for token in required_tokens:

        if token not in vocab:
            raise ValueError(
                f"Missing required token: {token}"
            )

    print(f"✅ Tokenizer validated | vocab={vocab_size}")


def tokenizer_info(tokenizer):

    vocab_size = tokenizer.get_vocab_size()

    print("\n===== TOKENIZER INFO =====")
    print(f"Vocab size: {vocab_size}")

    vocab = tokenizer.get_vocab()

    special = [
        token for token in vocab
        if token.startswith("[")
    ]

    print(f"Special tokens: {special}")