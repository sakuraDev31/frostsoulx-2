from pathlib import Path
import re

path = Path('/home/ubuntu/frostsoulx/app/src/main/kotlin/dev/vxs/frostsoulx/ui/menu/PlayerMenu.kt')
text = path.read_text()
clean = re.sub(r'//.*', lambda match: ' ' * len(match.group(0)), text)
clean = re.sub(r'/\*.*?\*/', lambda match: ''.join('\n' if ch == '\n' else ' ' for ch in match.group(0)), clean, flags=re.S)
clean = re.sub(r'"(?:\\.|[^"\\])*"', lambda match: ' ' * len(match.group(0)), clean)
depth = 0
stack = []
for number, line in enumerate(clean.splitlines(), 1):
    for character in line:
        if character == '{':
            depth += 1
            stack.append(number)
        elif character == '}':
            depth -= 1
            if stack:
                stack.pop()
    if 900 <= number <= 1060:
        print(f'{number:4}: depth={depth:3} {line[:120]}')
print(f'FINAL_DEPTH={depth}')
print('UNMATCHED_OPENINGS=' + ','.join(map(str, stack)))
