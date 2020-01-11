import os
import pandas as pd
import xgBoost
import TreeNet
import time
import funcs
import copy

data_folder = "../Data/Classification/"
reptroot = "../Reports"
report_folder = reptroot + '/RGBOOST4/'
if not os.path.isdir(reptroot):
    os.mkdir(reptroot)
if not os.path.isdir(report_folder):
    os.mkdir(report_folder)
dsl = pd.read_excel("../Datasets4.xlsx")
COMMA = ","
NTHREADS = 4
# rgl += pd.read_csv('RGL_NUMBERS_0.1_0.5_var2.csv')

# datasets_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# datasets_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
# datasets_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# datasets_nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# datasets_nums = [6, 7, 8, 9, 10, 11, 12, 13, 14]
# datasets_nums = [11, 12, 13, 14]
# datasets_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# datasets_nums = [12, 13, 14]
# datasets_nums = [13, 14]
# datasets_nums = [14]
datasets_nums = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]

# cases = {"_0_0_0_0.1_0.5": ("0", "0", "0")}
# cases = {'_var1': ("", "", "")}
# cases = {'_var2': ("", "", "")}
# cases = {'_0.1_var1': ("", "", "")}
# cases = {'_0.1_var2': ("", "", "")}
# cases = {'_0.0_0.5_var1': ("", "", "")}
# cases = {'_0.0_0.5_var2': ("", "", "")}


# cases = {'_RGLs-0_INF-0.0_SUBS-1.0_LR-0.1': {'INFLUENCE': '0.0', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.1'},
#          '_RGLs-0_INF-0.1_SUBS-1.0_LR-0.1': {'INFLUENCE': '0.1', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.1'},
#          '_RGLs-0_INF-0.0_SUBS-0.5_LR-0.1': {'INFLUENCE': '0.0', 'SUBSAMPLE': '0.5', 'LEARNRATE': '0.1'},
#          '_RGLs-0_INF-0.0_SUBS-1.0_LR-0.3': {'INFLUENCE': '0.0', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.3'},
#          '_RGLs-0_INF-0.1_SUBS-1.0_LR-0.3': {'INFLUENCE': '0.1', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.3'},
#          '_RGLs-0_INF-0.0_SUBS-0.5_LR-0.3': {'INFLUENCE': '0.0', 'SUBSAMPLE': '0.5', 'LEARNRATE': '0.3'},
#          '_RGLs-0_INF-0.0_SUBS-1.0_LR-0.5': {'INFLUENCE': '0.0', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.5'},
#          '_RGLs-0_INF-0.1_SUBS-1.0_LR-0.5': {'INFLUENCE': '0.1', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.5'},
#          '_RGLs-0_INF-0.0_SUBS-0.5_LR-0.5': {'INFLUENCE': '0.0', 'SUBSAMPLE': '0.5', 'LEARNRATE': '0.5'},
#          '_RGLs-0_INF-0.0_SUBS-1.0_LR-0.8': {'INFLUENCE': '0.0', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.8'},
#          '_RGLs-0_INF-0.1_SUBS-1.0_LR-0.8': {'INFLUENCE': '0.1', 'SUBSAMPLE': '1.0', 'LEARNRATE': '0.8'},
#          '_RGLs-0_INF-0.0_SUBS-0.5_LR-0.8': {'INFLUENCE': '0.0', 'SUBSAMPLE': '0.5', 'LEARNRATE': '0.8'},
#          '_RGLs-0_INF-0.0_SUBS-1.0_LR-1.0': {'INFLUENCE': '0.0', 'SUBSAMPLE': '1.0', 'LEARNRATE': '1.0'},
#          '_RGLs-0_INF-0.1_SUBS-1.0_LR-1.0': {'INFLUENCE': '0.1', 'SUBSAMPLE': '1.0', 'LEARNRATE': '1.0'},
#          '_RGLs-0_INF-0.0_SUBS-0.5_LR-1.0': {'INFLUENCE': '0.0', 'SUBSAMPLE': '0.5', 'LEARNRATE': '1.0'}}

