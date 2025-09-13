## 🧭 Breadth-First Search (BFS) for SSML

### Why BFS?
BFS explores the tree **level by level**:
- Useful for **level summaries** (e.g., list all top-level blocks under `<speak>`),
- **Diagnostics/visualization** (what’s the structure by depth?),
- Some **validations** that rely on relative depth or “first seen at level…”.

### How it works
- Use a **queue** (FIFO).
- Start with `(root, depth=0)`.
- Repeatedly pop from the queue, then push each child with `depth+1`.

### When BFS vs DFS?
- **DFS**: natural for reading order, transformations, and inheritance.
- **BFS**: natural for **level-order outputs**, **breadth summaries**, and **first-occurrence by depth** tasks.

### Complexity
- **Time**: `O(N)` nodes
- **Space**: up to `O(W)` where `W` is max width (most nodes on any level).

### Pitfalls
- BFS alone doesn’t handle **reading order** (text/tail) correctly.
- You still need a **separate pass** for text flattening or style inheritance.
- Be explicit about how you represent “text nodes” (ElementTree keeps text as fields, not separate nodes).