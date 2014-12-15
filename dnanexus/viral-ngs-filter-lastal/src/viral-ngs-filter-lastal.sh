#!/bin/bash

main() {
    set -e -x -o pipefail

    # stage the inputs
    dx cat "$resources" | zcat | tar x -C / &
    dx download "$reference" -o reference.fasta &
    dx cat "$reads" | zcat > reads.fastq
    wait

    # build Lastal reference database
    viral-ngs/tools/build/last-490/bin/lastdb -c reference.db reference.fasta

    # filter the reads
    python viral-ngs/taxon_filter.py filter_lastal reads.fastq reference.db filtered_reads.fastq

    # upload filtered reads
    name=$(dx describe --name "$reads")
    name="${name%.fastq.gz}"
    filtered_reads=$(gzip -c filtered_reads.fastq | dx upload --brief --destination "${name}.filtered.fastq.gz" -)
    dx-jobutil-add-output filtered_reads "$filtered_reads" --class=file
}
