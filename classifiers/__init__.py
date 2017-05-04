__author__ = 'Anna'
from sklearn import neighbors, datasets, svm
from sklearn.naive_bayes import GaussianNB
from  numpy import sum
from sklearn.neural_network import MLPClassifier
from sklearn import tree


def knn_classify():
    print("\nkNN")
    n_neighbors = 15

    # import some data to play with
    iris = datasets.load_iris()
    X = iris.data
    print(X)
    print("target")
    y = iris.target
    print(y)

    weights = 'uniform' #, 'distance'
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    y_pred = clf.predict(X)
    print("y_pred")
    print(y_pred)
    print("Number of mislabeled points out of a total %d points : %d" %(len(X), (y != y_pred).sum()))


def svm_classify():
    print("\nSVM")
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    clf = svm.SVC()
    clf.fit(X, y)
    y_pred = clf.predict(X)
    print(y_pred)
    print("Number of mislabeled points out of a total %d points : %d" %(len(X), (y != y_pred).sum()))


def gaussian_naive_bayes_classify():
    print("\nGaussian Naive Bayes")
    iris = datasets.load_iris()
    gnb = GaussianNB()
    print("target")
    print(iris.target)
    gnb.fit(iris.data, iris.target)
    y_pred = gnb.predict(iris.data)
    print("y_pred")
    print(y_pred)
    print("Number of mislabeled points out of a total %d points : %d" %(iris.data.shape[0], (iris.target != y_pred).sum()))


def ann_classify():
    print("\nNeural network")
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
    clf.fit(X, y)
    y_pred = clf.predict(X)
    print("y_pred")
    print(y_pred)
    print("Number of mislabeled points out of a total %d points : %d" %(iris.data.shape[0], (iris.target != y_pred).sum()))


def decision_trees_classify():
    print("\nDecision trees")
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    y_pred = clf.predict(X)
    print("y_pred")
    print(y_pred)
    print("Number of mislabeled points out of a total %d points : %d" %(iris.data.shape[0], (iris.target != y_pred).sum()))

knn_classify()