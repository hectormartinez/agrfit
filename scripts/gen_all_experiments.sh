#!/usr/bin/env bash
python scripts/gen_regression_xp.py|parallel|grep "^{" > results/regression_results.jsonl
python scripts/gen_classification_xp.py|parallel|grep "^{" > results/classification_results.jsonl
python scripts/gen_classification_ablation_xp.py|parallel|grep "^{" > results/classification_ablation_results.jsonl
python scripts/gen_regression_ablation_xp.py|parallel|grep "^{" > results/regression_ablation_results.jsonl