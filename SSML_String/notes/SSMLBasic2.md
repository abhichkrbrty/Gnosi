## ⏸️ The `<break>` Element in SSML

### Purpose
`<break>` inserts a **pause** in speech.  
It can be controlled by either **time** (milliseconds/seconds) or **strength** (qualitative levels).

### Attributes
- **`time`** → exact pause duration
  - `"500ms"`, `"1s"`, `"2000ms"`
- **`strength`** → relative pause
  - `"none"`, `"x-weak"`, `"weak"`, `"medium"`, `"strong"`, `"x-strong"`
  - The actual duration depends on the TTS engine.

### Behavior
- `<break time="500ms"/>` → pause for half a second.
- `<break strength="strong"/>` → engine chooses a longer pause.
- If both are given, **`time` usually takes precedence**.

### Why important?
- Adds **natural rhythm** to speech.
- Useful for **lists, commas, paragraph breaks**.
- In parsing tasks, we need to:
  1. **Detect `<break>`**.
  2. **Add its duration** into total speech time.
  3. Optionally represent it as a special token (e.g., `[PAUSE 0.5s]`).

### Example
```xml
<speak>
  Hello world. <break time="700ms"/> This sentence starts after a pause.
</speak>


## ⏸️ `<break>` — Strength vs Explicit Time

### Explicit Time
- Attribute: `time`
- Format: `"500ms"`, `"1s"`, `"2000ms"`
- Behavior: Always pauses for that exact duration.
- **Deterministic**: You control the exact pause length.

Example:
```xml
<break time="700ms"/>