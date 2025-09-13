## 🔍 Depth-First Search (DFS) for SSML

### Why DFS for SSML?
SSML is XML, which forms a rooted **tree**:
- Each **element** (e.g., `<speak>`, `<p>`, `<s>`, `<prosody>`) is a node.
- Nodes can have **text**, **children**, and **tail** (text after a child, before the next sibling).
- Many SSML tasks are **hierarchical**: flattening to visible text, inheriting prosody/rate, validating nesting.
DFS follows the natural parent→children relationship, making it the default workhorse for:
- **Flattening text in reading order** (respecting text, children, and `tail`)
- **Attribute inheritance** (e.g., nested `<prosody>` overrides)
- **Structural validation** (e.g., disallowing invalid children inside certain tags)

### DFS Orders
- **Pre-order DFS** (most common for SSML): visit node, then recurse children (left→right).
- **Post-order**: visit children first, then the node (less common, used for aggregations).

### Reading Order (critical!)
To reproduce user-visible text properly, you must:
1. Read the node’s `.text` (if any)
2. DFS into each child (in document order)
3. After each child returns, read the child’s `.tail` (if any)

This gives: **text → child → child.tail → next child → …**

### Complexity
- **Time**: `O(N)` nodes (and text spans)
- **Space**: `O(H)` call stack for recursion, where `H` is tree height  
  (Iterative implementations use an explicit stack, similar complexity.)

### Common Pitfalls
- ❗ Ignoring `.tail` breaks natural reading order.
- ❗ Normalizing whitespace too early can lose intended pauses.
- ❗ Forgetting attribute inheritance (e.g., prosody) when aggregating styles.
- ❗ Very deep trees can hit recursion limits — prefer iterative DFS if needed.

### Minimal Rules of Thumb
- Use **pre-order DFS** for transformations/flattening.
- Always handle: `el.text`, **each** child, **each** child’s `tail`.
- Keep traversal pure; do formatting/normalization in separate steps to avoid bugs.