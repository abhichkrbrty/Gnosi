## 🔊 `<emphasis>` — Stressing Words in Speech

### Purpose
The `<emphasis>` tag tells the TTS engine to **stress certain words or phrases**.  
It affects **intonation and prominence**, making the enclosed text stand out.

---

### Attributes
- **`level`** → controls degree of emphasis
  - `"strong"` → more prominent (like italic+bold in speech)  
  - `"moderate"` / `"medium"` → default emphasis  
  - `"reduced"` → deemphasize (make less prominent)

---

### Examples
```xml
<speak>
  Normal text. 
  <emphasis level="strong">This is strongly emphasized.</emphasis> 
  <emphasis level="reduced">This is softened.</emphasis>
</speak>


🔊 Output (approximate):
	•	This is strongly emphasized → spoken with more force/stress.
	•	This is softened → spoken with less energy.

⸻

Why important?
	•	Helps control intonation in key phrases.
	•	Useful for dialogue, storytelling, accessibility (highlighting important parts).
	•	Parsing tasks should capture emphasis levels along with text.

⸻

Implementation Notes
	•	Treat <emphasis> as metadata, similar to <prosody>.
	•	In DFS traversal:
	•	If node is <emphasis>, add its level into the current style.
	•	Emphasis rarely changes timing, but influences style annotations.