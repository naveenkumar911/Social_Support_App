import pandas as pd
from pathlib import Path
def parse_file(path):
    p = Path(path)
    if p.suffix.lower() in ['.csv']:
        df = pd.read_csv(path)
        return df.head(10).to_dict(orient='records')
    if p.suffix.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(path)
        return df.head(10).to_dict(orient='records')
    return {'info': 'file saved', 'path': str(path)}