#!/usr/bin/env python3

import argparse
import gzip
from datetime import datetime
import pyfastx
import re

def msg_ts(thismessage: str) -> str:
    return str(datetime.now()) + ": " + thismessage

def convert_MGI_ID(in_id, i5, i7, runID, instrumentID) -> str:
    
    # The MGI has the following format of the header:
    # @V350018879L4C001R0020000010/1 and it consists of the following parts
    # V350018879 L4 C001 R002 0000010 1 which can be captured into groups

    m = re.search(r"^(\w+)L(\d+)C(\d+)R(\d{3})(\d+)\/([12])", in_id)

    # Use the parts from MGI read ID and add additional parts based on provided arguments or their defaults
    # to create Illumina ID in the format
    # @R100400180029:20210917154250:V350018879:4:10:1:2 1:N:0:CACTAGCG+AATAATCT
    id = "%s:%s:%s:%d:%d:%d:%d %d:N:0:%s+%s"%(
        instrumentID, runID,
        m.group(1), int(m.group(2)),
        int(m.group(5)), int(m.group(3)),
        int(m.group(4)), int(m.group(6)),
        i5, i7
    )

    return id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="FASTQ format converter",
        description="Convert MGI Read IDs to Illumina read IDs to ensure compatibility with pipelines",
    )
    parser.add_argument(
        "-i",
        type=str,
        required=True,
        help="Path to input FASTQ file. REQUIRED",
        dest="fastq_in",
    )
    parser.add_argument(
        "-o",
        type=str,
        required=True,
        help="Path to the output FASTQ file. REQUIRED",
        dest="fastq_out"
    )
    parser.add_argument(
        "-i5",
        "--i5-barcode",
        type=str,
        required=True,
        help="i5 barcode of the sample. REQUIRED",
        dest="i5",
        default=None
    )
    parser.add_argument(
        "-i7",
        "--i7-barcode",
        type=str,
        required=True,
        help="i7 barcode of the sample. REQUIRED",
        dest="i7",
        default=None
    )
    parser.add_argument(
        "-r",
        "--run-id",
        type=str,
        required=True,
        help="Run ID. REQUIRED",
        dest="run_id",
        default=None
    )
    parser.add_argument(
        "-x",
        "--instrument-id",
        type=str,
        required=True,
        help="ID of the instrument used. REQUIRED",
        dest="instrument_id",
        default=None
    )

    args = parser.parse_args()

    i5 = args.i5
    i7 = args.i7
    run_id = args.run_id
    instrument_id = args.instrument_id
    fastq_out = args.fastq_out
    fastq_in = args.fastq_in

    print(msg_ts("Start reading."))

    with gzip.open(fastq_out, "wt") as fout:
        fq = pyfastx.Fastq(fastq_in, build_index=False)
        for id,seq,qual in fq:
            cid = convert_MGI_ID(id, i5=i5, i7=i7, runID=run_id, instrumentID=instrument_id)
            entry = "@%s\n%s\n+\n%s\n"%(cid, seq, qual)
            fout.write(entry)

    print(msg_ts("Finished writing."))
