import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import DATA_FILE, NAMES_FILE, RANDOM_STATE, TEST_SIZE, TARGET


def load_column_names() -> list[str]:
    names = []
    for line in NAMES_FILE.read_text().splitlines():
        if line.strip().endswith("continuous."):
            names.append(line.rsplit(":", 1)[0].strip())
    return names + [TARGET]


def load_spambase() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, header=None, names=load_column_names())


def clean_spambase(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(keep="first").reset_index(drop=True)


def get_train_test():
    df = clean_spambase(load_spambase())
    X = df.drop(columns=TARGET)
    y = df[TARGET]
    return train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )
