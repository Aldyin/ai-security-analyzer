import torch

import torch.nn as nn

from torch.utils.data import DataLoader

from src.infrastructure.datasets.vulnerability_dataset import (
    VulnerabilityDataset
)

from src.infrastructure.models.transformer_vuln import (
    VulnerabilityClassifier
)

from src.infrastructure.tokenizers.hf_tokenizer import (
    load_tokenizer
)

from src.logging.logger import (
    get_logger
)

from src.config import *


logger = get_logger(
    "train_vuln",
    "logs/train_vuln.log"
)


def train():

    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    logger.info(
        f"Using device: {device}"
    )

    tokenizer = load_tokenizer()

    label_map = {

        v: i

        for i, v in enumerate(
            VULN_CLASSES
        )
    }

    dataset = VulnerabilityDataset(

        "data/vulnerability/train.csv",

        tokenizer,

        label_map
    )

    loader = DataLoader(

        dataset,

        batch_size=BATCH_SIZE,

        shuffle=True
    )

    model = VulnerabilityClassifier(

        vocab_size=30000,

        embed_dim=EMBED_DIM,

        num_heads=NUM_HEADS,

        ff_dim=FF_DIM,

        num_layers=NUM_LAYERS,

        num_classes=VULN_NUM_CLASSES

    ).to(device)

    optimizer = torch.optim.Adam(

        model.parameters(),

        lr=LR
    )

    # ======================================
    # CLASS IMBALANCE WEIGHTS
    # ======================================

    pos_weights = torch.tensor([

        12.0,  # SQLI

        12.0,  # XSS

        12.0,  # RCE

        6.0,   # PATH_TRAVERSAL

        12.0,  # COMMAND_INJECTION

        1.0    # SAFE

    ]).to(device)

    criterion = nn.BCEWithLogitsLoss(
        pos_weight=pos_weights
    )

    # ======================================
    # TRAIN LOOP
    # ======================================

    for epoch in range(EPOCHS):

        model.train()

        total_loss = 0

        for x, y in loader:

            x = x.to(device)

            y = y.to(device)

            optimizer.zero_grad()

            logits = model(x)

            loss = criterion(
                logits,
                y
            )

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        avg_loss = (
            total_loss / len(loader)
        )

        logger.info(

            f"Epoch {epoch + 1} | "

            f"Loss: {avg_loss:.4f}"
        )

    # ======================================
    # SAVE MODEL
    # ======================================

    torch.save(

        model.state_dict(),

        "artifacts/model_vuln.pth"
    )

    logger.info(
        "Vulnerability model saved!"
    )


if __name__ == "__main__":

    train()