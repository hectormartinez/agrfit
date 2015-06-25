python common2feats.py ../data/common/en_framenet_cst.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/en_framenet_cst.entr.tsv > ../data/feats/en_framenet.feats
python common2feats.py ../data/common/en_masc_crowdsourced.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/en_masc_crowdsourced.entr.tsv > ../data/feats/en_masc_crowdsourced.feats
python common2feats.py ../data/common/da_semcor.common ../data/res/da_freqs_max6 ../data/res/da_stem_idf.tsv ../data/res/da_form_stem_count.tsv ../data/res/entropy/da.curated.entr.tsv > ../data/feats/da_semcor.feats
python common2feats.py ../data/common/eu_semcor.common ../data/res/eu_freqs_max6 ../data/res/eu_stem_idf.tsv ../data/res/eu_form_stem_count.tsv ../data/res/entropy/eu_semcor.entr.tsv > ../data/feats/eu_semcor.feats
python common2feats.py ../data/common/en_ritter_sst.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/en_ritter_sst.entr.tsv > ../data/feats/en_ritter_sst.feats

for keyword in fair-j know-v land-n long-j quiet-j say-v show-v tell-v time-n work-n
do
 	python common2feats.py ../data/common/round2.1-$keyword-sentences.txt.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/round2.1.entr.tsv > ../data/feats/round2.1.$keyword.feats
 	 done

for keyword in fair-j know-v land-n long-j quiet-j say-v show-v tell-v time-n work-n
do
 	python common2feats.py ../data/common/round2.2-$keyword-sentences.txt.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/round2.2.entr.tsv > ../data/feats/round2.2.$keyword.feats
done

for keyword in chance-n cool-j familiar-j juice-n justify-v player-n rapid-j rip-v try-v
do 
	python common2feats.py ../data/common/round3-$keyword-sentences.txt.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/round3.entr.tsv > ../data/feats/round3.$keyword.feats
done

for keyword in curious-j entitle-v exercise-v exercise-n mature-v maturity-n officer-n rate-n smart-j succeed-v success-n succession-n suspicious-j
do
 	python common2feats.py ../data/common/round4-$keyword-sentences.txt.common ../data/res/en_wordfreqs_min6 ../data/res/en_stem_idf.tsv ../data/res/en_form_stem_count.tsv ../data/res/entropy/round4.entr.tsv  > ../data/feats/round4.$keyword.feats
 done
