import json
from pathlib import Path
p = Path('NUTRITION (2) FINAL.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
for idx in [146,147,148,149,150,151,152,153,154,155,165,166,167,168,169,170,178,179,180,181,182]:
    cell = nb['cells'][idx]
    print('--- CELL', idx, '---')
    print(''.join(cell.get('source', [])))
