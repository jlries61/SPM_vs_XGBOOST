REM ***Setting Filenames
OUTPUT "/home/jries/projects/SPM_vs_XGBOOST/Scripts/spmx_output.dat"
GROVE "/home/jries/projects/SPM_vs_XGBOOST/Scripts/treenetx_model.grv"
USE "../Data/Classification/Ring-Norm/SAMPLES4/data_trainx_7.csv"
PARTITION FILE = "../Data/Classification/Ring-Norm/SAMPLES4/data_testx_7.csv"
PENALTY /MISSING=1,1 HLC=1,1
REM ***Settings from GENERAL category
FORMAT = 5
THREADS = 4
REM ***Settings from LOPTIONS category
LOPTIONS GAINS = NO
LOPTIONS MEANS = NO
LOPTIONS PLOTS = NO
LOPTIONS ROC = NO
LOPTIONS TIMING = NO
LOPTIONS UNS = NO
REM ***Settings from LIMIT category
REM ***Settings from TREENET category
TREENET DEPTH = 7
TREENET INFLUENCE = 0.0
TREENET INTER = NO
TREENET LEARNRATE = 0.1
TREENET LOCAL = NO
TREENET LOSS = AUTO
TREENET MINCHILD = 10
TREENET NODES = 1000
TREENET PLOTS = NO,NO,NO,NO
TREENET PREDS = 500
TREENET RGBOOST = YES
TREENET RGL0 = 0
TREENET RGL1 = 0
TREENET RGL2 = 0
TREENET SUBSAMPLE = 1.0
TREENET TREES = 400
TREENET TSTATS = "/home/jries/projects/SPM_vs_XGBOOST/Scripts/treenet_tstatsx.csv"
TREENET VPAIR = NO
REM ***Settings from ICL category
REM ***Settings from VARS category
CATEGORY
AUXILIARY
MODEL class
KEEP
CATEGORY class
REM ***Run
TREENET GO
OUTPUT
QUIT
