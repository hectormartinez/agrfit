import argparse
import json
import pandas as pd
from pathlib import Path
from sklearn.cross_validation import cross_val_predict
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
from features_common import extract_list_of_dicts

parser = argparse.ArgumentParser(description="")
parser.add_argument("feature_file",  metavar="FILE", help="TSV file with dataset", type=Path)
parser.add_argument("--bag", help="Include bag features", action='store_true')
parser.add_argument('--baseline', help="Run baseline experiment", choices=('uniform', 'stratified', 'most_frequent'))
args = parser.parse_args()

D_features = pd.read_csv(str(args.feature_file), sep="\t")
D_features = D_features.dropna()
y_mult = D_features.y_Class_s
# y_reg = D_features.y_Ao_n

list_of_dicts = extract_list_of_dicts(D_features, args.bag)


vec = DictVectorizer()
X = vec.fit_transform(list_of_dicts)

if args.baseline:
    clf = DummyClassifier(args.baseline)
else:
    clf = LogisticRegression()


y_pred = cross_val_predict(clf, X, y_mult, cv=10, n_jobs=-1)
print(classification_report(y_mult, y_pred))
print(json.dumps({'dataset': args.feature_file.name,
                  'system': args.baseline if args.baseline else 'logreg',
                  'bag_features': args.bag,
                  'precision': precision_score(y_mult, y_pred, pos_label=None, average='weighted'),
                  'recall': recall_score(y_mult, y_pred, pos_label=None, average='weighted'),
                  'f1': f1_score(y_mult, y_pred, pos_label=None, average='weighted')
                  }))