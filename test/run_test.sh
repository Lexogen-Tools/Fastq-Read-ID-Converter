#!/bin/bash

mkdir test/out_test

python convert_readid.py -i test/in/R1.fastq.gz -o test/out_test/FASTQ_C_R1.fastq.gz -i5 AAAAAAAA -i7 TTTTTTTT -r RID1 -x IID1

files=($(find test/out_test/ -mindepth 1 -type f | sort -V))
                                                  
if [ ${#files[@]} -ne 1 ] || [ "${files[0]}" != "test/out_test/FASTQ_C_R1.fastq.gz" ]; then
    echo -e "Unexpected output generated in test/out_test/ for SR mode"
    exit 1;
fi

d=$(diff <(zcat test/out_test/FASTQ_C_R1.fastq.gz) <(zcat test/out_compare/FASTQ_C_R1.fastq.gz))
l=$(echo $d | wc -c)

if [ $l -gt 1 ]; then
    echo -e "Difference found in test/out_compare/FASTQ_C_R1.fastq.gz"
    echo -e ${d}
    exit 1;
fi

rm test/out_test/*.fastq.gz