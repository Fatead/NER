from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=500, noise=0.30, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)  # 顺序不要写错
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

log_clf = LogisticRegression(solver="liblinear", random_state=42)
svm_clf = SVC(gamma="auto", random_state=42)  # SVC默认使用RBF核函数
rnd_clf = RandomForestClassifier(n_estimators=10, random_state=42)
voting_clf = VotingClassifier(
    estimators=[('svc', svm_clf), ('lr', log_clf), ('rl', rnd_clf)],
    voting='hard'
)
voting_clf.fit(X_train, y_train)
from sklearn.metrics import accuracy_score

for clf in (svm_clf, log_clf, rnd_clf, voting_clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(clf.__class__.__name__, accuracy_score(y_pred, y_test))