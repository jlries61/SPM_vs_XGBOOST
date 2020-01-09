import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import os
import shutil
import matplotlib.pyplot as plt
from scipy import stats

def df_anyobj(df):
  anyobj = False
  for varname in df.columns:
    if df[varname].dtype == "object":
      anyobj = True
      break
  return anyobj

def expandClass(inframe, varlist):
  outframe = inframe.copy()
  for varname in inframe.columns:
    if inframe[varname].dtype == "object":
      varlist.add(varname)
  for varname in varlist:
    values = inframe[varname]
    cats = values.unique()
    for cat in cats:
      dummy = list()
      for value in values:
        if pd.isnull(cat) and pd.isnull(value):
          dummy.append(1)
        elif value == cat:
          dummy.append(1)
        else:
          dummy.append(0)
      if pd.isnull(cat):
        name = varname + "_miss"
      else:
        name = varname + "_" + str(cat)
      outframe[name] = pd.Series(dummy)
    outframe.drop(varname, axis=1, inplace=True)
  return outframe

def fileparts(path):
    folder_ = os.path.dirname(path)
    file_ = os.path.basename(path).split('.')[0]
    ext_ = os.path.splitext(path)[1]
    return folder_, file_, ext_


def fbb(s, n=12, t='l'):  # fill by blanks
    if n <= len(s):
        return s
    bl = ''
    for i in range(n - len(s)):
        bl += ' '
    if t == "l":
        s = bl+s
    if t == 'r':
        s = s+bl
    return s


def get_dict_row(dict_input, row):
    dict_output = {}
    for key in dict_input.keys():
        dict_output[key] = dict_input[key][row]
    return dict_output


def copy_and_delete(source_filename, destination_filename, rem_source=True):

    if os.path.isfile(destination_filename):
        os.remove(destination_filename)

    if os.path.isfile(source_filename):
        shutil.copyfile(source_filename, destination_filename)
        if rem_source:
            os.remove(source_filename)


