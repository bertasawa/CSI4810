# CSI4810

Spam detection on the UCI Spambase dataset (4,601 emails, 57 word and character features). The data ships with the repo in `spambase/`.

## Setup

Python 3.12 works. Run these from the repo root.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows CMD
.venv\Scripts\Activate.ps1      # Windows PowerShell
source .venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

## Run order

Open the notebooks from the `notebooks/` folder and run each one top to bottom, in this order. Each part saves its tables to results/part1 through results/part4 and its figures to figures/part1 through figures/part4.

| Part | Notebook | What it covers |
|---|---|---|
| 1 | `01_data_eda.ipynb` | Loading, cleaning, EDA and the train/test split |
| 2 | `02_Logistic_DecisionTree.ipynb` | Logistic regression and decision tree |
| 3 | `03_RF_KNN.ipynb` | Random Forest and KNN, tuning and decision thresholds |
| 4 | `04_model_comparison.ipynb` | Comparing all models, confusion matrices, FP/FN and error analysis, limitations |

Part 4 reads what Parts 2 and 3 save, so run it last. The seed is 42 everywhere (`src/config.py`), and every part takes its split from `get_train_test()` in `src/data.py`. That way all models get scored on the same 842 test emails.
