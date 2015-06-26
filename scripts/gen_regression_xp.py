from pathlib import Path

datasets = ['all_rounds.feats', 'da_semcor.feats', 'en_framenet.feats',
            'en_masc_crowdsourced.feats', 'en_ritter_sst.feats', 'eu_semcor.feats']

dataset_dir = (Path(__file__).parent / '../data/feats').resolve()

for dataset_name in datasets:
    dataset_path = dataset_dir / dataset_name
    print("python source/regress.py {} --logit".format(dataset_path))

    for baseline in ('mean', 'median'):
        print("python source/regress.py {} --baseline {}".format(dataset_path, baseline))