def create_report(report_folder, models, dataset, note=""):
    report = list()

    report.append("========= Dataset name: " + dataset['Name'] + " =========\n")
    report.append(" - train part size: {}".format(dataset['N_obs_train_sam']) + "\n")
    report.append(" - test part size: {}".format(dataset['N_obs_test_sam']) + "\n")
    report.append(" - number of features: {}".format(dataset['N_features']) + "\n")
    report.append(" - number of classes: {}".format(dataset['N_classes']) + "\n")
    report.append("\n")
    report.append("\n")

    report.append(" --- Time elapsed during training ---\n")
    for model in models:
        report.append(" - " + model.perf['Name'] + ": {:.3f}".format(model.perf['TrainingTime']) + " seconds\n")
    report.append("\n")
    report.append("\n")

    report.append(" --- Individual AUCs ---\n")
    for model in models:
        report.append(" - " + model.perf['Name'] + ": {:.3f}".format(model.perf['AUC']) + "\n")
    report.append("\n")
    report.append("\n")

    report.append(" --- Performance for test set ---\n")
    for model in models:
        report.append("\n")
        report.append(" --- " + model.perf['Name'] + " ---\n")
        report.append("\n")
        report.append(model.perf['StatsTxt'])

    if not os.path.isdir(report_folder):
        os.mkdir(report_folder)

    f_report = open(report_folder + "/report" + note + ".txt", "w")
    for line in report:
        f_report.writelines(line)
    f_report.close()

    plt.clf()
    for model in models:
        plt.plot(1-model.perf['ROC_Specificity'], model.perf['ROC_Sensitivity'], model.perf['Color'], linewidth=2, label="AUC={:6.4f}, ".format(model.perf['AUC']) + model.perf['Name'])
    plt.xlabel('False Positive Rate (1-Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.title('ROC (Dataset: ' + dataset['Name'] + ')')
    plt.legend(loc=4)
    plt.grid(True)
    plt.savefig(report_folder + "/roc_curves" + note + ".png")


def get_common_stats(report_folder, models_lists, dataset, note):
    n_model = len(models_lists)
    n_sam = dataset['N_data_samples']
    model_names = list()
    for model_list in models_lists:
        model_names.append(model_list[0].perf['Name'])

    auc = np.zeros((n_sam, n_model))
    fp = np.arange(0, 1.01, 0.01)
    tp = np.zeros((len(fp), n_sam))

    plt.clf()
    for i in range(n_model):
        for j in range(n_sam):
            perf = models_lists[i][j].perf
            if np.isnan(perf['AUC']):
                continue
            auc[j, i] = perf['AUC']
            sensitivity = perf['ROC_Sensitivity']
            specificity = perf['ROC_Specificity']
            ispec = 1-specificity
            plt.plot(ispec, sensitivity, perf['Color'], linewidth=0.5, alpha=0.4)
            tp[:, j] = np.interp(fp, ispec, sensitivity)
        tp_mean = np.mean(tp, axis=1)
        plt.plot(fp, tp_mean, perf['Color'], linewidth=2,
                 label="AUC={:6.4f}, ".format(np.mean(auc[:, i])) + model_names[i])

    plt.xlabel('False Positive Rate (1-Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.title('ROC (Dataset: ' + dataset['Name'] + ')')
    plt.legend(loc=4)
    plt.grid(True)
    plt.savefig(report_folder + dataset['Name'] + "_roc_curves" + note + ".png")

    auc_stats = {'Mean ': np.mean(auc, axis=0), 'Min  ': np.min(auc, axis=0), 'Max  ': np.max(auc, axis=0),
                 'Range': np.max(auc, axis=0)-np.min(auc, axis=0), 'Std  ': np.std(auc, axis=0)}

    time_sam = np.zeros((n_sam, n_model))
    for i in range(n_model):
        for j in range(n_sam):
            time_sam[j, i] = models_lists[i][j].perf['TrainingTime']
    time_mean = np.mean(time_sam, 0)

    report = list()
    report.append("========= Dataset name: " + dataset['Name'] + " =========\n")
    report.append(" - train part size: {}".format(dataset['N_obs_train_sam']) + "\n")
    report.append(" - test part size: {}".format(dataset['N_obs_test_sam']) + "\n")
    report.append(" - number of features: {}".format(dataset['N_features']) + "\n")
    report.append(" - number of classes: {}".format(dataset['N_classes']) + "\n")
    report.append(" - number of data samples: {}".format(dataset['N_data_samples']) + "\n")
    report.append("\n")
    report.append("\n")
    report.append("========= Average time elapsed during training (sec) =========\n")
    line1 = '    '
    line2 = 'Time'
    for i in range(n_model):
        line1 += fbb(model_names[i], 12)
        line2 += '{:12.3f}'.format(time_mean[i])
    report.append(line1 + "\n")
    report.append(line2 + "\n")
    report.append("\n")
    report.append("\n")
    report.append("========= Individual AUCs =========\n")
    line1 = '         '
    for i in range(n_model):
        line1 += fbb(model_names[i], 12)
    report.append(line1 + "\n")
    for i in range(n_sam):
        line2 = fbb("Sample#" + str(i+1), 9, 'r')
        for j in range(n_model):
            line2 += '{:12.3f}'.format(auc[i, j])
        report.append(line2 + "\n")
    report.append("\n")
    report.append("\n")
    report.append("========= Summary =========\n")
    line1 = '     '
    for i in range(n_model):
        line1 += fbb(model_names[i], 12)
    report.append(line1 + "\n")
    for key in auc_stats.keys():
        line2 = key
        for i in range(n_model):
            line2 += '{:12.3f}'.format(auc_stats[key][i])
        report.append(line2 + "\n")
    report.append("\n")
    report.append("\n")
    for i in range(0, n_model-1):
        for j in range(i+1, n_model):
            t, p = stats.ttest_rel(auc[:, i], auc[:, j])
            report.append("========= Paired t-Test (" + model_names[i] + " <-> " + model_names[j] + ") =========\n")
            report.append("t = {:.4f}".format(t) + "\n")
            report.append("p = {:.4e}".format(p) + "\n")
            if p <= 0.05:
                report.append("Mean difference is significant.\n")
            else:
                report.append("Mean difference is NOT significant.\n")
            report.append('\n')

    f_report = open(report_folder + dataset['Name'] + "_summary_report" + note + ".txt", "w")
    for line in report:
        f_report.writelines(line)
    f_report.close()
