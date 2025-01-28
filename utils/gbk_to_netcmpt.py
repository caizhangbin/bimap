#!/usr/bin/env python3

import sys
import os
from Bio import SeqIO

"""
Usage:
    python gbk_to_netcmpt.py *.gbk > genomes.tsv

This script:
  1. Loops over all GenBank files listed on the command line.
  2. Extracts every EC_number from each CDS in each GenBank record.
  3. Prints one line per .gbk file in the format:
        <filename>\tEC1 EC2 EC3 ...
"""

for gbk_filename in sys.argv[1:]:
    # Remove the .gbk extension for a clean "genome ID"
    prefix = os.path.splitext(gbk_filename)[0]

    ec_list = []
    with open(gbk_filename, "r") as handle:
        for record in SeqIO.parse(handle, "genbank"):
            # Each GBK can have multiple contigs or records,
            # but usually Prokka outputs one record per contig
            for feature in record.features:
                # Only look at CDS features
                if feature.type == "CDS":
                    # Check if EC_number is in the qualifiers dictionary
                    if "EC_number" in feature.qualifiers:
                        # qualifiers["EC_number"] is a list (often just 1 item)
                        ec_list.extend(feature.qualifiers["EC_number"])
    
    # De-duplicate and sort
    ec_set = sorted(set(ec_list))

    # Print in NetCmpt format: genome_id \t EC1 EC2 ...
    # If there are no ECs, you'll just get:  prefix\t
    print(f"{prefix}\t{' '.join(ec_set)}")
