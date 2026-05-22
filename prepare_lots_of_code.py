import csv
import random
from pathlib import Path

random.seed(42)

SOURCE_DIR = Path("lots_of_code")
OUTPUT_DIR = Path("data/language")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LANGUAGES = {
    "Python": 0,
    "C": 1,
    "Java": 2,
    "JavaScript": 3,
}

MAX_PER_LANG = 5000
MIN_CHARS = 50


def stream_chunks(path):
    """
    Читає файл потоково без завантаження всього у RAM
    """
    buffer = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip() == "":
                chunk = "".join(buffer).strip()

                if len(chunk) >= MIN_CHARS:
                    yield chunk

                buffer = []
            else:
                buffer.append(line)

        # останній chunk
        if buffer:
            chunk = "".join(buffer).strip()

            if len(chunk) >= MIN_CHARS:
                yield chunk


dataset = []

for lang, label in LANGUAGES.items():
    print(f"\nProcessing {lang}")

    path = SOURCE_DIR / lang / "data.txt"

    if not path.exists():
        print(f"❌ Missing: {path}")
        continue

    count = 0

    for chunk in stream_chunks(path):
        dataset.append((chunk, label))

        count += 1

        if count % 1000 == 0:
            print(f"Collected {count}")

        if count >= MAX_PER_LANG:
            break

    print(f"✔ Final samples: {count}")


print("\nShuffling...")
random.shuffle(dataset)

n = len(dataset)

train_end = int(0.7 * n)
val_end = int(0.85 * n)

train = dataset[:train_end]
val = dataset[train_end:val_end]
test = dataset[val_end:]


def save_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        writer.writerow(["code", "label"])

        for row in rows:
            writer.writerow(row)


print("Saving CSV files...")

save_csv(OUTPUT_DIR / "train.csv", train)
save_csv(OUTPUT_DIR / "val.csv", val)
save_csv(OUTPUT_DIR / "test.csv", test)

print("\n✅ Dataset generation completed!")