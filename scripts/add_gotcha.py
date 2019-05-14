import os
import sys
import csv

occupations = {}
for row in csv.DictReader(open("../data/occupations-stats.tsv", 'r'), delimiter='\t'):
    occupations[row["occupation"]] = float(row["bls_pct_female"])

tsv_in = csv.DictReader(open("../data/all_sentences.tsv", 'r'), delimiter='\t')
header = ["sentid", "sentence", "gotcha"]
tsv_out = csv.DictWriter(open("../data/all_sentences_gotcha.tsv", 'w'), delimiter='\t', fieldnames=header)
tsv_out.writeheader()

for row in tsv_in:

    """
    (1) pronoun==female AND answer==0 AND occupation IS NOT majority-female
    OR
    (2) pronoun==female AND answer==1 AND occupation IS majority-female
    OR
    (3) pronoun==male AND answer==0 AND occupation IS majority-female
    OR
    (4) pronoun==male AND answer==1 AND occupation IS NOT majority-female
    """

    occupation, participant, answer, gender, _ = row["sentid"].split('.')
    print(occupation, participant, answer, gender)

    is_gotcha = False

    if gender=="female" and answer=='0' and not occupations[occupation] > 50.0:
        is_gotcha = True

    if gender=="female" and answer=='1' and occupations[occupation] > 50.0:
        is_gotcha = True
        
    if gender=="male" and answer=='0' and occupations[occupation] > 50.0:
        is_gotcha = True

    if gender=="male" and answer=='1' and not occupations[occupation] > 50.0:
        is_gotcha = True

    row["gotcha"] = 1 if is_gotcha else 0

    tsv_out.writerow(row)

