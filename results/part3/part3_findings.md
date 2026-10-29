# Part 3 findings

Random Forest
Chosen parameters: {'max_depth': None, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'n_estimators': 200}
Mean outer-fold AP: 0.9762 before tuning and 0.9767 after tuning (change +0.0005).
Test at 0.5: accuracy 0.9430, precision 0.9364, recall 0.9196, F1 0.9279, AP 0.9841, ROC-AUC 0.9897.
Conservative threshold 0.735000: FP/FN changed from 21/27 to 2/56.
Conservative test precision 0.9929; recall 0.8333.
98% precision target met on test: True.

KNN
Chosen parameters: {'knn__n_neighbors': 21, 'knn__p': 1, 'knn__weights': 'distance'}
Mean outer-fold AP: 0.9072 before tuning and 0.9618 after tuning (change +0.0546).
Test at 0.5: accuracy 0.9169, precision 0.9618, recall 0.8244, F1 0.8878, AP 0.9684, ROC-AUC 0.9802.
Conservative threshold 0.633226: FP/FN changed from 11/59 to 5/86.
Conservative test precision 0.9804; recall 0.7440.
98% precision target met on test: True.

Scaling changed default KNN mean CV AP by +0.1580.

These results describe this dataset and split. Fold variation is not a significance test. A better AP does not guarantee a better F1 or recall at 0.5. Compare all metrics in the test table.

Limitations: historical data, one fixed test split, donor-specific non-spam vocabulary, conflicting labels and a finite parameter grid. Matching feature rows are grouped, but related senders or threads cannot be identified from the available features. Part 1 already explored the full dataset; the model grids here were fixed before checking test outcomes. Thresholds may behave differently on a new inbox, and the precision target is not a guarantee. No original email text is available to verify the reasons for individual errors.

Part 4 can combine test_metrics.csv and test_predictions.csv with Part 2 results from the same split.
