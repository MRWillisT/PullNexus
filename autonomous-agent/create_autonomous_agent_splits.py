#!/usr/bin/env python3
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_GLOB = "autonomous_agent*.jsonl"
EXCLUDE_FILES = {
    "autonomous_agent_train.jsonl",
    "autonomous_agent_val.jsonl",
    "autonomous_agent_test.jsonl",
}
SPLIT_RATIOS = (0.8, 0.1, 0.1)  # train, val, test
SEED = 20260428


def load_examples():
    examples = []
    for path in sorted(ROOT.glob(SOURCE_GLOB)):
        if path.name in EXCLUDE_FILES:
            continue
        if path.name.startswith("autonomous_agent_dataset_"):
            continue
        if path.name in {"autonomous_agent_dataset_manifest.json"}:
            continue
        if path.suffix != ".jsonl":
            continue
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                text = line.strip()
                if not text:
                    continue
                obj = json.loads(text)
                obj["_source_file"] = path.name
                obj["_source_line"] = line_no
                examples.append(obj)
    return examples


def write_jsonl(path: Path, items):
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for item in items:
            payload = dict(item)
            payload.pop("_source_file", None)
            payload.pop("_source_line", None)
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main():
    examples = load_examples()
    if not examples:
        print("No source examples found.")
        return 1

    rng = random.Random(SEED)
    rng.shuffle(examples)

    n = len(examples)
    n_train = int(n * SPLIT_RATIOS[0])
    n_val = int(n * SPLIT_RATIOS[1])
    n_test = n - n_train - n_val

    train_items = examples[:n_train]
    val_items = examples[n_train:n_train + n_val]
    test_items = examples[n_train + n_val:]

    write_jsonl(ROOT / "autonomous_agent_train.jsonl", train_items)
    write_jsonl(ROOT / "autonomous_agent_val.jsonl", val_items)
    write_jsonl(ROOT / "autonomous_agent_test.jsonl", test_items)

    print(f"Total: {n}")
    print(f"Train: {len(train_items)}")
    print(f"Val: {len(val_items)}")
    print(f"Test: {len(test_items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
