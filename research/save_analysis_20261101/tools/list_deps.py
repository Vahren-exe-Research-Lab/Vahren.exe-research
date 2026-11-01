"""List hakushin_compat modules transitively imported by the save analysis tools."""
import ast, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(os.path.dirname(HERE), 'pkg', 'hakushin_compat')
seen, todo = set(), ['normal_save_body_and_tail']
while todo:
    m = todo.pop()
    if m in seen:
        continue
    seen.add(m)
    tree = ast.parse(open(os.path.join(PKG, m + '.py'), encoding='utf-8').read())
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom) and n.level == 1 and n.module:
            todo.append(n.module.split('.')[0])
        elif isinstance(n, ast.ImportFrom) and n.module and n.module.startswith('hakushin_compat.'):
            todo.append(n.module.split('.')[1])
print(sorted(seen))
bad = []
for m in sorted(seen):
    s = open(os.path.join(PKG, m + '.py'), encoding='utf-8').read()
    if 'C:\\' in s or 'Users' in s or '@' in s and 'gmail' in s:
        bad.append(m)
print('suspect', bad)
