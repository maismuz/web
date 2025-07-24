with open('apps/contratamuz/templates/contratamuz/servicos.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total de linhas: {len(lines)}")
print(f"Linha 190: '{lines[189].strip()}'")

# Verificar blocos
import re
content = ''.join(lines)

# Procurar todos os blocos
for match in re.finditer(r'{%\s*block\s+(\w+)\s*%}', content):
    line_num = content[:match.start()].count('\n') + 1
    block_name = match.group(1)
    print(f"Block '{block_name}' na linha {line_num}")

for match in re.finditer(r'{%\s*endblock\s*%}', content):
    line_num = content[:match.start()].count('\n') + 1
    print(f"Endblock na linha {line_num}")
