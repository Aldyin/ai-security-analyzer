import random
import csv
from pathlib import Path
import os

random.seed(42)

SOURCE_DIR = Path("lots_of_code")
OUTPUT_FILE = Path("data/language/test.csv")

LANGUAGES = {
    "Python": 0,
    "C": 1,
    "Java": 2,
    "JavaScript": 3,
}

MIN_CHARS = 50
MAX_PER_LANG = 500


def read_txt(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def split_into_chunks(text):
    raw_chunks = text.split("\n\n")

    chunks = []
    for chunk in raw_chunks:
        chunk = chunk.strip()

        if len(chunk) < MIN_CHARS:
            continue

        # фільтр "це код"
        if chunk.count("{") + chunk.count(";") + chunk.count(":") < 2:
            continue

        chunks.append(chunk)

    return chunks


def generate():
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
            dataset.append((chunk, label))
            count += 1

            if count >= MAX_PER_LANG:
                break

        print(f"Used {count} samples")

    random.shuffle(dataset)

    print("\n====================")
    print(f"TOTAL TEST SAMPLES: {len(dataset)}")
    print("====================")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        os.remove(OUTPUT_FILE)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(
            f,
            quoting=csv.QUOTE_ALL,
            escapechar="\\"
        )

        writer.writerow(["code", "label"])
        writer.writerows(dataset)

    print("\n✅ test.csv CREATED!")


if __name__ == "__main__":
    generate()