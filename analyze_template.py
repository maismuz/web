with open('apps/contratamuz/templates/contratamuz/servicos.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
print(f"Total de linhas: {len(lines)}")

# Verificar se há duplicação
seen = set()
duplicates = []
for i, line in enumerate(lines, 1):
    if line in seen and line.strip():
        duplicates.append((i, line.strip()[:50]))
    seen.add(line)

if duplicates:
    print("Linhas duplicadas encontradas:")
    for line_num, content in duplicates:
        print(f"Linha {line_num}: {content}")
else:
    print("Nenhuma duplicação encontrada")

# Verificar blocos
import re
content = ''.join(lines)
block_starts = []
block_ends = []

for match in re.finditer(r'{%\s*block\s+(\w+)\s*%}', content):
    line_num = content[:match.start()].count('\n') + 1
    block_name = match.group(1)
    block_starts.append((line_num, block_name))

for match in re.finditer(r'{%\s*endblock\s*%}', content):
    line_num = content[:match.start()].count('\n') + 1
    block_ends.append(line_num)

print(f"\nBlocos encontrados:")
print(f"Block starts: {block_starts}")
print(f"Block ends: {block_ends}")

if len(block_starts) != len(block_ends):
    print(f"ERRO: {len(block_starts)} blocos abertos, {len(block_ends)} blocos fechados")
