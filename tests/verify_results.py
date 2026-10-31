#!/usr/bin/env python3
"""Lightweight numerical assertions for the released secondary analysis."""
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'output/results.json').read_text())
assert r['n_models_full'] == 55
assert r['n_models_matched'] == 52
assert r['class_counts_full'] == {'CNN':34,'Transformer':21}
assert r['class_counts_adjusted'] == {'CNN':31,'Transformer':21}
assert set(r['missing_accuracy']) == {'eca_nfnet_l0','googlenet','semnasnet_100'}
expected={
    'veRSA':{'coefficient':-0.013403903263322775,'p':0.05074825535688663,'r2':0.16152724244275962},
    'cRSA': {'coefficient':-0.03672385752618286,'p':0.012992161517019585,'r2':0.16274319362889045},
}
for metric, vals in expected.items():
    q=r[metric]
    assert abs(q['adjusted_coef']['transformer']-vals['coefficient']) < 1e-7
    assert abs(q['adjusted_p_HC3']['transformer']-vals['p']) < 1e-7
    assert abs(q['adjusted_R2']-vals['r2']) < 1e-7
assert len(pd.read_csv(ROOT/'output/verified_55_models.csv'))==55
assert len(pd.read_csv(ROOT/'output/verified_52_performance_matched_models.csv'))==52
assert len(pd.read_csv(ROOT/'output/source_Figure2_440_subject_rows.csv'))==440
assert len(pd.read_csv(ROOT/'output/source_Figure5C_198_rows.csv'))==198
print('PASS: source matching, model counts, statistical coefficients and output tables verified.')
