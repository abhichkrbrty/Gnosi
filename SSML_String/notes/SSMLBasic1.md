SSML basics: structure & parsing.
we’ll cover the root <speak>, common child tags, attributes, and how to traverse/inspect the tree. then you’ll run one script locally.

concept (what you need to know)
	•	SSML is XML: a single root element <speak> … </speak>.
	•	Elements (tags) can contain:
	•	text (el.text) before the first child,
	•	children (for c in el:),
	•	tail text (c.tail) that appears immediately after a child, before the next sibling/closing tag.
	•	Attributes are key/value strings (e.g., <voice name="en-US-JennyNeural"> has {"name": "en-US-JennyNeural"}).
	•	You typically:
	1.	parse into a tree,
	2.	walk the tree (DFS/BFS) to inspect or transform,
	3.	optionally flatten to text or compute metrics (we’ll do that too).