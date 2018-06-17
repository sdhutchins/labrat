"""Protein Analysis functions."""

import re

from labrat.utils import import_json

fasta_file = input('Type your fasta file name: ')

__codons_dict = import_json("codons.json")

CODONS = __codons_dict['CODONS']


def dna2aminoacid(fasta_file, codons=CODONS):
    AAsequence = ''
    with open(fasta_file) as fileObj:
        for line in fileObj:
            line.strip()
        cont = fileObj.read()
        sequenceSearch = re.compile(r'')  # need to complete
        content = sequenceSearch.search(cont)
        print(content.group())
        for i in range(0, len(content.group()), 3):
            seq = cont[i:i+3]
            AAsequence += codons[seq]
    return AAsequence
