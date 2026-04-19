import json
import os

# ── Load tree ──────────────────────────────────────────────────────────────────
def load_tree(path="reflection-tree.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {node["id"]: node for node in data["nodes"]}

# ── Signal accumulator ─────────────────────────────────────────────────────────
signals = {
    "A1": [],  # locus
    "A2": [],  # orientation
    "A3": []   # radius
}

summary_signals = {
    "A1_signal": None,
    "A2_signal": None,
    "A3_signal": None
}

def record_signal(node_id, signal):
    if signal is None:
        return
    if node_id.startswith("A1"):
        signals["A1"].append(signal)
        summary_signals["A1_signal"] = signal
    elif node_id.startswith("A2"):
        signals["A2"].append(signal)
        summary_signals["A2_signal"] = signal
    elif node_id.startswith("A3"):
        signals["A3"].append(signal)
        summary_signals["A3_signal"] = signal

# ── Interpolate summary ────────────────────────────────────────────────────────
def interpolate(text, interpolation_map):
    for key, mapping in interpolation_map.items():
        signal = summary_signals.get(key)
        value  = mapping.get(signal, "—")
        text   = text.replace("{" + key + "}", value)
    return text

# ── Print helpers ──────────────────────────────────────────────────────────────
def divider():
    print("\n" + "─" * 55 + "\n")

def print_node_text(node):
    type_labels = {
        "start":      "✦  WELCOME",
        "bridge":     "→  TRANSITION",
        "question":   "?  QUESTION",
        "reflection": "◎  REFLECTION",
        "summary":    "★  SUMMARY",
        "end":        "✔  END",
        "decision":   "⇒  DECISION"
    }
    label = type_labels.get(node["type"], node["type"].upper())
    print(f"{label}")
    print(node["text"])

# ── Walk the tree ──────────────────────────────────────────────────────────────
def walk(tree, start_id="START"):
    current_id = start_id
    transcript = []

    while current_id:
        node = tree.get(current_id)
        if not node:
            print(f"[ERROR] Node '{current_id}' not found.")
            break

        divider()
        print_node_text(node)
        transcript.append({"id": current_id, "type": node["type"], "text": node["text"]})

        # ── DECISION node ──────────────────────────────────────────────────────
        if node["type"] == "decision":
            # Decision nodes route silently — no user input needed
            # They rely on the last answer stored in last_answer
            current_id = node["rules"][0]["target"]  # default fallback
            continue

        # ── QUESTION node ──────────────────────────────────────────────────────
        if node["type"] == "question":
            options = node.get("options", [])
            print()
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt['text']}")
            print()

            while True:
                try:
                    choice = int(input("  Your answer (enter number): "))
                    if 1 <= choice <= len(options):
                        break
                    print(f"  Please enter a number between 1 and {len(options)}.")
                except ValueError:
                    print("  Please enter a valid number.")

            chosen = options[choice - 1]
            signal = chosen.get("signal")
            record_signal(current_id, signal)

            transcript.append({
                "answered": chosen["text"],
                "signal":   signal
            })

            # If option has its own target (Q5 router questions)
            if chosen.get("target"):
                current_id = chosen["target"]
            else:
                current_id = node.get("target")
            continue

        # ── REFLECTION node ────────────────────────────────────────────────────
        if node["type"] == "reflection":
            record_signal(current_id, node.get("signal"))
            input("\n  [ Press Enter to continue ] ")
            current_id = node.get("target")
            continue

        # ── BRIDGE / START node ────────────────────────────────────────────────
        if node["type"] in ("bridge", "start"):
            input("\n  [ Press Enter to continue ] ")
            current_id = node.get("target")
            continue

        # ── SUMMARY node ───────────────────────────────────────────────────────
        if node["type"] == "summary":
            interp = node.get("interpolation", {})
            print()
            print("  " + interpolate(node["text"], interp))
            transcript.append({"summary": interpolate(node["text"], interp)})
            input("\n  [ Press Enter to finish ] ")
            current_id = node.get("target")
            continue

        # ── END node ───────────────────────────────────────────────────────────
        if node["type"] == "end":
            print()
            break

    return transcript

# ── Save transcript ────────────────────────────────────────────────────────────
def save_transcript(transcript, filename="transcript.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for entry in transcript:
            if "type" in entry:
                f.write(f"[{entry['type'].upper()}] {entry['text']}\n")
            if "answered" in entry:
                f.write(f"  → Answer: {entry['answered']} (signal: {entry['signal']})\n")
            if "summary" in entry:
                f.write(f"\nSUMMARY: {entry['summary']}\n")
        f.write("\nSignals recorded:\n")
        for axis, sigs in signals.items():
            f.write(f"  {axis}: {sigs}\n")
    print(f"\n  Transcript saved to '{filename}'")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 55)
    print("      DAILY REFLECTION TREE")
    print("═" * 55)

    tree = load_tree("reflection-tree.json")

    name = input("\nBefore we start — what's your name? ").strip() or "Friend"
    print(f"\nGood to have you here, {name}.")

    transcript = walk(tree)

    print("\n" + "═" * 55)
    save_name = input("Save transcript as (press Enter for 'transcript.txt'): ").strip()
    if not save_name:
        save_name = "transcript.txt"
    save_transcript(transcript, save_name)

    print("\n  Done. See you tomorrow.\n")