# cases = {'_RGLs-0_DEPTH-7_PREDS-500': {'DEPTH': '7', 'PREDS': '500', 'colsample_bytree': '1.0'},
#          '_RGLs-0_DEPTH-6_PREDS-500': {'DEPTH': '6', 'PREDS': '500', 'colsample_bytree': '1.0'},
#          '_RGLs-0_DEPTH-5_PREDS-500': {'DEPTH': '5', 'PREDS': '500', 'colsample_bytree': '1.0'},
#          '_RGLs-0_DEPTH-4_PREDS-500': {'DEPTH': '4', 'PREDS': '500', 'colsample_bytree': '1.0'},
#          '_RGLs-0_DEPTH-3_PREDS-500': {'DEPTH': '3', 'PREDS': '500', 'colsample_bytree': '1.0'},
#          '_RGLs-0_DEPTH-7_PREDS-350': {'DEPTH': '7', 'PREDS': '350', 'colsample_bytree': '0.7'},
#          '_RGLs-0_DEPTH-7_PREDS-250': {'DEPTH': '7', 'PREDS': '250', 'colsample_bytree': '0.5'},
#          '_RGLs-0_DEPTH-7_PREDS-150': {'DEPTH': '7', 'PREDS': '150', 'colsample_bytree': '0.3'},
#          '_RGLs-0_DEPTH-7_PREDS-50':  {'DEPTH': '7', 'PREDS': '50',  'colsample_bytree': '0.1'}}

cases = {'_RGLs-0_INF-0.0_SUBS-1.0_LR-0.1_DEPTH-7_PREDS-500_NTREES-400': {'NTREES': '400'}}

# type_ = "_opt"
type_ = ""

cases_keys = list(cases.keys())

time_start_research = time.time()

