from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
languages = pd.read_csv(app_dir / "languages.csv")
jobs = pd.read_csv(app_dir / "jobs_app_1.csv")

