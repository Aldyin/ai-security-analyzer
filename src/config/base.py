# ==========================================
# TOKENIZER / INPUT
# ==========================================

MAX_LEN = 128

PAD_IDX = 0

VOCAB_SIZE = 30000

# ==========================================
# TRANSFORMER
# ==========================================

EMBED_DIM = 128

NUM_HEADS = 4

FF_DIM = 256

NUM_LAYERS = 2

# ==========================================
# LANGUAGES
# ==========================================

LANGUAGE_CLASSES = [
    "Python",
    "JavaScript",
    "C",
    "Java"
]

NUM_CLASSES = len(LANGUAGE_CLASSES)

# ==========================================
# VULNERABILITIES
# ==========================================

VULN_CLASSES = [
    "SAFE",
    "SQLI",
    "XSS",
    "RCE",
    "PATH_TRAVERSAL",
    "COMMAND_INJECTION"
]

NUM_VULN_CLASSES = len(VULN_CLASSES)

# ==========================================
# TRAINING
# ==========================================

BATCH_SIZE = 32

EPOCHS = 5

LR = 1e-3

# ==========================================
# PATHS
# ==========================================

TOKENIZER_PATH = "artifacts/hf_tokenizer.json"

LANG_MODEL_PATH = "artifacts/model_lang.pth"

VULN_MODEL_PATH = "artifacts/model_vuln.pth"