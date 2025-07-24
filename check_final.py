import re

with open('apps/contratamuz/templates/contratamuz/servicos.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Verificar estrutura de blocos
block_pattern = r'{%\s*block\s+(\w+)\s*%}'
endblock_pattern = r'{%\s*endblock\s*%}'

blocks = re.findall(block_pattern, content)
endblocks = len(re.findall(endblock_pattern, content))

print(f"Blocos encontrados: {blocks}")
print(f"Total de blocos abertos: {len(blocks)}")
print(f"Total de blocos fechados: {endblocks}")

if len(blocks) == endblocks:
    print("✅ Estrutura de blocos está correta!")
else:
    print("❌ Problema na estrutura de blocos!")
    
# Verificar se há caracteres especiais ou problemas
lines = content.split('\n')
print(f"Total de linhas: {len(lines)}")

# Verificar linha 190 especificamente
if len(lines) >= 190:
    print(f"Linha 190: '{lines[189]}'")
else:
    print("Arquivo tem menos de 190 linhas")
