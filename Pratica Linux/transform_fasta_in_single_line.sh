#!/bin/bash
########################## use this script to change multiples lines in FASTA file to just ONE LINE ##########################
#### >name_of_(1,2,3) | 1) gene ; 2) scaffold; 3) cromossomo ---> >name_of_(1,2,3) | 1) gene ; 2) scaffold; 3) cromossomo ####
####  ATGGGACTAATC					     ---> ATGGGACTAATCTTGAGCGGGCCAGACTTTGAG*TAG  #####################
####  TTGAGCGGGCCA                                                           #####################
####  GACTTTGAG*TAG                                                          #####################
for file in [input].fasta;
do
    awk '
    /^>/ {
        # Print newline before headers (except first header)
        if (NR > 1) { printf "\n" }
        print $0  # Print the header
        next
    }
    {
        printf "%s", $0  # Print sequence without newlines
    }
    END { printf "\n" }  # Final newline
    ' "$file" > "single_line_$file"
done

# awk '/^>/ {if (NR > 1) { printf "\n" } print $0} {printf "%s", $0} END { printf "\n" }' [input].fasta > [output].fasta
