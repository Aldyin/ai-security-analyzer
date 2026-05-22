import torch


DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

MAX_LEN = 128

PAD_IDX = 0