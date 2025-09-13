def is_well_formed_markup(s: str) -> bool:
    """Very small checker for angle-bracket tags like <a> ... </a> and <br/>.
    Not a full XML validator—meant for practicing stacks.
    """
    stack = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] == "<":
            j = s.find(">", i+1)
            if j == -1:
                return False
            inside = s[i+1:j].strip()
            if not inside:
                return False
            if inside.startswith("/"):
                tag = inside[1:].strip()
                if not stack or stack[-1] != tag:
                    return False
                stack.pop()
            elif inside.endswith("/"):
                # self-closing; ok
                pass
            else:
                # start tag name up to first space
                name = inside.split()[0]
                stack.append(name)
            i = j + 1
        else:
            i += 1
    return len(stack) == 0
