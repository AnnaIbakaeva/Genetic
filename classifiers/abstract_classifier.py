__author__ = 'Anna'
from sklearn import neighbors, datasets, svm
from sklearn.naive_bayes import GaussianNB
from  numpy import sum
from sklearn.neural_network import MLPClassifier
from sklearn import tree

class AbstractClassifier(object):

    def __init__(self, features, target):
        self.target = target
        self.clf = None
        self.__fit(features)

    def __fit(self, features):
        pass

    def predict(self, features):
        y_pred = self.clf.predict(features)
        overall_count = len(features)
        mislabeled_count = (self.target != y_pred).sum()
        return ((mislabeled_count * 100) / overall_count)


class KnnClassifier(AbstractClassifier):
    def __init__(self, features, target, n_neighbors=15, weights='uniform'):
        self.n_neighbors = n_neighbors
        self.weights = weights
        super(KnnClassifier, self).__init__(features, target)

    def __fit(self, features):
        self.clf = neighbors.KNeighborsClassifier(self.n_neighbors, weights=self.weights)
        self.clf.fit(features, self.target)


class SvmClassifier(AbstractClassifier):
    def __fit(self, features):
         self.clf = svm.SVC()
         self.clf.fit(features, self.target)


class BayesClassifier(AbstractClassifier):
    def __fit(self, features):
        self.clf = GaussianNB()
        self.clf.fit(features, self.target)


class DecisionTreesClassifier(AbstractClassifier):
    def __fit(self, features):
        self.clf = tree.DecisionTreeClassifier()
        self.clf.fit(features, self.target)


class AnnClassifier(AbstractClassifier):
    def __init__(self, features, target, solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1):
        self.solver = solver
        self.alpha = alpha
        self.hidden_layer_sizes = hidden_layer_sizes
        self.random_state = random_state
        super(AnnClassifier, self).__init__(features, target)

    def __fit(self, features):
        self.clf = MLPClassifier(solver=self.solver, alpha=self.alpha, hidden_layer_sizes=self.hidden_layer_sizes,
                                 random_state=self.random_state)
        self.clf.fit(features, self.target)