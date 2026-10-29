from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "spambase"
DATA_FILE = DATA_DIR / "spambase.data"
NAMES_FILE = DATA_DIR / "spambase.names"

FIGURES_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"

RANDOM_STATE = 42

TEST_SIZE = 0.20

TARGET = "spam"
