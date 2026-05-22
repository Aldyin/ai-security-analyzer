import random
import csv
from pathlib import Path
import os

random.seed(42)

# =====================
# CONFIG
# =====================

SOURCE_DIR = Path("lots_of_code")
OUTPUT_DIR = Path("data/vulnerability")

LANGUAGES = {
    "Python": 0,
    "C": 1,
    "Java": 2,
    "JavaScript": 3,
}

VULN_CLASSES = [
    "SQLI",
    "XSS",
    "RCE",
    "PATH_TRAVERSAL",
    "COMMAND_INJECTION",
    "SAFE"
]

MIN_CHARS = 50
MAX_PER_LANG = 2000

TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15

# =====================
# RULES (ключова частина)
# =====================

def detect_vulnerabilities(code):
    c = code.lower()
    labels = []

    # RCE
    if any(x in c for x in ["eval(", "exec(", "os.system", "subprocess"]):
        labels.append("RCE")

    # SQL Injection
    if ("select" in c or "insert" in c) and ("+" in c or "%" in c):
        labels.append("SQLI")

    # XSS
    if any(x in c for x in ["<script>", "innerhtml", "document.write"]):
        labels.append("XSS")

    # Path Traversal
    if "../" in c or "..\\" in c:
        labels.append("PATH_TRAVERSAL")

    # Command Injection
    if any(x in c for x in ["system(", "popen("]):
        labels.append("COMMAND_INJECTION")

    if not labels:
        labels.append("SAFE")

    return list(set(labels))


# =====================
# HELPERS
# =====================

def read_txt(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def split_into_chunks(text):
    raw_chunks = text.split("\n\n")

    chunks = []
    for chunk in raw_chunks:
        chunk = chunk.strip()

        if len(chunk) < MIN_CHARS:
            continue

        if chunk.count("{") + chunk.count(";") + chunk.count(":") < 2:
            continue

        chunks.append(chunk)

    return chunks


# =====================
# DATA COLLECTION
# =====================

dataset = []

for lang, label in LANGUAGES.items():
    print(f"\nProcessing {lang}")

    file_path = SOURCE_DIR / lang / "data.txt"

    if not file_path.exists():
        print(f"❌ {file_path} not found")
        continue

    text = read_txt(file_path)
    chunks = split_into_chunks(text)

    print(f"Found {len(chunks)} chunks")

    count = 0

    for chunk in chunks:
        vulns = detect_vulnerabilities(chunk)

        dataset.append({
            "code": chunk,
            "labels": ",".join(vulns)
        })

        count += 1

        if count >= MAX_PER_LANG:
            break

    print(f"Used {count} samples")

# =====================
# SHUFFLE
# =====================

random.shuffle(dataset)

# =====================
# SPLIT
# =====================

n = len(dataset)

train_end = int(TRAIN_SPLIT * n)
val_end = int((TRAIN_SPLIT + VAL_SPLIT) * n)

train = dataset[:train_end]
val = dataset[train_end:val_end]
test = dataset[val_end:]

print("\n====================")
print(f"TOTAL: {n}")
print(f"TRAIN: {len(train)}")
print(f"VAL:   {len(val)}")
print(f"TEST:  {len(test)}")
print("====================")

# =====================
# SAVE
# =====================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save_csv(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar="\\")

        writer.writerow(["code", "labels"])

        for row in data:
            writer.writerow([row["code"], row["labels"]])

save_csv(OUTPUT_DIR / "train.csv", train)
save_csv(OUTPUT_DIR / "val.csv", val)
save_csv(OUTPUT_DIR / "test.csv", test)

print("\n✅ Vulnerability dataset CREATED!")