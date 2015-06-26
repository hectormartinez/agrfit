from pathlib import Path

datasets = ['all_rounds.feats', 'da_semcor.feats', 'en_framenet.feats',
            'en_masc_crowdsourced.feats', 'en_ritter_sst.feats', 'eu_semcor.feats']

dataset_dir = (Path(__file__).parent / '../data/feats').resolve()

for dataset_name in datasets:
    dataset_path = dataset_dir / dataset_name
    print("python source/classify.py {}".format(dataset_path))
    print("python source/classify.py {} --bag".format(dataset_path))

    for baseline in ('most_frequent', 'stratified', 'uniform'):
        print("python source/classify.py {} --baseline {}".format(dataset_path, baseline))
