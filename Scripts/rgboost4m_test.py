import os
import pandas as pd
import xgBoost
import TreeNet
import time
import funcs
import copy

data_folder = "../Data/Classification/"
reptroot = "../Reports"
report_folder = reptroot + '/RGBOOST4M/'
if not os.path.isdir(reptroot):
    os.mkdir(reptroot)
if not os.path.isdir(report_folder):
    os.mkdir(report_folder)
dsl = pd.read_excel("../Datasets4.xlsx")
COMMA = ","
datasets_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

cases = {'_RGLs-0_INF-0.0_SUBS-1.0_LR-0.1_DEPTH-7_PREDS-500_NTREES-400': {'NTREES': '400'}}

type_ = ""

cases_keys = list(cases.keys())

time_start_research = time.time()

for i_ck in range(0, len(cases_keys)):
    key = cases_keys[i_ck]

    note = key + type_
    TREES = cases[key]['NTREES']
    ETA = '0.1'
    SUBSAMPLE = '1.0'
    PREDS, colsample_bytree = "500", "1"
    MINCHILD_TN, MINCHILD_XG = "10", "1"
    DEPTH = "7"
    NODES = "1000"
    INFLUENCE = '0.0'
    RGBOOST, TSTATS = "YES", "YES"
    RGL0 = gamma_ = '0'
    RGL1 = alpha_ = '0'
    RGL2 = lambda_ = '0'

    for i_ds in datasets_nums:
        name = dsl['Name'][i_ds]
        nsamp = dsl['N_data_samples'][i_ds]
        tgtname = dsl['TARGET'][i_ds]
        sampdir = data_folder + name + "/SAMPLES4"
        nfeat = int(dsl['N_features'][i_ds])
        ipred = int(PREDS)
        anycat = os.access(sampdir + "/" + "data_trainx_1.csv", os.F_OK)

        tn = TreeNet.TreeNetModel(report_note="")
        tn.perf['Name'] = "TN RGB (MHESS=0)"
        tn.spm_executable = "spmu"
        tn.VARS_MODEL = tgtname
        tn.VARS_CATEGORY = tgtname
        tn.PARTITION = 'FILE'
        tn.TREENET_LOSS = "AUTO"
        tn.TREENET_TREES = TREES
        tn.TREENET_LEARNRATE = ETA
        tn.TREENET_SUBSAMPLE = SUBSAMPLE
        tn.TREENET_PREDS = PREDS
        tn.TREENET_NODES = NODES
        tn.TREENET_MINCHILD = MINCHILD_TN
        tn.TREENET_DEPTH = DEPTH
        tn.TREENET_INFLUENCE = INFLUENCE
        tn.TREENET_LOCAL = "NO"
        tn.TREENET_TSTATS = TSTATS
        tn.TREENET_RGBOOST = RGBOOST
        tn.TREENET_RGL0 = RGL0
        tn.TREENET_RGL1 = RGL1
        tn.TREENET_RGL2 = RGL2
        tn0 = copy.deepcopy(tn)
        tn0.perf['Name'] = "Plain TN (MART)"
        tn0.perf['Color'] = "m-"
        tn0.TREENET_RGBOOST = "NO"
        tn0.filename_output = os.getcwd().replace('\\', '/') + "/mart_output" +\
            tn.perf['ReportNote'] + ".dat"
        tn0.filename_grove = os.getcwd().replace('\\', '/') + "/mart_model" +\
            tn.perf['ReportNote'] + ".grv"
        tn0.filename_score_test = os.getcwd().replace('\\', '/') + "/mart_score_test" +\
            tn.perf['ReportNote'] + ".csv"
        tn0.filename_cmd_train = os.getcwd().replace('\\', '/') + "/mart_train" +\
            tn.perf['ReportNote'] + ".cmd"
        tn0.filename_cmd_test = os.getcwd().replace('\\', '/') + "/mart_test" +\
            tn.perf['ReportNote'] + ".cmd"
        tn0.filename_tstats = os.getcwd().replace('\\', '/') + "/mart_tstats" +\
            tn.perf['ReportNote'] + ".csv"
        tn0.filename_translate = os.getcwd().replace('\\', '/') + "/mart_translate" +\
            tn.perf['ReportNote'] + ".xml"
        tn0.filename_cmd_translate = os.getcwd().replace('\\', '/') + "/mart_translate" +\
            tn.perf['ReportNote'] + ".cmd"
        tn2 = copy.deepcopy(tn)
        tn2.perf['Name'] = "TN RGB (MHESS=1)"
        tn2.perf['Color'] = "g-"
        tn2.TREENET_MINHESS = "1"
        tn2.filename_output = os.getcwd().replace('\\', '/') + "/spm2_output" +\
            tn2.perf['ReportNote'] + ".dat"
        tn2.filename_grove = os.getcwd().replace('\\', '/') + "/treenet2_model" +\
            tn2.perf['ReportNote'] + ".grv"
        tn2.filename_score_test = os.getcwd().replace('\\', '/') + "/treenet2_score_test" +\
            tn2.perf['ReportNote'] + ".csv"
        tn2.filename_cmd_train = os.getcwd().replace('\\', '/') + "/treenet_train" +\
            tn2.perf['ReportNote'] + "2.cmd"
        tn2.filename_cmd_test = os.getcwd().replace('\\', '/') + "/treenet_test" +\
            tn2.perf['ReportNote'] + "2.cmd"
        tn2.filename_tstats = os.getcwd().replace('\\', '/') + "/treenet_tstats" +\
            tn2.perf['ReportNote'] + "2.csv"
        tn2.filename_translate = os.getcwd().replace('\\', '/') + "/treenet_translate" +\
            tn2.perf['ReportNote'] + "2.xml"
        tn2.filename_cmd_translate = os.getcwd().replace('\\', '/') + "/treenet2_translate" +\
            tn2.perf['ReportNote'] + ".cmd"

        xg = xgBoost.XGBoostModel(report_note="")
        xg.cli_num_round = TREES
        xg.trb_eta = ETA
        xg.trb_subsample = SUBSAMPLE
        if ipred < nfeat:
            xg.trb_colsample_bynode  = str(ipred/nfeat)
        xg.trb_min_child_weight = MINCHILD_XG
        xg.trb_max_depth = DEPTH
        xg.trb_gamma = gamma_
        xg.trb_alpha = alpha_
        xg.trb_lambda99 = lambda_

        tn_list = list()
        tn0_list = list()
        tn2_list = list()
        xg_list = list()
        for i in range(nsamp):
            stri = str(i+1)
            if anycat:
                tn.filename_train = sampdir + "/" + "data_trainx_" + stri + ".csv"
                tn.filename_test = sampdir + "/" + "data_testx_" + stri + ".csv"
                tn.filename_hold = sampdir + "/" + "data_holdx_" + stri + ".csv"
            else:
                tn.filename_train = sampdir + "/" + "data_train_" + stri + ".csv"
                tn.filename_test = sampdir + "/" + "data_test_" + stri + ".csv"
                tn.filename_hold = sampdir + "/" + "data_hold_" + stri + ".csv"
            tn2.filename_train = tn.filename_train
            tn2.filename_test = tn.filename_test
            tn2.filename_hold = tn.filename_hold
            tn0.filename_train = tn.filename_train
            tn0.filename_test = tn.filename_test
            tn0.filename_hold = tn.filename_hold
            xg.filename_train = sampdir + "/" + "data_train_" + stri + ".txt"
            xg.filename_hold = sampdir + "/" + "data_hold_" + stri + ".txt"

            fh = open(tn.filename_train, "r")
            header = fh.readline()
            varnames = header.split(sep=COMMA)
            for itgt in range(len(varnames)):
                if varnames[itgt] == tgtname:
                    break

            tn.create_command_file_train()
            tn.create_command_file_test()
            tn.create_command_file_translate()
            tn0.create_command_file_train()
            tn0.create_command_file_test()
            tn0.create_command_file_translate()
            tn2.create_command_file_train()
            tn2.create_command_file_test()
            tn2.create_command_file_translate()
            tn.execute_command_file_train()
            tn.execute_command_file_test()
            tn.execute_command_file_translate()
            tn0.execute_command_file_train()
            tn0.execute_command_file_test()
            tn0.execute_command_file_translate()
            tn2.execute_command_file_train()
            tn2.execute_command_file_test()
            tn2.execute_command_file_translate()
            xg.cli_num_round = str(tn.get_optimal_n_trees())
            xg.create_conf_file_train(format = "csv", labelcol = itgt)
            xg.train_model()
            xg.test_model(itgt=itgt, csv=True)

            tn.make_classification_stats()
            tn0.make_classification_stats()
            tn2.make_classification_stats()
            xg.make_classification_stats()
            modlist = [tn0, tn, tn2, xg]
            funcs.create_report(report_folder + name + note, modlist,
                                funcs.get_dict_row(dsl, i_ds), tn.perf['SampleNote'])
            tn.prepare_replication(report_folder + name + note)
            tn0.prepare_replication(report_folder + name + note)
            tn2.prepare_replication(report_folder + name + note)
            xg.prepare_replication(report_folder + name + note)
            tn.clean_workspace()
            tn0.clean_workspace()
            tn2.clean_workspace()
            xg.clean_workspace()
            tn_list.append(copy.deepcopy(tn))
            tn0_list.append(copy.deepcopy(tn0))
            tn2_list.append(copy.deepcopy(tn2))
            xg_list.append(copy.deepcopy(xg))
        modlist = [tn0_list, tn_list, tn2_list, xg_list]
        funcs.get_common_stats(report_folder, modlist, funcs.get_dict_row(dsl, i_ds), note)

time_end_research = time.time()
print("\nTime elapsed: {:.2f} seconds".format(time_end_research - time_start_research))
