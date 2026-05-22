import os

import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from src.infrastructure.datasets.language_dataset import (
    LanguageDataset
)

from src.infrastructure.models.transformer_lang import (
    TransformerClassifier
)

from src.infrastructure.tokenizers.hf_tokenizer import (
    load_tokenizer
)

from src.utils.logger import get_logger

from src.config.base import *


logger = get_logger(
    "train_lang",
    "logs/train_lang.log"
)


def train():

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    logger.info(f"Using device: {device}")

    tokenizer = load_tokenizer()

    dataset = LanguageDataset(
        "data/language/train.csv",
        tokenizer,
        MAX_LEN,
        PAD_IDX
    )

    logger.info(
        f"Dataset size: {len(dataset)}"
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    model = TransformerClassifier(
        vocab_size=30000,
        embed_dim=EMBED_DIM,
        num_heads=NUM_HEADS,
        ff_dim=FF_DIM,
        num_layers=NUM_LAYERS,
        num_classes=NUM_CLASSES
    ).to(device)

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LR
    )

    criterion = nn.CrossEntropyLoss()

    # =========================
    # TRAIN LOOP
    # =========================

    for epoch in range(EPOCHS):

        total_loss = 0

        model.train()

        for x, y in loader:

            x = x.to(device)
            y = y.to(device)

            optimizer.zero_grad()

            logits = model(x)

            loss = criterion(logits, y)

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(loader)

        logger.info(
            f"Epoch {epoch + 1} | "
            f"Loss: {avg_loss:.4f}"
        )

    # =========================
    # SAVE
    # =========================

    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    torch.save(
        model.state_dict(),
        "artifacts/model_lang.pth"
    )

    logger.info(
        "Language model saved!"
    )


if __name__ == "__main__":
    train()