got it 👍 — here’s a single clean Markdown block for your notes on <say-as> with no extra Python comments. you can paste this directly into your notes.

⸻


## 🗣️ `<say-as>` — Interpretation of Text

### Purpose
`<say-as>` tells the TTS engine **how to interpret and pronounce** the enclosed text.  
Without it, the engine uses defaults (e.g., “123” → *one hundred twenty-three*).  
With `<say-as>`, you can override this behavior: digits, characters, dates, phone numbers, etc.

---

### Common `interpret-as` values

1. **`characters`** → spell out each character.  
   ```xml
   <say-as interpret-as="characters">HTML</say-as>

🔊 H T M L
	2.	digits → speak each digit separately.

<say-as interpret-as="digits">1234</say-as>

🔊 one two three four

	3.	cardinal → default numeric reading.

<say-as interpret-as="cardinal">1234</say-as>

🔊 one thousand two hundred thirty-four

	4.	ordinal → ordinal numbers.

<say-as interpret-as="ordinal">5</say-as>

🔊 fifth

	5.	date → interpret as a date.
Attributes:
	•	format (e.g., mdy, dmy, ymd)
	•	detail (optional: year only, month+year, etc.)

<say-as interpret-as="date" format="mdy">10/05/2025</say-as>

🔊 October fifth twenty twenty-five

	6.	time → interpret as time of day.

<say-as interpret-as="time" format="hms12">12:30pm</say-as>

🔊 twelve thirty p m

	7.	telephone → read as phone number.

<say-as interpret-as="telephone">8005551212</say-as>

🔊 eight zero zero five five five one two one two

	8.	currency → interpret as money.

<say-as interpret-as="currency">99.99</say-as>

🔊 ninety-nine dollars and ninety-nine cents

⸻

Why important?
	•	Prevents mispronunciations of acronyms, numbers, IDs, dates.
	•	Makes speech output clearer and listener-friendly.
	•	Parsing/flattening tasks need to simulate how text would expand.

⸻

Implementation Notes
	•	During flattening, replace <say-as> content with a transformed version based on interpret-as.
	•	If unknown value → fallback to the original text.
	•	Real TTS engines handle language-specific rules; in practice, we use mock transformations for testing.
