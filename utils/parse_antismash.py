#!/usr/bin/env python3

import os
import json
import subprocess
import tempfile
import shutil

def extract_bgcs(genome_fasta):
    """
    Run antiSMASH on the provided genome FASTA file and return the count of identified BGCs.

    Parameters
    ----------
    genome_fasta : str
        Path to the input genome FASTA file.

    Returns
    -------
    int
        The number of biosynthetic gene clusters identified by antiSMASH.
    """

    # Create a temporary directory for antiSMASH output
    temp_dir = tempfile.mkdtemp(prefix="antismash_")

    try:
        # Run antiSMASH
        # Note: This command may vary based on your antiSMASH installation.
        cmd = [
            "antismash",
            "--output-dir", temp_dir,
            "--cpus", "4",             # Adjust CPU usage as needed
            "--clusterblast",          # Run ClusterBlast for additional info (optional)
            "--smcogs",                # Identify smCOGs (optional)
            genome_fasta
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # The summary.json file typically resides in the output directory
        summary_file = os.path.join(temp_dir, "summary.json")

        if not os.path.isfile(summary_file):
            # If summary.json is missing, antiSMASH might have failed or no clusters found
            return 0

        # Parse the summary.json file
        with open(summary_file, 'r') as f:
            data = json.load(f)

        # Count the clusters
        bgc_count = 0
        if "clusters" in data:
            bgc_count = len(data["clusters"])

        return bgc_count

    except subprocess.CalledProcessError as e:
        # Handle errors running antiSMASH if needed
        print(f"Error running antiSMASH: {e}")
        return 0
    finally:
        # Clean up temporary directory 
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    # Example usage:
    # python parse_antismash.py path_to_genome.fasta
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parse_antismash.py <genome_fasta>")
        sys.exit(1)

    genome_file = sys.argv[1]
    count = extract_bgcs(genome_file)
    print(f"BGCs found: {count}")
