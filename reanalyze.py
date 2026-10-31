#!/usr/bin/env python3
"""Reproduce a limited, source-verifiable, vision-only analysis from Conwell et al.
Inputs: source_data.xlsx from Conwell et al. (2024), Nature Communications.
Source: https://doi.org/10.1038/s41467-024-53147-y
No estimate from the unverifiable historical 21-model mixed-domain regression is recreated.
"""
import os, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parent
SRC=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'source_data.xlsx'
D=ROOT/'output';D.mkdir(exist_ok=True)
xls=pd.ExcelFile(SRC)
r2=pd.read_excel(xls,'Figure2');r5=pd.read_excel(xls,'Figure5C')
required2={'architecture','contrast','metric','subj_id','score','rank','display_name'}
required5={'model_string','metric','score','imagenet_accuracy'}
assert required2 <= set(r2.columns) and required5 <= set(r5.columns), 'Input schema differs'
assert len(r2)==440 and len(r5)==198, 'Unexpected row count'
assert set(r2.metric.str.lower())=={'crsa','wrsa'},'Unexpected metric'
assert set(r5.metric.str.upper())=={'CRSA','WRSA'},'Unexpected metric'
assert not r2.duplicated(['architecture','metric','subj_id']).any(),'Duplicate model/subject/metric'
assert not r5.duplicated(['model_string','metric']).any(),'Duplicate accuracy row'
assert r2.groupby(['architecture','metric']).size().eq(4).all(),'Some models have non-4 subjects'
assert r2.groupby('architecture').contrast.nunique().eq(1).all(), 'Inconsistent architecture assignments'
assert r5.groupby('model_string').imagenet_accuracy.nunique().eq(1).all(), 'Inconsistent accuracy'
means=r2.groupby(['architecture','display_name','contrast','metric'],as_index=False).score.mean()
wide=means.pivot(index=['architecture','display_name','contrast'],columns='metric',values='score').reset_index()
wide.columns.name=None
acc=r5[r5.metric=='CRSA'][['model_string','imagenet_accuracy']].copy()
acc['architecture']=acc.model_string.str.removesuffix('_classification')
assert acc.architecture.is_unique
wide=wide.merge(acc[['architecture','imagenet_accuracy']],on='architecture',how='left',validate='one_to_one')
assert len(wide)==55, f'Unexpected {len(wide)} models'
assert wide.contrast.value_counts().to_dict()=={'CNN':34,'Transformer':21}
assert wide.imagenet_accuracy.notna().sum()==52
matched=wide.dropna(subset=['imagenet_accuracy']).copy()
assert matched.contrast.value_counts().to_dict()=={'CNN':31,'Transformer':21}
matched['transformer']=(matched.contrast=='Transformer').astype(int)
matched['top1_10']=(matched.imagenet_accuracy-75.0)/10.0
assert matched.imagenet_accuracy.between(0,100).all()

results={'source':'Conwell et al. 2024 Nature Communications doi:10.1038/s41467-024-53147-y','input_file':SRC.name,'n_models_full':55,'n_models_matched':52,'class_counts_full':wide.contrast.value_counts().to_dict(),'class_counts_adjusted':matched.contrast.value_counts().to_dict(),'missing_accuracy':wide.loc[wide.imagenet_accuracy.isna(),'architecture'].tolist(),'notes':'Model is unit of inference; per-subject results averaged. Exploratory secondary reanalysis, not original mixed-domain 21-model regression.'}
for k,name in [('wrsa','veRSA'),('crsa','cRSA')]:
 x=wide.loc[wide.contrast=='CNN',k].to_numpy();y=wide.loc[wide.contrast=='Transformer',k].to_numpy()
 welch=stats.ttest_ind(y,x,equal_var=False);n1,n2=len(x),len(y)
 md=float(y.mean()-x.mean());sdiff=np.sqrt(x.var(ddof=1)/n1+y.var(ddof=1)/n2)
 df=(x.var(ddof=1)/n1+y.var(ddof=1)/n2)**2/((x.var(ddof=1)/n1)**2/(n1-1)+(y.var(ddof=1)/n2)**2/(n2-1))
 ci=(md-stats.t.ppf(.975,df)*sdiff,md+stats.t.ppf(.975,df)*sdiff)
 X=sm.add_constant(matched[['top1_10','transformer']]);fit=sm.OLS(matched[k],X).fit(cov_type='HC3')
 m2=sm.OLS(matched[k],sm.add_constant(matched[['top1_10','transformer']].assign(interaction=matched.top1_10*matched.transformer))).fit(cov_type='HC3')
 results[name]={
 'group_means':{'CNN':float(x.mean()),'Transformer':float(y.mean())},
 'unadjusted_difference_transformer_minus_CNN':md,'welch_p':float(welch.pvalue),'welch_CI95':list(map(float,ci)),'welch_df':float(df),
 'adjusted_N':len(matched),'adjusted_R2':float(fit.rsquared),'adjusted_coef':{key:float(val) for key,val in fit.params.items()},'adjusted_p_HC3':{key:float(val) for key,val in fit.pvalues.items()},'adjusted_SE_HC3':{key:float(val) for key,val in fit.bse.items()},'adjusted_CI95_HC3':{key:list(map(float,val)) for key,val in fit.conf_int().iterrows()},
 'interaction_exploratory_beta':float(m2.params['interaction']),'interaction_exploratory_p':float(m2.pvalues['interaction']),
 'n_models_full':len(wide),'n_models_adjusted':len(matched)
 }

# Verify that the independent source rows agree with the per-model means.
for metric in ['CRSA','WRSA']:
 row=r5[r5.metric==metric].copy();row['architecture']=row.model_string.str.removesuffix('_classification')
 check=wide[['architecture',metric.lower()]].merge(row[['architecture','score']],on='architecture',how='inner')
 assert np.allclose(check[metric.lower()],check.score,atol=1e-10),f'Failed published data consistency check for {metric}'

r2.to_csv(D/'source_Figure2_440_subject_rows.csv',index=False)
r5.to_csv(D/'source_Figure5C_198_rows.csv',index=False)
wide.to_csv(D/'verified_55_models.csv',index=False)
matched.to_csv(D/'verified_52_performance_matched_models.csv',index=False)
with open(D/'results.json','w') as f: json.dump(results,f,indent=2,ensure_ascii=False)
for k in ('veRSA','cRSA'):
 r=results[k]
 print(f'{k}: unadjusted CNN={r["group_means"]["CNN"]:.4f}, Transformer={r["group_means"]["Transformer"]:.4f}, Welch p={r["welch_p"]:.5f}; adjusted Transformer beta={r["adjusted_coef"]["transformer"]:.5f}, CI={r["adjusted_CI95_HC3"]["transformer"]}, p={r["adjusted_p_HC3"]["transformer"]:.5f}')
print('CHECK: Figure2 per-model source averages exactly match Figure5C values for all 52 matched models.')
