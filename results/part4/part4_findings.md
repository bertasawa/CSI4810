# Part 4 findings (draft text for the report)

Everything here comes from `notebooks/04_model_comparison.ipynb`, run on all four models from Parts 2 and 3 plus the majority baseline. Figure numbers below match the file names in `figures/part4/`. The report will renumber them.

## Tables for the report

TABLE I. Test results on the 842 held out emails at threshold 0.5. Brackets are 95% bootstrap intervals.

| Model | Accuracy | Bal. acc. | Precision | Recall | Specificity | F1 [95% CI] | AP [95% CI] | FP | FN |
|---|---|---|---|---|---|---|---|---|---|
| Majority baseline | 0.601 | 0.500 | 0.000 | 0.000 | 1.000 | 0.000 | 0.399 | 0 | 336 |
| Logistic Regression | 0.935 | 0.930 | 0.930 | 0.905 | 0.955 | 0.917 [0.894, 0.937] | 0.962 [0.941, 0.979] | 23 | 32 |
| Decision Tree | 0.909 | 0.903 | 0.894 | 0.875 | 0.931 | 0.884 [0.857, 0.909] | 0.887 [0.851, 0.920] | 35 | 42 |
| Random Forest | 0.943 | 0.939 | 0.936 | 0.920 | 0.958 | 0.928 [0.906, 0.948] | 0.984 [0.974, 0.992] | 21 | 27 |
| KNN | 0.917 | 0.901 | 0.962 | 0.824 | 0.978 | 0.888 [0.859, 0.913] | 0.968 [0.949, 0.982] | 11 | 59 |

TABLE II. Five fold CV on the training set, mean ± standard deviation across folds. Tuned models use nested CV.

| Model | F1 | AP | Recall |
|---|---|---|---|
| Logistic Regression | 0.899 ± 0.012 | 0.945 ± 0.017 | 0.882 ± 0.027 |
| Decision Tree | 0.889 ± 0.013 | 0.865 ± 0.018 | 0.874 ± 0.024 |
| Random Forest | 0.932 ± 0.014 | 0.977 ± 0.011 | 0.919 ± 0.023 |
| KNN | 0.856 ± 0.018 | 0.962 ± 0.008 | 0.771 ± 0.034 |

## Figure captions

**Fig. 1** (`01_confusion_matrices.png`). Confusion matrices at threshold 0.5. Each cell shows the count and the share of its true class.

**Fig. 2** (`02_metric_comparison.png`). Test scores with 95% bootstrap intervals. The majority baseline is in Table I.

**Fig. 3** (`03_roc_pr_curves.png`). ROC and precision and recall curves, zoomed in on the region where the models differ. Dots mark threshold 0.5 and stars mark the strict threshold, which only Random Forest and KNN have.

**Fig. 4** (`04_fp_fn_tradeoff.png`). False alarms (left) and missed spam (right) at the default and strict thresholds.

**Fig. 5** (`05_error_profile.png`). Share of emails in each outcome group that contain each token, for Random Forest at threshold 0.5.

**Fig. 6** (`06_donor_word_false_alarms.png`). False alarm rate on real emails with and without the donor words george, hp, hpl and 650. Error bars are Wilson 95% intervals.

## Results and discussion

Table I and Fig. 2 compare the four models on the 842 test emails. Random Forest is the strongest on almost every metric, with F1 0.928 [0.906, 0.948] and AP 0.984 [0.974, 0.992], and five fold CV agrees (Table II). Logistic regression is a close second at F1 0.917. KNN gets the best precision (0.962) and specificity (0.978), but it pays for that with the lowest recall, 0.824. The decision tree is weakest overall, with the lowest AP (0.887) and the most errors, 35 false alarms and 42 misses. All four are far above the majority baseline, which reaches 0.601 accuracy by calling every email real and doesn't catch a single spam.

McNemar's test [3] with a Holm correction [4] separates three of the six pairs. Random Forest beats KNN (Holm p = 0.036) and the tree (Holm p = 0.0002), and logistic regression beats the tree (Holm p = 0.041). Random Forest and logistic regression can't be told apart at the 0.5 threshold (p = 0.35, F1 difference [-0.031, +0.009]). Random Forest does rank emails better, though. Its AP lead over logistic regression is 0.022 [0.009, 0.039], and its curves in Fig. 3 sit above the others almost everywhere.

That ranking edge matters once the threshold moves (Fig. 4). Part 3's strict rule picks the highest recall with at least 98% precision on out of fold predictions, and for Random Forest it cuts false alarms from 21 to 2 while missed spam rises from 27 to 56. The trade pays off whenever one lost real email costs more than about 1.5 missed spams, which is a low bar for most people. The same rule finds no threshold at all for logistic regression or the tree, since their out of fold precision tops out at 97.7% and 92.0%. At its strict threshold Random Forest beats KNN at 0.5 on both errors at once (2 vs 11 false alarms, 56 vs 59 misses), so it's the setup we'd recommend.

## Error analysis

Most test emails are easy. 712 of the 842 fool nobody, while 20 fool all four models (6 real emails and 14 spams). Random Forest has only 5 solo mistakes. The tree's 27 solo mistakes are mostly false alarms, and KNN's 25 are almost all missed spam. KNN struggles with short spam in particular. It catches 59% of spam with four or fewer tracked words, against 71% to 75% for the other models, because sparse spam sits right among real emails in its distance space.

