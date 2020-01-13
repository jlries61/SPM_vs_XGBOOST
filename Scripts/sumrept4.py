import os
import pandas as pd
import re
from sklearn.metrics import roc_auc_score

fields = ["Name", "N Replications", "N Features", "N Learn", "N Holdout",
          "Avg ROC (TN)", "Avg ROC (XGB)", "StdDev ROC (TN)", "Avg Delta_ROC", "Min Delta ROC",
          "Max Delta ROC", "StdDev Delta ROC"]
SPREAD = "../Datasets4.xlsx"
OUTFILE = "tn_vs_xgb_sumrept4.xlsx"
REPTDIR = "../Reports/RGBOOST4"
DATADIR = "../Data/Classification"
SLASH = "/"
MODSET = "_RGLs-0_INF-0.0_SUBS-1.0_LR-0.1_DEPTH-7_PREDS-500_NTREES-400"
xgb_filename_root = "xgb_score_test_"
scorenames = ["Class", "Prob"]
summary = pd.DataFrame(columns=fields)

dsl = pd.read_excel(SPREAD)
for i in dsl.index:
  dataname = dsl.loc[i, "Name"]
  dirname = REPTDIR + "/" + dataname + MODSET
  if not os.path.isdir(dirname):
    continue
  row = dict()
  nrepl = dsl.loc[i, "N_data_samples"]
  row["Name"] = dataname
  row["N Replications"] = nrepl
  row["N Features"] = dsl.loc[i, "N_features"]
  datadir = DATADIR + SLASH + dataname + SLASH + "SAMPLES4"
  reptdir = REPTDIR + SLASH + dataname + MODSET
  trainfile1 = datadir + SLASH + "data_train_1.csv"
  holdfile1 = datadir + SLASH + "data_hold_1.csv"
  traindata = pd.read_csv(trainfile1, low_memory=False)
  holddata = pd.read_csv(holdfile1, low_memory=False)
  row["N Learn"] = len(traindata.index)
  row["N Holdout"] = len(holddata.index)
  del traindata, holddata
  rept = REPTDIR + SLASH + dataname + "_summary_report" + MODSET + ".txt"
  roc = pd.DataFrame(columns=["TN", "XGB", "Delta"])
  besttn = -1
  with open(rept) as fh:
    for line in fh:
      if re.match("^Mean ", line):
        values = line.split()
        values.pop(0)
        nval = len(values)
        maxroc_tn = 0
        for i in range(nval):
          if i == 2:
            continue
          value = float(values[i])
          if value > maxroc_tn:
            besttn = i
            maxroc_tn = value
        break
  tn_filename_root = ""
  if besttn == 0:
    tn_filename_root = "treenet_score_test_"
  elif besttn == 1:
    tn_filename_root = "treenet2_score_test_"
  elif besttn == 3:
    tn_filename_root = "treenetx_score_test_"
  elif besttn == 4:
    tn_filename_root = "treenet2x_score_test_"
  for irepl in range(1, nrepl):
    roc_row = dict()
    tn_score_file = reptdir + SLASH + tn_filename_root + str(irepl) + ".csv"
    xgb_score_file = reptdir + SLASH + xgb_filename_root + str(irepl) + ".csv"
    tn_scores = pd.read_csv(tn_score_file, names=scorenames)
    xgb_scores = pd.read_csv(xgb_score_file, names=scorenames)
    roc_row["TN"] = roc_auc_score(tn_scores["Class"], tn_scores["Prob"])
    roc_row["XGB"] = roc_auc_score(xgb_scores["Class"], xgb_scores["Prob"])
    roc_row["Delta"] = roc_row["TN"] - roc_row["XGB"]
    roc = roc.append(roc_row, ignore_index=True)
  row["Avg ROC (TN)"] = roc["TN"].mean()
  row["Avg ROC (XGB)"] = roc["XGB"].mean()
  row["StdDev ROC (TN)"] = roc["TN"].std()
  row["Avg Delta_ROC"] = roc["Delta"].mean()
  row["Min Delta ROC"] = roc["Delta"].min()
  row["Max Delta ROC"] = roc["Delta"].max()
  row["StdDev Delta ROC"] = roc["Delta"].std()
  del roc
  summary = summary.append(row, ignore_index=True)
summary.to_excel(OUTFILE, index=False)
