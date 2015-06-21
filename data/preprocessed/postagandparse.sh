#!/bin/bash


file=$1
lang=$2

parameterfile="/home/alonso/proj/text2depparse/data/$lang/$lang-ud-train.treetagger.model"
parsermodel="/home/alonso/proj/text2depparse/data/$lang/$lang-ud-train.10cols.conll.model"


    inputfile=$file.input
    taggedtemp=$file.postemp
    taggedfile=$file.pos
    parsedfile=$file.conll

    /home/alonso/proj/text2depparse/tools/tree-tagger-linux-3.2/bin/tree-tagger -token $parameterfile $inputfile $taggedtemp
    python /home/alonso/proj/text2depparse/source/treetagger2parserinput.py $taggedtemp $taggedfile
    #rm $inputfile
    #rm $taggedtemp

cd /home/alonso/tool/TurboParser-2.2.0/
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:`pwd;`/deps/local/lib:"

        #parsedfile="/home/alonso/proj/framenetxling/data/framenet_annotation_2015/$lang/topos/$file.conll"
        ./TurboParser --test --file_model=$parsermodel --file_test=$taggedfile  --file_prediction=$parsedfile --logtostderr
        #rm $taggedfile


cd -
