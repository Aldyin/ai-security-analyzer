import pandas as pd
from tokenizers import Tokenizer, models, trainers, pre_tokenizers


def train_tokenizer():
    df = pd.read_csv("data/language/train.csv")

    with open("tmp.txt", "w", encoding="utf-8") as f:
        for code in df["code"]:
            f.write(str(code) + "\n")

    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

    trainer = trainers.BpeTrainer(
        vocab_size=30000,
        special_tokens=["[PAD]", "[UNK]", "[CODE]"]
    )

    tokenizer.train(["tmp.txt"], trainer)
    tokenizer.save("artifacts/hf_tokenizer.json")

    print("✅ tokenizer ready")


if __name__ == "__main__":
    train_tokenizer()