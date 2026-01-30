#!/bin/bash
for file in ;
do
perl -e '
($id,$fasta)=@ARGV;
open(ID,$id);
while (<ID>) {
    s/\r?\n//;
    /^>?(\S+)/;
    $ids{$1}++;
}
$num_ids = keys %ids;
open(F, $fasta);
$s_read = $s_wrote = $print_it = 0;
while (<F>) {
    if (/^>(\S+)/) {
	$s_read++;
	if ($ids{$1}) {
	    $s_wrote++;
	    $print_it = 1;
	    delete $ids{$1}
	}
	else {
	    $print_it = 0
	}

    };
    if ($print_it) {
	print $_
    }
};
END {
    warn "Searched $s_read FASTA records.\nFound $s_wrote IDs out of $num_ids in the ID list.\n"
}
' Genes_total $file > Gene_of_specie_$file;
done
