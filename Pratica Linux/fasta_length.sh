#!/bin/bash
### Count othe length of sequencies in a fasta file

for file in *.fasta;
do awk '/^>/ {if (seqlen){print seqlen}; print ;seqlen=0;next; } { seqlen += length($0)}END{print seqlen}' $file > length_of_$file;
done
