## 🔄 `<sub>` — Text Substitution

### Purpose
`<sub>` lets you display one text but have the TTS **pronounce a substitute**.  
It is often used for **abbreviations**, **acronyms**, or **symbols**.

### Attributes
- **`alias`** → the substitution text that will be spoken.

### Behavior
- The **inner text** is displayed, but the **alias** is spoken instead.
- If no `alias` is provided, the inner text is spoken normally.

### Examples
```xml
<speak>
  I live in <sub alias="New York City">NYC</sub>.
</speak>