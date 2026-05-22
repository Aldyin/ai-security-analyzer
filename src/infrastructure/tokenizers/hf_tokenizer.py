from transformers import PreTrainedTokenizerFast

from src.config import *

tokenizer = PreTrainedTokenizerFast(
    tokenizer_file=TOKENIZER_PATH
)

tokenizer.add_special_tokens({
    "pad_token": "[PAD]"
})

tokenizer.pad_token = "[PAD]"

print(
    f"✅ Tokenizer validated | vocab={tokenizer.vocab_size}"
)


def load_tokenizer():

    return tokenizer


def encode_code(code: str):

    encoded = tokenizer.encode(
        code,
        padding="max_length",
        truncation=True,
        max_length=MAX_LEN
    )

    return encoded