import os
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import time
import funcs
import xgboost as xgb

class XGBoostModel(object):

    def __init__(self, report_note=""):
        self.test_type = 'Samples'  # Usual
        self.i_sample = -1
        self.perf = {'Name': 'xgBoost', 'Color': 'r-', 'ReportNote': report_note, 'SampleNote': ''}

        self.xgb_executable = 'xgboost'
        # Filenames
        self.filename_log = os.getcwd().replace('\\', '/') + "/xgb_output" +\
                            self.perf['ReportNote'] + ".txt"
        self.filename_model = os.getcwd().replace('\\', '/') + "/xgb_model" +\
                              self.perf['ReportNote'] + ".model"
        self.filename_cmd_train = os.getcwd().replace('\\', '/') + "/xgb_config" +\
                                  self.perf['ReportNote'] + ".conf"
        self.filename_train = os.getcwd().replace('\\', '/') + "/dataset_train.csv"
        self.filename_hold = os.getcwd().replace('\\', '/') + "/dataset_hold.csv"
        self.filename_score_test = os.getcwd().replace('\\', '/') + "/xgb_score_test" +\
                                   self.perf['ReportNote'] + ".csv"
        self.bf = {}
        self.backup_filenames()

        # General Parameters
        self.gen_booster = 'gbtree'
        self.gen_silent = '0'
        self.gen_nthread = '4'

        # Parameters for Tree Booster
        self.trb_eta = '0.3'
        self.trb_gamma = '0'
        self.trb_max_depth = '6'
        self.trb_min_child_weight = '1'
        self.trb_max_delta_step = '0'
        self.trb_subsample = '1'
        self.trb_colsample_bytree = '1'
        self.trb_colsample_bynode = '1'
        self.trb_lambda99 = '1'
        self.trb_alpha = '0'

        # Learning Task Parameters
        self.ltp_objective = 'binary:logistic'
        self.ltp_base_score = '0.5'
        self.ltp_eval_metric = 'logloss'
        self.ltp_seed = '0'

        # Command Line Parameters
        self.cli_use_buffer = '0'
        self.cli_num_round = '200'
        self.cli_save_period = '0'

    def backup_filenames(self):
        self.bf = {'filename_log': self.filename_log,
                   'filename_model': self.filename_model,
                   'filename_cmd_train': self.filename_cmd_train,
                   'filename_train': self.filename_train,
                   'filename_hold': self.filename_hold,
                   'filename_score_test': self.filename_score_test}

    def restore_filenames(self):
        self.filename_log = self.bf['filename_log']
        self.filename_model = self.bf['filename_model']
        self.filename_cmd_train = self.bf['filename_cmd_train']
        self.filename_train = self.bf['filename_train']
        self.filename_hold = self.bf['filename_hold']
        self.filename_score_test = self.bf['filename_score_test']

    def create_conf_file_train(self, format="", labelcol=-1):
        if self.test_type == "Samples":
            self.i_sample += 1
            self.perf['SampleNote'] = '_' + str(self.i_sample+1)

        opt_names = dir(self)

        lines = list()

        trainset = self.filename_train
        holdset = self.filename_hold
        if len(format) > 0:
            fmtstr = "?format=" + format
            trainset = trainset + fmtstr
            holdset = holdset + fmtstr
        if labelcol >= 0:
            fmtstr = "&label_column=" + str(labelcol)
            trainset = trainset + fmtstr
            holdset = holdset + fmtstr
        lines.append('# Filenames' + '\n')
        lines.append('data' + ' = ' + trainset + '\n')
        if self.filename_hold != "":
            lines.append('test:data' + ' = ' + holdset + '\n')

        lines.append('\n' + '# General Parameters' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "gen" and getattr(self, name) != "":
                lines.append(('_'.join(buf[1:len(buf)]).replace('99', '')) +
                             ' = ' + getattr(self, name) + '\n')

        lines.append('\n' + '# Tree Booster Parameters' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "trb" and getattr(self, name) != "":
                lines.append(('_'.join(buf[1:len(buf)]).replace('99', '')) + ' = ' +
                             getattr(self, name) + '\n')

        lines.append('\n' + '# Learning Task Parameters' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "ltp" and getattr(self, name) != "":
                lines.append(('_'.join(buf[1:len(buf)]).replace('99', '')) + ' = ' +
                             getattr(self, name) + '\n')

        lines.append('\n' + '# Command Line Parameters' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "cli" and getattr(self, name) != "":
                lines.append(('_'.join(buf[1:len(buf)]).replace('99', '')) + ' = ' +
                             getattr(self, name) + '\n')

        f = open(self.filename_cmd_train, "w")
        for line in lines:
            f.writelines(line)
        f.close()

    def train_model(self):
        time_start = time.time()
        os.system(self.xgb_executable + ' ' + self.filename_cmd_train + ' task=train' +
                  ' model_out=' + self.filename_model + ' 2>' + self.filename_log)
        time_end = time.time()
        self.perf['TrainingTime'] = time_end - time_start

    def test_model(self, itgt=0, convert_scores=True, csv=False):
        os.system(self.xgb_executable + ' ' + self.filename_cmd_train + ' task=pred' + ' model_in=' +
                  self.filename_model)

        if convert_scores:
            filename_score_test = os.getcwd().replace('\\', '/') + "/pred.txt"
            d_pred = np.loadtxt(filename_score_test, delimiter=",", skiprows=0, ndmin=2, dtype=float)
            dlm = " "
            if csv:
                dlm = ","
            d_test = np.loadtxt(self.filename_hold, delimiter=dlm, skiprows=0, ndmin=2, dtype=str)
            np.savetxt(self.filename_score_test, np.c_[d_test[:, itgt].astype(dtype=float),
                                                       d_pred[:, 0]], delimiter=',', fmt='%f')
            os.remove(filename_score_test)

    def clean_workspace(self):
         if os.path.isfile(self.filename_cmd_train):
             os.remove(self.filename_cmd_train)
         if os.path.isfile(self.filename_log):
            os.remove(self.filename_log)
         if os.path.isfile(self.filename_model):
            os.remove(self.filename_model)
         if os.path.isfile(self.filename_score_test):
             os.remove(self.filename_score_test)

    def prepare_replication(self, folder_to_save):
        if not os.path.isdir(folder_to_save):
            os.mkdir(folder_to_save)

        folder_, file_, ext_ = funcs.fileparts(self.filename_score_test)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_score_test, destination_file, rem_source=True)
        #self.filename_score_test = destination_file
        folder_, file_, ext_ = funcs.fileparts(self.filename_cmd_train)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_cmd_train, destination_file, rem_source=True)
        #self.filename_cmd_train = destination_file

    def make_classification_stats(self):
        d = np.loadtxt(self.filename_score_test, delimiter=",", skiprows=0, ndmin=2, dtype=float)
        y_targ = (d[:, 0])
        prob1 = d[:, 1]
        y_pred = np.zeros((len(prob1), 1))
        y_pred[prob1 >= 0.5] = 1

        cm = confusion_matrix(y_targ, y_pred)
        auc = roc_auc_score(y_targ, prob1)

        fpr, tpr, thresholds = roc_curve(y_targ, prob1)
        roc_sensitivity = tpr
        roc_specificity = 1 - fpr

        self.perf['ConfusionMatrix'] = cm
        self.perf['AUC'] = auc
        self.perf['ROC_Sensitivity'] = roc_sensitivity
        self.perf['ROC_Specificity'] = roc_specificity

        tp = cm[1, 1]
        fp = cm[0, 1]
        tn = cm[0, 0]
        fn = cm[1, 0]

        specificity = float(tn)/(tn + fp)
        sensitivity = float(tp)/(tp + fn)

        stats_txt = list()
        stats_txt.append(' Actual       Predicted Class                  Actual\n')
        stats_txt.append(' Class                    0            1        Total\n')
        stats_txt.append(' ----------------------------------------------------\n')
        stats_txt.append(' 0            {: 13.2f}{: 13.2f}{: 13.2f}\n'.format(cm[0, 0], cm[0, 1],
                                                                              cm[0, 0]+cm[0, 1]))
        stats_txt.append(' 1            {: 13.2f}{: 13.2f}{: 13.2f}\n'.format(cm[1, 0], cm[1, 1],
                                                                              cm[1, 0]+cm[1, 1]))
        stats_txt.append(' ----------------------------------------------------\n')
        stats_txt.append(' Pred. Tot.   {: 13.2f}{: 13.2f}{: 13.2f}\n'.format(cm[0, 0]+cm[1, 0],
                                                                              cm[0, 1]+cm[1, 1],
                                                                              cm[0, 0]+cm[1, 0]+
                                                                              cm[0, 1]+cm[1, 1]))
        stats_txt.append(' Correct      {: 13.5f}{: 13.5f}\n'.
                         format(float(cm[0, 0])/(cm[0, 0]+cm[0, 1]),
                                float(cm[1, 1])/(cm[1, 0]+cm[1, 1])))
        # stats_txt.append(' Success Ind. {: 13.5f}{: 13.5f}\n'.format())
        stats_txt.append(' Tot. Correct {: 13.5f}\n'.
                         format(float(cm[0, 0]+cm[1, 1])/(cm[0, 0]+cm[1, 0]+cm[0, 1]+cm[1, 1])))
        stats_txt.append('\n')
        stats_txt.append(' Specificity (True Ref): {: 7.5f},  Sensitivity (True Resp): {: 7.5f}\n'.
                         format(specificity, sensitivity))
        stats_txt.append(' False Reference: {: 7.5f},  False Response: {: 7.5f}\n'.
                         format(float(cm[1, 0])/(cm[1, 0]+cm[1, 1]),
                                float(cm[0, 1])/(cm[0, 0]+cm[0, 1])))
        stats_txt.append(' Reference = 0, Response = 1\n')
        stats_txt.append(' Approx Integrated ROC: {: 9.7f}'.format(auc) + "\n")

        self.perf['StatsTxt'] = stats_txt

