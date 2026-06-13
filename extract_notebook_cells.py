import json
from pathlib import Path
p = Path('NUTRITION (2) FINAL.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
keys = [
    'data=pd.read_csv("Final_data_with_goal.csv")',
    'LogisticRegression',
    'model_logreg =',
    'y2= data[\'Calories\']',
    'RandomForestRegressor',
    'joblib.dump(model_logreg',
    'joblib.dump(model_reg',
]
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell.get('source', []))
    if any(key in src for key in keys):
        print('--- CELL', i, '---')
        print(src)
