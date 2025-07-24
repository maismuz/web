import re

with open('apps/contratamuz/templates/contratamuz/servicos.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Encontrar todos os blocos
blocks = re.findall(r'({%\s*block\s+\w+\s*%}|{%\s*endblock\s*%})', content)
for i, block in enumerate(blocks):
    line_num = content[:content.find(block)].count('\n') + 1
    print(f'Linha {line_num}: {block}')
