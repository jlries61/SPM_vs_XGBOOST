import numpy as np
import os
import subprocess
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
import time
import xmltodict as xd
import funcs

class TreeNetModel(object):

    def __init__(self, report_note=""):
        self.test_type = 'Samples'  # Usual
        self.i_sample = -1
        self.perf = {'Name': 'TreeNet', 'Color': 'b-', 'ReportNote': report_note, 'SampleNote': ''}

        self.spm_executable = "spmu"
        self.filename_output = os.getcwd().replace('\\', '/') + "/spm_output" +\
            self.perf['ReportNote'] + ".dat"
        self.filename_grove = os.getcwd().replace('\\', '/') + "/treenet_model" +\
            self.perf['ReportNote'] + ".grv"
        self.filename_train = os.getcwd().replace('\\', '/') + "/dataset_train.csv"
        self.filename_test = os.getcwd().replace('\\', '/') + "/dataset_test.csv"
        self.filename_hold = os.getcwd().replace('\\', '/') + "/dataset_hold.csv"
        self.filename_score_train = os.getcwd().replace('\\', '/') + "/treenet_score_train" +\
            self.perf['ReportNote'] + ".csv"
        self.filename_score_test = os.getcwd().replace('\\', '/') + "/treenet_score_test" +\
            self.perf['ReportNote'] + ".csv"
        self.filename_cmd_train = os.getcwd().replace('\\', '/') + "/treenet_train" +\
            self.perf['ReportNote'] + ".cmd"
        self.filename_cmd_test = os.getcwd().replace('\\', '/') + "/treenet_test" +\
            self.perf['ReportNote'] + ".cmd"
        self.filename_tstats = os.getcwd().replace('\\', '/') + "/treenet_tstats" +\
            self.perf['ReportNote'] + ".csv"
        self.filename_translate = os.getcwd().replace('\\', '/') + "/treenet_translate" +\
            self.perf['ReportNote'] + ".xml"
        self.filename_cmd_translate = os.getcwd().replace('\\', '/') + "/treenet_translate" +\
            self.perf['ReportNote'] + ".cmd"
        self.bf = {}
        self.backup_filenames()

        self.PARTITION = "NONE"
        self.PENALTY = "/MISSING=1,1 HLC=1,1"

        self.GENERAL_THREADS = "4"
        self.GENERAL_FORMAT = "5"

        self.VARS_MODEL = ""
        self.VARS_KEEP = ""
        # self.VARS_EXCLUDE = ""
        self.VARS_CATEGORY = ""
        # self.VARS_AUXILIARY = ""

        self.LOPTIONS_MEANS = "NO"
        self.LOPTIONS_TIMING = "NO"
        # self.PREDICTION_SUCCESS = "NO"
        # self.LOPTIONS_NOPTINT = "NO"
        # self.LOPTIONS_PS = "NO"
        # self.LOPTIONS_CONFUSION_MATRIX = "YES/BOTH"
        self.LOPTIONS_GAINS = "NO"
        self.LOPTIONS_ROC = "NO"
        self.LOPTIONS_PLOTS = 'NO'
        self.LOPTIONS_UNS = "NO"

        # self.LIMIT_DEPTH = "AUTO"
        # self.LIMIT_MINCHILD = "1"

        self.ICL_ADDITIVE = ""
        self.ICL_ALLOW = ""
        self.ICL_DISALLOW = ""
        self.ICL_PENALTY = ""

        self.TREENET_TREES = "200"
        # self.TREENET_MAXTREES = "10000"
        self.TREENET_NODES = "6"
        self.TREENET_DEPTH = "7"
        # # self.TREENET_RNODES = "NO"
        self.TREENET_MINCHILD = "10"
        self.TREENET_LOSS = "AUTO"
        # # self.TREENET_OPTIMAL = "AVGLL"
        self.TREENET_LEARNRATE = "AUTO"
        # self.TREENET_SCALELEARN = "0.0"
        # self.TREENET_DECAYLEARN = "1.0"
        self.TREENET_SUBSAMPLE = "0.5"
        # # self.TREENET_SUB0 = "0.5"
        # # self.TREENET_SUB1 = "0.5"
        self.TREENET_INFLUENCE = "0.1"
        # # self.TREENET_BREAKDOWN = "0.9"
        # # self.TREENET_FULLREPORT = "YES"
        # # srgboost2_test.pyelf.TREENET_NODEDETAIL = "NO"
        # # self.TREENET_GB = "10"
        # self.TREENET_PROB = "YES"
        # # self.TREENET_CTHRESHOLD = '0.5'
        # # self.TREENET_LTHRESHOLD = '0.1'
        # # self.TREENET_SEED = '987654321'
        # self.TREENET_STT = "NO"
        # self.TREENET_SRL = "NO"
        # self.TREENET_SIT = "NO"
        # # self.TREENET_FR = '100000'
        # self.TREENET_INIT = ""
        # # self.TREENET_SIGMA = "NO"
        # # self.TREENET_CENTER = "YES"
        # # self.TREENET_QUANTILE = "0.5"
        # # self.TREENET_TRIMGOOD = "YES"
        # # self.TREENET_TRIMBAD = "YES"
        # # self.TREENET_TRIMPOS = "YES"
        # # self.TREENET_TRIMNEG = "YES"
        # # self.TREENET_TRIMAFTER = "100000"
        # # self.TREENET_PP = "500,5000,0,0"
        self.TREENET_PLOTS = "NO,NO,NO,NO"
        # # self.TREENET_MV = "30,30,0,0"
        # # self.TREENET_MP = "0,500,0,0"
        self.TREENET_PF = ""
        # self.TREENET_LINFLUENCE = ""
        # self.TREENET_GPS = "NO"
        self.TREENET_INTER = "NO"
        self.TREENET_VPAIR = "NO"
        self.TREENET_PREDS = "0"
        # # self.TREENET_LOWMEMORY = "NO"
        # # self.TREENET_INDEX = "YES"
        # # self.TREENET_LSAMPLING = "YES"
        # # self.TREENET_FOLD = ""
        # self.TREENET_CALIB = "NO"
        # self.TREENET_TN2 = "NO"
        # # self.TREENET_ONETREE = "NO"
        # # self.TREENET_SPARSE = "NONE"
        self.TREENET_LOCAL = ""

        self.TREENET_RGBOOST = ""
        self.TREENET_RGL0 = ""
        self.TREENET_RGL1 = ""
        self.TREENET_RGL2 = ""
        self.TREENET_TSTATS = ""

    def backup_filenames(self):
        self.bf = {'filename_output': self.filename_output,
                   'filename_grove': self.filename_grove,
                   'filename_train': self.filename_train,
                   'filename_test': self.filename_test,
                   'filename_hold': self.filename_hold,
                   'filename_score_train': self.filename_score_train,
                   'filename_score_test': self.filename_score_test,
                   'filename_cmd_train': self.filename_cmd_train,
                   'filename_cmd_test': self.filename_cmd_test,
                   'filename_tstats': self.filename_tstats,
                   'filename_translate': self.filename_translate,
                   'filename_cmd_translate': self.filename_cmd_translate}

    def restore_filenames(self):
        self.filename_output = self.bf['filename_output']
        self.filename_grove = self.bf['filename_grove']
        self.filename_train = self.bf['filename_train']
        self.filename_test = self.bf['filename_test']
        self.filename_hold = self.bf['filename_hold']
        self.filename_score_train = self.bf['filename_score_train']
        self.filename_score_test = self.bf['filename_score_test']
        self.filename_cmd_train = self.bf['filename_cmd_train']
        self.filename_cmd_test = self.bf['filename_cmd_test']
        self.filename_tstats = self.bf['filename_tstats']
        self.filename_translate = self.bf['filename_translate']
        self.filename_cmd_translate = self.bf['filename_cmd_translate']

    def create_command_file_train(self):
        if self.test_type == "Samples":
            self.i_sample += 1
            self.perf['SampleNote'] = '_' + str(self.i_sample+1)

        opt_names = dir(self)

        lines = list()
        lines.append('REM ***Setting Filenames' + '\n')
        lines.append('OUTPUT "' + self.filename_output + '"' + '\n')
        lines.append('GROVE "' + self.filename_grove + '"' + '\n')
        lines.append('USE "' + self.filename_train + '"' + '\n')
        # lines.append('SAVE "' + self.filename_score_train + '"' + '\n')

        if self.PARTITION == "NONE":
            lines.append('PARTITION NONE' + '\n')
        elif self.PARTITION == "FILE":
            lines.append('PARTITION FILE = "' + self.filename_test + '"' + '\n')
            
        if self.PENALTY != "NONE":
        	    lines.append('PENALTY ' + self.PENALTY + '\n')

        lines.append('REM ***Settings from GENERAL category' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "GENERAL" and getattr(self, name) != "":
                lines.append('_'.join(buf[1:len(buf)]) + ' = ' + getattr(self, name) + '\n')

        lines.append('REM ***Settings from LOPTIONS category' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "LOPTIONS" and getattr(self, name) != "":
                lines.append(buf[0] + ' ' + '_'.join(buf[1:len(buf)]) + ' = ' +\
                             getattr(self, name) + '\n')

        lines.append('REM ***Settings from LIMIT category' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "LIMIT" and getattr(self, name) != "":
                lines.append(buf[0] + ' ' + '_'.join(buf[1:len(buf)]) + ' = ' +\
                             getattr(self, name) + '\n')

        lines.append('REM ***Settings from TREENET category' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "TREENET" and buf[1] == "TSTATS":
                if getattr(self, name) == "YES":
                    lines.append('TREENET TSTATS = "' + self.filename_tstats + '"' + '\n')
            elif buf[0] == "TREENET" and getattr(self, name) != "":
                lines.append(buf[0] + ' ' + '_'.join(buf[1:len(buf)]) + ' = ' +\
                             getattr(self, name) + '\n')

        lines.append('REM ***Settings from ICL category' + '\n')
        for name in opt_names:
            buf = name.split('_')
            if buf[0] == "ICL" and getattr(self, name) != "":
                lines.append(buf[0] + ' ' + '_'.join(buf[1:len(buf)]) + ' = ' +\
                             getattr(self, name) + '\n')

        lines.append('REM ***Settings from VARS category' + '\n')
        lines.append("CATEGORY" + '\n')
        lines.append("AUXILIARY" + '\n')
        lines.append("MODEL" + ' ' + self.VARS_MODEL + '\n')
        lines.append("KEEP" + '\n')
        if self.VARS_KEEP != "":
            lines.append("KEEP" + ' ' + self.VARS_KEEP + '\n')
        if self.VARS_CATEGORY != "":
            lines.append("CATEGORY" + ' ' + self.VARS_CATEGORY + '\n')

        lines.append('REM ***Run' + '\n')
        lines.append('TREENET GO' + '\n')
        # lines.append('SCORE GO' + '\n')
        lines.append('OUTPUT' + '\n')
        lines.append('QUIT' + '\n')

        f = open(self.filename_cmd_train, "w")
        for line in lines:
            f.writelines(line)
        f.close()

    def create_command_file_test(self):
        lines = list()

        lines.append('USE "' + self.filename_hold + '"' + '\n')
        lines.append('GROVE "' + self.filename_grove + '" READONLY' + '\n')
        lines.append('SAVE "' + self.filename_score_test + '"' + '\n')
        lines.append('SCORE GO' + '\n')
        lines.append('QUIT' + '\n')

        f = open(self.filename_cmd_test, "w")
        for line in lines:
            f.writelines(line)
        f.close()

    def create_command_file_translate(self):
        lines = list()

        lines.append('GROVE "' + self.filename_grove + '" READONLY' + '\n')
        lines.append('TRANSLATE LANGUAGE = PMML, VLIST = yes, TLIST = yes, DETAILS = yes, '
                     'OUTPUT = "' + self.filename_translate + '"' + '\n')
        lines.append('QUIT' + '\n')

        f = open(self.filename_cmd_translate, "w")
        for line in lines:
            f.writelines(line)
        f.close()

    def execute_command_file_train(self, convert_scores=False):
        time_start = time.time()
        args = [self.filename_cmd_train]
        #os.system(self.spm_executable + ' ' + self.filename_cmd_train)
        retval = subprocess.call([self.spm_executable, "-q", self.filename_cmd_train])
        time_end = time.time()
        self.perf['TrainingTime'] = time_end - time_start
        print("TreeNet Training Time: " + str(time_end - time_start))
        if (retval != 0):
            print("Training job", self.filename_cmd_train, "failed")
        elif convert_scores:
            d = np.loadtxt(self.filename_score_train, delimiter=",", skiprows=1, ndmin=2,
                           dtype=float)
            np.savetxt(self.filename_score_train, np.c_[d[:, 3], d[:, 6]], delimiter=',', fmt='%f')
        return retval

    def execute_command_file_test(self, convert_scores=True):
        os.system(self.spm_executable + ' -q ' + self.filename_cmd_test)
        if convert_scores:
            d = np.loadtxt(self.filename_score_test, delimiter=",", skiprows=1, ndmin=2, dtype=float)
            np.savetxt(self.filename_score_test, np.c_[d[:, 6], d[:, 3]], delimiter=',', fmt='%f')

    def execute_command_file_translate(self):
        os.system(self.spm_executable + ' -q ' + self.filename_cmd_translate)

    def clean_workspace(self):
        # if os.path.isfile(self.filename_cmd_train):
        #     os.remove(self.filename_cmd_train)
        if os.path.isfile(self.filename_cmd_test):
            os.remove(self.filename_cmd_test)
        if os.path.isfile(self.filename_score_train):
            os.remove(self.filename_score_train)
        if os.path.isfile(self.filename_score_test):
            os.remove(self.filename_score_test)
        if os.path.isfile(self.filename_grove):
            os.remove(self.filename_grove)
        if os.path.isfile(self.filename_output):
            os.remove(self.filename_output)
        if os.path.isfile(self.filename_tstats):
            os.remove(self.filename_tstats)
        if os.path.isfile(self.filename_translate):
            os.remove(self.filename_translate)
        if os.path.isfile(self.filename_cmd_translate):
            os.remove(self.filename_cmd_translate)

    def prepare_replication(self, folder_to_save):
        if not os.path.isdir(folder_to_save):
            os.mkdir(folder_to_save)

        folder_, file_, ext_ = funcs.fileparts(self.filename_output)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_output, destination_file, rem_source=True)
        #self.filename_output = destination_file
        folder_, file_, ext_ = funcs.fileparts(self.filename_score_test)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_score_test, destination_file, rem_source=True)
        #self.filename_score_test = destination_file
        folder_, file_, ext_ = funcs.fileparts(self.filename_cmd_train)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_cmd_train, destination_file, rem_source=True)
        #self.filename_cmd_train = destination_file
        folder_, file_, ext_ = funcs.fileparts(self.filename_tstats)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_tstats, destination_file, rem_source=True)
        # self.filename_tstats = destination_file
        folder_, file_, ext_ = funcs.fileparts(self.filename_translate)
        destination_file = folder_to_save + "/" + file_ + self.perf['SampleNote'] + ext_
        funcs.copy_and_delete(self.filename_translate, destination_file, rem_source=True)
        #self.filename_translate = destination_file

    def make_classification_stats(self):
        xtest = True
        if os.path.isfile(self.filename_score_test):
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
        else:
            xtest = False
            cm = "N/A"
            auc = np.nan
            roc_sensitivity = np.nan
            roc_specificity = np.nan

        self.perf['ConfusionMatrix'] = cm
        self.perf['AUC'] = auc
        self.perf['ROC_Sensitivity'] = roc_sensitivity
        self.perf['ROC_Specificity'] = roc_specificity

        stats_txt = list()
        if not xtest:
            stats_txt.append('Model build failed')
        else:
            tp = cm[1, 1]
            fp = cm[0, 1]
            tn = cm[0, 0]
            fn = cm[1, 0]

            specificity = float(tn)/(tn + fp)
            sensitivity = float(tp)/(tp + fn)

            stats_txt.append(' Actual       Predicted Class                  Actual\n')
            stats_txt.append(' Class                    0            1        Total\n')
            stats_txt.append(' ----------------------------------------------------\n')
            stats_txt.append(' 0            {: 13.2f}{: 13.2f}{: 13.2f}\n'.\
                             format(cm[0, 0], cm[0, 1], cm[0, 0]+cm[0, 1]))
            stats_txt.append(' 1            {: 13.2f}{: 13.2f}{: 13.2f}\n'.\
                             format(cm[1, 0], cm[1, 1], cm[1, 0]+cm[1, 1]))
            stats_txt.append(' ----------------------------------------------------\n')
            stats_txt.append(' Pred. Tot.   {: 13.2f}{: 13.2f}{: 13.2f}\n'.
                             format(cm[0, 0]+cm[1, 0], cm[0, 1]+cm[1, 1],
                                    cm[0, 0]+cm[1, 0]+cm[0, 1]+cm[1, 1]))
            stats_txt.append(' Correct      {: 13.5f}{: 13.5f}\n'.\
                             format(float(cm[0, 0])/(cm[0, 0]+cm[0, 1]),
                                    float(cm[1, 1])/(cm[1, 0]+cm[1, 1])))
            # stats_txt.append(' Success Ind. {: 13.5f}{: 13.5f}\n'.format())
            stats_txt.append(' Tot. Correct {: 13.5f}\n'.\
                             format(float(cm[0, 0]+cm[1, 1])/(cm[0, 0]+cm[1, 0]+cm[0, 1]+cm[1, 1])))
            stats_txt.append('\n')
            stats_txt.append(' Specificity (True Ref): {: 7.5f},  Sensitivity (True Resp): {: 7.5f}\n'.\
                             format(specificity, sensitivity))
            stats_txt.append(' False Reference: {: 7.5f},  False Response: {: 7.5f}\n'.\
                             format(float(cm[1, 0])/(cm[1, 0]+cm[1, 1]),
                                    float(cm[0, 1])/(cm[0, 0]+cm[0, 1])))
            stats_txt.append(' Reference = 0, Response = 1\n')
            stats_txt.append(' Approx Integrated ROC: {: 9.7f}'.format(auc) + "\n")

        self.perf['StatsTxt'] = stats_txt

    def get_optimal_n_trees(self):
        if not os.path.exists(self.filename_translate):
            if not os.path.exists(filename_cmd_translate):
                self.create_command_file_translate()
            self.execute_command_file_translate()
        with open(self.filename_translate) as fh:
                  doc = xd.parse(fh.read(), disable_entities=False)
        pmml = doc["PMML"]
        datadict = pmml["DataDictionary"]
        model = pmml["MiningModel"]
        schema = model["MiningSchema"]
        target = ""
        ncat = np.nan
        for field in schema["MiningField"]:
            if field["@usageType"] == "predicted":
                target = field["@name"]
                break
        for field in datadict["DataField"]:
            if field["@name"] == target:
                ncat = 0
                if field["@optype"] == "categorical":
                    for value in field["Value"]:
                        ncat = ncat + 1
                break
        ntrees = 0
        segmentation = model["Segmentation"]
        for segment in segmentation["Segment"]:
            if segment.__contains__("TreeModel"):
                ntrees = ntrees + 1
        return ntrees
