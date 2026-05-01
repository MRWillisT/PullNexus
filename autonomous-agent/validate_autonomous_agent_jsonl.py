#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GLOB = "autonomous_agent*.jsonl"
SPLIT_FILES = {
    "autonomous_agent_train.jsonl",
    "autonomous_agent_val.jsonl",
    "autonomous_agent_test.jsonl",
}


def validate_sharegpt(obj, path, line_no, errors):
    conv = obj.get("conversations")
    if not isinstance(conv, list) or not conv:
        errors.append(f"{path}:{line_no} missing or empty conversations")
        return
    for i, turn in enumerate(conv):
        if not isinstance(turn, dict):
            errors.append(f"{path}:{line_no} conversations[{i}] not object")
            continue
        if turn.get("from") not in {"human", "gpt"}:
            errors.append(f"{path}:{line_no} conversations[{i}].from invalid")
        if not isinstance(turn.get("value"), str) or not turn.get("value").strip():
            errors.append(f"{path}:{line_no} conversations[{i}].value invalid")


def validate_chatml(obj, path, line_no, errors):
    msgs = obj.get("messages")
    if not isinstance(msgs, list) or not msgs:
        errors.append(f"{path}:{line_no} missing or empty messages")
        return
    for i, msg in enumerate(msgs):
        if not isinstance(msg, dict):
            errors.append(f"{path}:{line_no} messages[{i}] not object")
            continue
        if msg.get("role") not in {"user", "assistant", "system"}:
            errors.append(f"{path}:{line_no} messages[{i}].role invalid")
        if not isinstance(msg.get("content"), str) or not msg.get("content").strip():
            errors.append(f"{path}:{line_no} messages[{i}].content invalid")


def validate_file(path, errors, seen_ids):
    local_ids = set()
    is_split_file = path.name in SPLIT_FILES
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                errors.append(f"{path}:{line_no} empty line not allowed")
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{path}:{line_no} invalid json: {e.msg}")
                continue

            if not isinstance(obj, dict):
                errors.append(f"{path}:{line_no} top-level must be object")
                continue

            item_id = obj.get("id")
            if not isinstance(item_id, str) or not item_id.strip():
                errors.append(f"{path}:{line_no} missing/invalid id")
            else:
                if item_id in local_ids:
                    errors.append(f"{path}:{line_no} duplicate id in file: {item_id}")
                local_ids.add(item_id)
                if (not is_split_file) and (item_id in seen_ids):
                    errors.append(f"{path}:{line_no} duplicate id: {item_id}")
                if not is_split_file:
                    seen_ids.add(item_id)

            has_conv = "conversations" in obj
            has_msgs = "messages" in obj
            if has_conv and has_msgs:
                errors.append(f"{path}:{line_no} contains both conversations and messages")
            elif has_conv:
                validate_sharegpt(obj, path.name, line_no, errors)
            elif has_msgs:
                validate_chatml(obj, path.name, line_no, errors)
            else:
                errors.append(f"{path}:{line_no} must include conversations or messages")


def main():
    files = sorted(ROOT.glob(GLOB))
    if not files:
        print(f"No files matching {GLOB}")
        return 1

    errors = []
    seen_ids = set()
    total_lines = 0
    for path in files:
        line_count = 0
        with path.open("r", encoding="utf-8") as f:
            for _ in f:
                line_count += 1
        total_lines += line_count
        validate_file(path, errors, seen_ids)

    print(f"Validated files: {len(files)}")
    print(f"Validated examples (lines): {total_lines}")
    print(f"Unique IDs: {len(seen_ids)}")

    if errors:
        print(f"Errors: {len(errors)}")
        for err in errors:
            print(f"- {err}")
        return 2

    print("Validation passed with no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
