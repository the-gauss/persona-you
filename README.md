# PersonaYou

PersonaYou lets you build a lightweight, personal “chat personality” that talks and behaves like a specific person based on your own message history with them. It is not a messaging app; it’s a personality layer you can query locally for fun and experimentation.

Important notes:
- Source data: your WhatsApp/iMessage exports (hundreds, not thousands, of messages per contact is fine).
- Scope: personality cloning for conversation style; not intended for impersonation in real-world contexts.
- Privacy: designed for local, personal use. You control the data and can delete it at any time.

## What This Is (and Isn’t)
- Chat personality, not a client: You don’t send messages from this tool; you chat with a simulated persona of yourself or a friend.
- Small-data friendly: Works with limited conversation history by combining retrieval with lightweight fine-tuning or adapters.
- Memory-driven: Incorporates factual “memories” you provide or extract (e.g., birthdays, preferences) to ground responses.

## High-Level Approach
1. Ingest your chats: Parse WhatsApp/iMessage exports into a normalized conversation dataset per person.
2. Build style + memory:
   - Style: learn tone, phrasing, emojis, and quirks via prompt templates or LoRA adapters.
   - Memory: extract stable facts and recurring preferences; store in a small vector/JSON memory.
3. Generate responses: Use a local model with retrieval-augmented prompts and optional adapters for each persona.

This hybrid approach works well when you have hundreds of messages: retrieval carries factual grounding; small adapters or carefully engineered prompts capture voice and cadence.

## Getting Started

Prereqs
- Python 3.10+
- A local model runtime (e.g., `llama.cpp`, `Ollama`, or `transformers` with a small GGUF/pt model) (All subject to change as the project progresses)
- Your exported chats (WhatsApp `.zip` or `.txt`, iMessage `.json`/`.csv` from export tools)

Setup
1. Place chat exports under `data/raw/<person_name>/`.
2. Run the ingestion script to produce a unified dataset under `data/processed/<person_name>.jsonl`.
3. (Optional) Run memory extraction to create `data/memory/<person_name>.json` and an embeddings index.
4. Choose a model backend and run the playground CLI to chat with the persona.

Example project layout
- `data/raw/` — raw exports per person
- `data/processed/` — cleaned message turns (`.jsonl` per person)
- `data/memory/` — factual memories and vector index
- `personas/` — prompt templates and (optional) LoRA adapters per person
- `scripts/` — ingestion, memory extraction, finetune helpers, chat CLI

## Data Ingestion

What we keep
- Speaker, timestamp (optional), message text, reactions/emojis.
- Basic thread boundaries to infer turn-taking.

What we drop
- Media contents (unless you opt-in for captions).
- Phone numbers, links, and IDs (can be masked).

Normalization tips
- Merge consecutive messages by the same speaker within a short window.
- Remove obvious boilerplate (e.g., “Missed voice call”).
- Keep emojis—style often depends on them.

## Building a Persona

Minimum viable persona
- Prompt template with style examples: few-shot snippets capturing tone, typical openings/closings, and emoji usage.
- Memory file with facts and stable preferences.

Upgrades for better mimicry
- LoRA/PEFT adapter trained on the person’s messages (hundreds of examples are enough for style transfer).
- A small retrieval index over their messages to surface phrasing patterns and contextually similar replies.

Safety and consent
- Only use chats you own and have consent to process.
- Label generated text as simulated; avoid using it to impersonate someone to others.
- Provide a one-command wipe: delete persona data, adapters, and indexes.

## Model Choices

Good local options (pick one based on your hardware):
- Small LLMs via Ollama (e.g., `llama3`, `mistral`) or `llama.cpp` GGUF builds.
- `transformers` with 7B-class models for adapter training (LoRA) if you have a GPU.

Serving
- Use a single system prompt per persona that encodes: voice descriptors, do/don’t rules, and memory injection.
- Prepend top-k retrieved style snippets or quotes from their history (with masking/anonymization).

## Training on Small Data

When you only have hundreds of messages:
- Prefer LoRA over full fine-tuning; train on reply pairs (prompt: interlocutor message; target: the person’s reply).
- Use deduplication and length filtering to avoid overfitting to very short acknowledgments.
- Add a style discriminator (optional): encourage emoji frequency or certain punctuation via reward shaping or curated examples.

Fast baseline (no training)
- Handcraft a style prompt + 10–20 cherry‑picked example turns.
- Add a few “negative” examples to avoid unwanted behavior (e.g., dodging sensitive topics).

## Memory

Two layers
- Facts: JSON store of stable info (names, places, recurring preferences).
- Style snippets: short lines that reflect voice (e.g., “yesss 😭”, “okok”, “lolol”).

Retrieval
- Embed both recent context and the interlocutor’s current message; retrieve relevant memories and style snippets.
- Inject them compactly into the prompt to steer tone and recall details.

## Usage (CLI Concept)

- `ingest`: parse raw exports into processed JSONL.
- `mem`: extract/update memories and build the index.
- `chat`: start a local chat with a selected persona.
- `wipe`: remove a persona’s data/adapters.

Example
```
persona-you ingest --person "Alice" --source data/raw/Alice/
persona-you mem --person "Alice"
persona-you chat --person "Alice"
```

## Ethics and Limits

- Personal fun is fine; do not use this to deceive or harm.
- Do not produce or store sensitive data without explicit consent.
- Consider adding watermarks or signature phrases that identify the bot as simulated.

## Roadmap

- Parsers for common export formats (WA/iMessage variants)
- Out-of-the-box Ollama backend + prompt templates
- Optional LoRA trainer and adapter loader per persona
- Simple web UI on top of the CLI
- One-command export/wipe for portability and privacy

## Status

Project scaffold and README. Implementation to follow. If you want me to create the initial scripts and CLI skeleton, say “scaffold it.”