Fig. 5 shows what Random Forest's mistakes look like. The real emails it flags read like ads. 43% of them contain "free" against 11% of the real mail it keeps, 33% contain "remove" against 1%, and almost none contain "hp" or "george", the strongest real mail signals in the data. Missed spam goes the other way. It's short and quiet, with a median of 4 tracked words against 10 for caught spam, and it rarely uses the classic tokens ("remove" shows up in 4% of missed spam and 51% of caught spam). One real email (row 2312) contains nearly every spam token plus a 214 character run of capitals, and all four models give it at least 0.98. A person skimming it might flag it too.

The biggest pattern comes from where the data came from. All real email in Spambase belongs to one HP Labs employee, and the UCI notes warn that words like "george" and "650" only make sense for a personal filter [5]. When the real test emails are split on george, hp, hpl and 650 (Fig. 6), every model flags the ones without a donor word far more often. Random Forest goes from 0.7% to 8.3%, logistic regression from 0.7% to 9.2%, the tree from 3.2% to 11.4% and KNN from 0.4% to 4.4%, and the Wilson intervals [6] never overlap. So each headline false alarm rate averages two very different groups, and a new user's mail would sit in the worse one. Those emails aren't spammier, either. In the training data they contain "$" and "business" less often than the donor's own mail. The donor words act like a pass that lets the models forgive a "$" or a "free", and logistic regression says so outright. Its two largest weights are george (-4.0) and hp (-2.5), bigger than its top spam signal, "$" (+1.2).

Dropping those four words and refitting every model with its final settings hits the simpler models hardest. Mean CV AP falls by 0.014 for logistic regression and 0.033 for the tree, but only about 0.005 for Random Forest and KNN. For Random Forest the two false alarm rates move toward each other, from 0.7% and 8.3% to 2.2% and 6.6%, without meeting.

## Limitations and responsible use

Every result here describes one inbox. The real email comes from one person at HP Labs in 1999, and Fig. 6 shows the filters are roughly twice as error prone on mail that doesn't look like theirs. The spam is old too. The UCI notes describe it as ads, money making schemes, chain letters and porn, while spam today leans on phishing links and images, which 57 word and character counts can't see. A misspelled word gets past these features, and word order and context are gone.

The labels reflect one person's judgment. Three pairs of identical feature rows even carry opposite labels, and without the raw text we can't check whether some errors are really labeling mistakes. And everything comes from one split of 842 emails. The bootstrap intervals cover resampling this dataset, not a different inbox.

These results aren't a ready spam filter. A false alarm hides real mail, so a filter like this should only move mail to a folder people can review, never delete it. The strict threshold is the safer default, and only Random Forest and KNN rank emails well enough to support one. The donor word result is a fairness problem in small form. Users whose mail doesn't look like the training inbox get no pass, and if their normal email mentions prices or deals they'll be flagged far more often. A deployed filter would also read private mail, which needs consent and careful handling.

Next steps. (1) Train and test on a newer corpus with many users, such as Enron Spam or the SpamAssassin public corpus, and hold whole users out of training. (2) Use the raw text with TF-IDF and a linear model, plus header and link features. (3) Blind the donor words as the UCI notes suggest, and report the subgroup false alarm rate next to the overall one. (4) Pick thresholds from real error costs and check calibration.

## Notes for whoever assembles the report

If space is tight, keep Fig. 1, Fig. 4 and Fig. 6. Table I covers most of what Fig. 2 shows, and Fig. 3 can move to an appendix.

Part 2's notebook saves summary scores but not predictions for each email. So Part 4 rebuilds its two models from the settings in that notebook and stops if they don't reproduce `results/02_model_metrics.csv` exactly. If Part 2 ever changes its models, update `PART2_MODELS` in section 2 of the Part 4 notebook to match.

Suggested contribution line for Part 4. Built `04_model_comparison.ipynb`, with bootstrap intervals and McNemar tests for the model comparison, the false positive and false negative analysis across thresholds, the error profiles, and the donor word subgroup check with its ablation. Wrote the error analysis and limitations text.

The references used above are in IEEE style, and they'll need renumbering to fit the full report.

[1] B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*. New York, NY, USA: Chapman & Hall, 1993.

[2] T. Saito and M. Rehmsmeier, "The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets," *PLoS ONE*, vol. 10, no. 3, Art. no. e0118432, 2015.

[3] T. G. Dietterich, "Approximate statistical tests for comparing supervised classification learning algorithms," *Neural Comput.*, vol. 10, no. 7, pp. 1895-1923, 1998.

[4] S. Holm, "A simple sequentially rejective multiple test procedure," *Scand. J. Statist.*, vol. 6, no. 2, pp. 65-70, 1979.

[5] M. Hopkins, E. Reeber, G. Forman, and J. Suermondt, "Spambase," UCI Machine Learning Repository, 1999. doi: 10.24432/C53G6X.

[6] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *J. Amer. Statist. Assoc.*, vol. 22, no. 158, pp. 209-212, 1927.
