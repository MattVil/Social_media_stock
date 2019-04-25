import numpy as np

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC

from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_auc_score

from utils import PROJECT_PATH



ALGORITHMS = {'Naive_Bayes' : GaussianNB(),
              'Decision_Tree' : DecisionTreeClassifier(),
              'K-NN' : KNeighborsClassifier(),
              'Random_Forest' : RandomForestClassifier(),
              'Logistic_Regression' : LogisticRegression(),
              'Ada_Boost' : AdaBoostClassifier()}
              # 'SVM' : SVC()}

# confusion_matrix, accuracy, precision, recall, F1, AUC
METRICS = {'Naive_Bayes' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0],
           'Decision_Tree' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0],
           'K-NN' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0],
           'Random_Forest' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0],
           'Logistic_Regression' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0],
           'Ada_Boost' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0]}
           # 'SVM' : [np.zeros((2, 2)), 0.0, 0.0, 0.0, 0.0, 0.0]}

NB_FOLD = 10

def binaryLabels(label):
    pos, neg = 0, 0
    y = []
    for i, elt in enumerate(label):
        if(elt > 0):
            y.append(True)
            pos += 1
        else:
            y.append(False)
            neg += 1
    print("{} Positive\t{} Negative".format(pos, neg))
    return np.asarray(y)


def main():
    label = np.load(PROJECT_PATH + "data/emo.npy")
    data = np.load(PROJECT_PATH + "data/label.npy")


    label = binaryLabels(label)

    kf = KFold(n_splits=NB_FOLD)

    for idx, (train_index, test_index) in enumerate(kf.split(data)):
        print("ITERATION {}:".format(idx))
        for name, alg in ALGORITHMS.items():
            x_train = data[train_index]
            x_test = data[test_index]
            y_train = label[train_index]
            y_test = label[test_index]
            alg.fit(x_train, y_train)
            y_pred = alg.predict(x_test)
            prf = precision_recall_fscore_support(y_test, y_pred, average='macro')
            METRICS[name][0] += confusion_matrix(y_test, y_pred)
            METRICS[name][1] += accuracy_score(y_test, y_pred)
            METRICS[name][2] += prf[0]
            METRICS[name][3] += prf[1]
            METRICS[name][4] += prf[2]
            METRICS[name][5] += roc_auc_score(y_test, y_pred)


    print("\n\n\nFinal metrics :")
    for alg in METRICS.keys():
        METRICS[alg][0] = METRICS[alg][0]/NB_FOLD
        METRICS[alg][1] = METRICS[alg][1]/NB_FOLD
        METRICS[alg][2] = METRICS[alg][2]/NB_FOLD
        METRICS[alg][3] = METRICS[alg][3]/NB_FOLD
        METRICS[alg][4] = METRICS[alg][4]/NB_FOLD
        METRICS[alg][5] = METRICS[alg][5]/NB_FOLD
        print("\nAlgorithm : {}".format(alg))
        print(METRICS[alg])



if __name__ == '__main__':
    main()
