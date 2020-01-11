import numpy as np
import os
import pandas as pd
import string
import tempfile as tf

import funcs

COMMA = ","
SPACE = " "
ext=".csv"
xext=".txt"
rseed=37
data_folder ="../Data/Classification/"
dsl = pd.read_excel("../Datasets4.xlsx")

datasets_nums = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]

for i_ds in datasets_nums:
    name = dsl['Name'][i_ds]
    stri = str(i_ds)
    nsamp = dsl['N_data_samples'][i_ds]
    tgtname = dsl['TARGET'][i_ds]
    datadir = data_folder + name
    sampdir = datadir + '/SAMPLES4'
    trainname = dsl["Train_filename_initial"][i_ds]
    testname = dsl["Test_filename_initial"][i_ds]
    keepall = (dsl["KEEP_identical"][i_ds] == "yes")
    exclude = dsl["Exclude"][i_ds]
    catstr = dsl["Categoricals"][i_ds]
    xlist = list()
    cats = set()
    if not pd.isnull(catstr):
        cats = set(catstr.split(sep=COMMA))
    if not (keepall == "yes" or pd.isnull(exclude)):
        xlist = exclude.split(sep=COMMA)
    print("Dataset #" + stri + " - " + name)
    if not os.path.isdir(sampdir):
        os.mkdir(sampdir)
    trainfile = data_folder + name + '/' + trainname

    print("Dataset #" + stri + " - " + name + ": Loading train file")
    init_train = pd.read_csv(trainfile, low_memory=False)
    if pd.isnull(testname):
        data_full = init_train
    else:
        testfile = data_folder + name + '/' + testname
        print("Dataset #" + stri + " - " + name + ": Loading test file")
        init_test = pd.read_csv(testfile, low_memory=False)
        data_full = init_train.append(init_test)
        del init_test
    del init_train
    if len(xlist) > 0:
        data_full.drop(columns = xlist, inplace = True)

    field_names = data_full.columns
    xpin = tf.mktemp(suffix=ext)
    xpout = tf.mktemp(suffix=ext)
    data_full.to_csv(xpin)
    del data_full
    indlist = list()
    for i in range(nsamp):
        indlist.append("sample"+str(i))
    indstr = ",".join(indlist)

    xpart = "xpartition --nlearn=2 --ntest=1 --nholdout=1 --indicators=" + indstr + " --rseed=" +\
        str(rseed) + SPACE + "--by=" + tgtname + SPACE + "--himem" + SPACE + xpin + SPACE +\
        xpout
    os.system(xpart)

    data_full = pd.read_csv(xpout, low_memory=False)
    os.remove(xpin)
    os.remove(xpout)

    xdata_full = pd.DataFrame()
    if len(cats) > 0 or funcs.df_anyobj(data_full):
        xdata_full = funcs.expandClass(data_full[field_names], cats)
    for j in range(nsamp):
        strj = str(j+1)
        sampvar = "sample" + str(j)
        trainfile = sampdir + "/data_train_" + strj + ext
        testfile = sampdir + "/data_test_" + strj + ext
        holdfile = sampdir + "/data_hold_" + strj + ext
        xtrainfile = sampdir + "/data_train_" + strj + xext
        xtestfile = sampdir + "/data_test_" + strj + xext
        xholdfile = sampdir + "/data_hold_" + strj + xext
        trainxfile = sampdir + "/data_trainx_" + strj + ext
        testxfile = sampdir + "/data_testx_" + strj + ext
        holdxfile = sampdir + "/data_holdx_" + strj + ext

        print("Dataset #" + stri + " - " + name + ": SAMPLES step #" + strj)
        data_train = data_full[field_names][data_full[sampvar]=="Learn"]
        data_test = data_full[field_names][data_full[sampvar]=="Test"]
        data_hold = data_full[field_names][data_full[sampvar]=="Holdout"]
        data_train.to_csv(trainfile, index=False)
        data_test.to_csv(testfile, index=False)
        data_hold.to_csv(holdfile, index=False)
        if xdata_full.empty:
            data_train.to_csv(xtrainfile, index=False, header=False)
            data_test.to_csv(xtestfile, index=False, header=False)
            data_hold.to_csv(xholdfile, index=False, header=False)
        else:
            data_trainx = xdata_full[data_full[sampvar]=="Learn"]
            data_testx = xdata_full[data_full[sampvar]=="Test"]
            data_holdx = xdata_full[data_full[sampvar]=="Holdout"]
            data_trainx.to_csv(trainxfile, index=False, header=True)
            data_testx.to_csv(testxfile, index=False, header=True)
            data_holdx.to_csv(holdxfile, index=False, header=True)
            data_trainx.to_csv(xtrainfile, index=False, header=False)
            data_testx.to_csv(xtestfile, index=False, header=False)
            data_holdx.to_csv(xholdfile, index=False, header=False)
