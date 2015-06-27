import argparse
import json
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.cross_validation import cross_val_predict
from sklearn.dummy import DummyRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import explained_variance_score, \
    mean_absolute_error, r2_score

from features_common import extract_list_of_dicts
from sklearn.preprocessing import scale


parser = argparse.ArgumentParser(description="")
parser.add_argument("feature_file",  metavar="FILE", help="TSV file with dataset", type=Path)
parser.add_argument("--bag", help="Include bag features", action='store_true')
parser.add_argument('--baseline', help="Run baseline experiment", choices=('median', 'mean'))
parser.add_argument('--logit', help="Perform logit transformation", action='store_true')
parser.add_argument('--ignore', help="Ignore these namespaces", nargs='+', default=[])
parser.add_argument('--keep', help="Keep these namespaces", nargs='+', default=[])
args = parser.parse_args()

D_features = pd.read_csv(str(args.feature_file), sep="\t")
D_features = D_features.dropna()
y_orig = D_features.y_Ao_n
if args.logit:

    y_reg = np.log(D_features.y_Ao_n / (1 - D_features.y_Ao_n))
    # Cap at -3 and 3
    y_reg[np.isneginf(y_reg)] = -3
    y_reg[np.isposinf(y_reg)] = 3

else:
    y_reg = D_features.y_Ao_n


list_of_dicts = extract_list_of_dicts(D_features, args.bag, args.ignore, args.keep)

vec = DictVectorizer(sparse=False)
X = vec.fit_transform(list_of_dicts)
X = scale(X)
print("Dataset shape: ", X.shape)

if args.baseline:
    reg = DummyRegressor(args.baseline)
else:
    reg = Ridge()


y_pred = cross_val_predict(reg, X, y_reg, cv=10, n_jobs=-1)
if args.logit:
    # Cap extreme values
    # y_pred[y_pred > 100] = 100
    # y_pred[y_pred < 100] = -100

    # print("Number of nans before", np.isnan(y_pred).sum())
    y_pred = np.exp(y_pred) / (np.exp(y_pred) + 1)
    # print("Number of nans after", np.isnan(y_pred).sum())
    y_reg = y_orig

print(json.dumps({'dataset': args.feature_file.name,
                  'system': args.baseline if args.baseline else 'linreg',
                  'bag_features': args.bag,
                  'num_features': X.shape[1],
                  'num_instances': X.shape[0],
                  'ignore': " ".join(sorted(args.ignore)),
                  'keep': " ".join(sorted(args.keep)),
                  'explained_variance': explained_variance_score(y_reg, y_pred),
                  'mean_absolute_error': mean_absolute_error(y_reg, y_pred),
                  'r2': r2_score(y_reg, y_pred)
                  }))