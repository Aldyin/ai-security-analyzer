import torch
import torch.nn as nn

from src.config import *


class PositionalEncoding(nn.Module):

    def __init__(self, embed_dim, max_len=512):
        super().__init__()

        pe = torch.zeros(max_len, embed_dim)

        position = torch.arange(
            0,
            max_len,
            dtype=torch.float
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                embed_dim,
                2
            ).float() * (-torch.log(torch.tensor(10000.0)) / embed_dim)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)

        self.register_buffer("pe", pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]


class VulnerabilityClassifier(nn.Module):

    def __init__(
        self,
        vocab_size,
        embed_dim,
        num_heads,
        ff_dim,
        num_layers,
        num_classes,
        max_len=512,
        dropout=0.1
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embed_dim,
            padding_idx=PAD_IDX
        )

        self.positional_encoding = PositionalEncoding(
            embed_dim,
            max_len
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.dropout = nn.Dropout(dropout)

        self.classifier = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(embed_dim, ff_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(ff_dim // 2, num_classes)
        )

    def forward(self, x):

        mask = (x != PAD_IDX)

        x = self.embedding(x)

        x = self.positional_encoding(x)

        x = self.encoder(
            x,
            src_key_padding_mask=~mask
        )

        x = x.mean(dim=1)

        x = self.dropout(x)

        logits = self.classifier(x)

        return logits