# Reflection Tree Project

A deterministic daily reflection tool built on three psychological axes.

---

## What It Does

Walks a user through 15 questions across three axes, accumulates signals, and returns a one-line summary of how they showed up at work today.

---

## The Three Axes

| Axis | Spectrum |
|---|---|
| Axis 1 — Locus of Control | Victim ↔ Victor |
| Axis 2 — Orientation | Entitlement ↔ Contribution |
| Axis 3 — Radius | Self ↔ Others |

---

## Files

| File | Description |
|---|---|
| `reflection-tree.json` | 37-node decision tree (questions, reflections, bridges, summary) |
| `agent.py` | Python script that loads the tree and runs the conversation |
| `transcript_persona_A.txt` | Victim / Entitled / Self-centric persona run |
| `transcript_persona_B.txt` | Victor / Contributing / Altrocentric persona run |

---

## How To Run

```bash
python agent.py
```

Make sure `reflection-tree.json` is in the same folder.

---

## Concepts Used

- Locus of Control
- Growth Mindset
- Psychological Entitlement
- Organisational Citizenship Behaviour (OCB)
- Self-Transcendence
- Perspective-Taking