# for key in cases.keys():
for i_ck in range(0, len(cases_keys)):
    key = cases_keys[i_ck]

    note = key + type_
    # note = "_"

    # rgl = pd.read_csv('RGL_Tables/RGL_TABLE' + key + type_ + '.csv')

    TREES = cases[key]['NTREES']
    ETA = '0.1'
    # ETA = cases[key]['LEARNRATE']
    SUBSAMPLE = '1.0'
    # SUBSAMPLE = cases[key]['SUBSAMPLE']
    PREDS, colsample_bytree = "500", "1"
    # PREDS, colsample_bytree = cases[key]['PREDS'], cases[key]['colsample_bytree']
    MINCHILD_TN, MINCHILD_XG = "10", "1"
    DEPTH = "7"
    # DEPTH = cases[key]['DEPTH']
    NODES = "1000"
    INFLUENCE = '0.0'
    # INFLUENCE = cases[key]['INFLUENCE']
    RGBOOST, TSTATS = "YES", "YES"
    # RGL0 = gamma_ = cases[key][0]
    # RGL1 = alpha_ = cases[key][1]
    # RGL2 = lambda_ = cases[key][2]
    RGL0 = gamma_ = '0'
    RGL1 = alpha_ = '0'
    RGL2 = lambda_ = '0'

    for i_ds in datasets_nums:
        # i_rgl = [i_rgl for i_rgl, x_rgl in enumerate(rgl['No']) if x_rgl == i_ds][0]

        name = dsl['Name'][i_ds]
        nsamp = dsl['N_data_samples'][i_ds]
        tgtname = dsl['TARGET'][i_ds]
        sampdir = data_folder + name + "/SAMPLES4"
        nfeat = int(dsl['N_features'][i_ds])
        ipred = int(PREDS)
        if ipred > nfeat:
            colsample_bytree = '1'
        else:
            colsample_bytree = str(ipred/nfeat)
        anycat = os.access(sampdir + "/" + "data_trainx_1.csv", os.F_OK)

        tn = TreeNet.TreeNetModel(report_note="")
        tn.perf['Name'] = "TN (MHESS=0)"
        tn.spm_executable = "spmu"
        tn.VARS_MODEL = tgtname
        tn.VARS_CATEGORY = tgtname
        tn.PARTITION = 'FILE'
        tn.TREENET_LOSS = "AUTO"
        tn.TREENET_TREES = TREES
        tn.TREENET_LEARNRATE = ETA
        # if name == "Bank_marketing" and cases[key]['LEARNRATE'] == "1.0":
        #     tn.TREENET_LEARNRATE = '0.99'
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
        tn2 = copy.deepcopy(tn)
        tn2.perf['Name'] = "TN (MHESS=1)"
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
        # if name == "Bank_marketing" and cases[key]['LEARNRATE'] == "1.0":
        #     xg.trb_eta = '0.99'
        xg.trb_subsample = SUBSAMPLE
        xg.trb_colsample_bytree = colsample_bytree
        xg.trb_min_child_weight = MINCHILD_XG
        xg.trb_max_depth = DEPTH
        xg.trb_gamma = gamma_
        xg.trb_alpha = alpha_
        xg.trb_lambda99 = lambda_
        # xg.trb_gamma = '{:.2f}'.format((rgl['RGL0_MIN'][i_rgl] + rgl['RGL0_MAX'][i_rgl])/2.0)
        # xg.trb_alpha = '{:.2f}'.format((rgl['RGL1_MIN'][i_rgl] + rgl['RGL1_MAX'][i_rgl])/2.0)
        # xg.trb_lambda99 = '{:.2f}'.format((rgl['RGL2_MIN'][i_rgl] + rgl['RGL2_MAX'][i_rgl])/2.0)


        if anycat:
            tnx = copy.deepcopy(tn)
            tnx.perf['Name'] = "TNX (MHESS=0)"
            tnx.perf['Color'] = "y-"
            tnx.filename_output = os.getcwd().replace('\\', '/') + "/spmx_output" +\
                tnx.perf['ReportNote'] + ".dat"
            tnx.filename_grove = os.getcwd().replace('\\', '/') + "/treenetx_model" +\
                tnx.perf['ReportNote'] + ".grv"
            tnx.filename_score_test = os.getcwd().replace('\\', '/') + "/treenetx_score_test" +\
                tnx.perf['ReportNote'] + ".csv"
            tnx.filename_cmd_train = os.getcwd().replace('\\', '/') + "/treenet_train" +\
                tnx.perf['ReportNote'] + "x.cmd"
            tnx.filename_cmd_test = os.getcwd().replace('\\', '/') + "/treenet_test" +\
                tnx.perf['ReportNote'] + "x.cmd"
            tnx.filename_tstats = os.getcwd().replace('\\', '/') + "/treenet_tstats" +\
                tnx.perf['ReportNote'] + "x.csv"
            tnx.filename_translate = os.getcwd().replace('\\', '/') + "/treenet_translate" +\
                tnx.perf['ReportNote'] + "x.xml"
            tnx.filename_cmd_translate = os.getcwd().replace('\\', '/') + "/treenetx_translate" +\
                tnx.perf['ReportNote'] + ".cmd"
            tn2x = copy.deepcopy(tn2)
            tn2x.perf['Name'] = "TNX (MHESS=1)"
            tn2x.perf['Color'] = "m-"
            tn2x.filename_output = os.getcwd().replace('\\', '/') + "/spm2x_output" +\
                tn2x.perf['ReportNote'] + ".dat"
            tn2x.filename_grove = os.getcwd().replace('\\', '/') + "/treenet2x_model" +\
                tn2x.perf['ReportNote'] + ".grv"
            tn2x.filename_score_test = os.getcwd().replace('\\', '/') + "/treenet2x_score_test" +\
                tn2x.perf['ReportNote'] + ".csv"
            tn2x.filename_cmd_train = os.getcwd().replace('\\', '/') + "/treenet_train" +\
                tn2x.perf['ReportNote'] + "2x.cmd"
            tn2x.filename_cmd_test = os.getcwd().replace('\\', '/') + "/treenet_test" +\
                tn2x.perf['ReportNote'] + "2x.cmd"
            tn2x.filename_tstats = os.getcwd().replace('\\', '/') + "/treenet_tstats" +\
                tn2x.perf['ReportNote'] + "2x.csv"
            tn2x.filename_translate = os.getcwd().replace('\\', '/') + "/treenet_translate" +\
                tn2x.perf['ReportNote'] + "2x.xml"
            tn2x.filename_cmd_translate = os.getcwd().replace('\\', '/') + "/treenet2x_translate" +\
                tn2x.perf['ReportNote'] + ".cmd"
            tnx_list = list()
            tn2x_list = list()
        tn_list = list()
        tn2_list = list()
        xg_list = list()
        for i in range(nsamp):
            stri = str(i+1)
            if anycat:
                tnx.filename_train = sampdir + "/" + "data_trainx_" + stri + ".csv"
                tnx.filename_test = sampdir + "/" + "data_testx_" + stri + ".csv"
                tnx.filename_hold = sampdir + "/" + "data_holdx_" + stri + ".csv"
                tn2x.filename_train = tnx.filename_train
                tn2x.filename_test = tnx.filename_test
                tn2x.filename_hold = tnx.filename_hold

            tn.filename_train = sampdir + "/" + "data_train_" + stri + ".csv"
            tn.filename_test = sampdir + "/" + "data_test_" + stri + ".csv"
            tn.filename_hold = sampdir + "/" + "data_hold_" + stri + ".csv"
            tn2.filename_train = tn.filename_train
            tn2.filename_test = tn.filename_test
            tn2.filename_hold = tn.filename_hold
            xg.filename_train = sampdir + "/" + "data_train_" + stri + ".txt"
            xg.filename_hold = sampdir + "/" + "data_hold_" + stri + ".txt"

            if anycat:
                fh = open(tnx.filename_train, "r")
            else:
                fh = open(tn.filename_train, "r")
            header = fh.readline()
            varnames = header.split(sep=COMMA)
            for itgt in range(len(varnames)):
                if varnames[itgt] == tgtname:
                    break

            tn.create_command_file_train()
            tn.create_command_file_test()
            tn.create_command_file_translate()
            tn2.create_command_file_train()
            tn2.create_command_file_test()
            tn2.create_command_file_translate()
            if anycat:
                tnx.create_command_file_train()
                tnx.create_command_file_test()
                tnx.create_command_file_translate()
                tn2x.create_command_file_train()
                tn2x.create_command_file_test()
                tn2x.create_command_file_translate()
                tnx.execute_command_file_train()
                tnx.execute_command_file_test()
                tnx.execute_command_file_translate()
                tn2x.execute_command_file_train()
                tn2x.execute_command_file_test()
                tn2x.execute_command_file_translate()
            tn.execute_command_file_train()
            tn.execute_command_file_test()
            tn.execute_command_file_translate()
            tn2.execute_command_file_train()
            tn2.execute_command_file_test()
            tn2.execute_command_file_translate()
            if anycat:
                xg.cli_num_round = str(tnx.get_optimal_n_trees())
            else:
                xg.cli_num_round = str(tn.get_optimal_n_trees())
            xg.create_conf_file_train(format = "csv", labelcol = itgt)
            xg.train_model()
            xg.test_model(itgt=itgt, csv=True)

            tn.make_classification_stats()
            tn2.make_classification_stats()
            if anycat:
                tnx.make_classification_stats()
                tn2x.make_classification_stats()
            xg.make_classification_stats()
            modlist = [tn, tn2, xg]
            if anycat:
                for model in (tnx, tn2x):
                    modlist.append(model)
            funcs.create_report(report_folder + name + note, modlist,
                                funcs.get_dict_row(dsl, i_ds), tn.perf['SampleNote'])
            tn.prepare_replication(report_folder + name + note)
            tn2.prepare_replication(report_folder + name + note)
            xg.prepare_replication(report_folder + name + note)
            tn.clean_workspace()
            tn2.clean_workspace()
            xg.clean_workspace()
            tn_list.append(copy.deepcopy(tn))
            tn2_list.append(copy.deepcopy(tn2))
            xg_list.append(copy.deepcopy(xg))
            if anycat:
                tnx.prepare_replication(report_folder + name + note)
                tn2x.prepare_replication(report_folder + name + note)
                tnx.clean_workspace()
                tn2x.clean_workspace()
                tnx_list.append(copy.deepcopy(tnx))
                tn2x_list.append(copy.deepcopy(tn2x))
        modlist = [tn_list, tn2_list, xg_list]
        if anycat:
            for model_list in (tnx_list, tn2x_list):
                modlist.append(model_list)
        funcs.get_common_stats(report_folder, modlist, funcs.get_dict_row(dsl, i_ds), note)

time_end_research = time.time()
print("\nTime elapsed: {:.2f} seconds".format(time_end_research - time_start_research))
