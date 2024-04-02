#!/usr/bin/env python3

import argparse
import gzip
import copy
from datetime import datetime
from Bio import SeqIO
from Bio import Seq
from Bio.SeqIO.QualityIO import FastqGeneralIterator
import random
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
        "--R1",
        "-1",
        type=str,
        required=True,
        help="Path to input R1 FASTQ file",
        dest="r1in",
    )
    parser.add_argument(
        "--R2",
        "-2",
        type=str,
        required=False,
        help="Path to input R2 FASTQ file. Only use for paired-end (PE) mode.",
        dest="r2in",
        default=None
    )
    parser.add_argument(
        "--Rout-prefix",
        "-o",
        type=str,
        required=True,
        help="""Output prefix to the output file. It will append _C_(R1 or R2).fastq.gz to the prefix. 
        Default is ./FASTQ_OUT creating FASTQ_OUT_C_R1(or R2).fastq.gz in the current directory.""",
        dest="out_prefix",
        default="./FASTQ_OUT"
    )
    parser.add_argument(
        "-i5",
        "--i5-barcode",
        type=str,
        required=False,
        help="i5 barcode of the sample. If not given a random sequence will be generated.",
        dest="i5",
        default=None
    )
    parser.add_argument(
        "-i7",
        "--i7-barcode",
        type=str,
        required=False,
        help="i7 barcode of the sample. If not given a random sequence will be generated.",
        dest="i7",
        default=None
    )
    parser.add_argument(
        "-r",
        "--run-id",
        type=str,
        required=False,
        help="Run ID. If not given, a new will be generated based on the time of the execution start.",
        dest="run_id",
        default=None
    )
    parser.add_argument(
        "-x",
        "--instrument-id",
        type=str,
        required=False,
        help="ID of the instrument used. If not given a random ID will be generated.",
        dest="instrument_id",
        default=None
    )

    args = parser.parse_args()

    if (args.i5 is None):
        i5 = ''.join(random.choice('CGTA') for _ in range(12))
    else:
        i5 = args.i5

    if (args.i7 is None):
        i7 = ''.join(random.choice('CGTA') for _ in range(12))
    else:
        i7 = args.i7

    if (args.run_id is None):
        run_id = datetime.now().strftime("%Y%m%d%H%M%S")
    else:
        run_id = args.run_id

    if (args.instrument_id is None):    
        instrument_id = "R%d"%(random.randint(100000000000,200000000000))
    else:
        instrument_id = args.instrument_id

    r1out="%s_C_R1.fastq.gz"%(args.out_prefix)

    print(msg_ts("Start reading"))

    with gzip.open(args.r1in, "rt") as handle1,\
        gzip.open(r1out, "wt") as out1:
        if (args.r2in is not None):
            r2out="%s_C_R2.fastq.gz"%(args.out_prefix)
            with gzip.open(args.r2in, "rt") as handle2,\
                gzip.open(r2out, "wt") as out2:
                for (r1id, r1seq, r1qual), (r2id, r2seq, r2qual) in zip(FastqGeneralIterator(handle1),FastqGeneralIterator(handle2)):
                    ro_id1 = convert_MGI_ID(r1id, i5, i7, run_id, instrument_id)
                    ro_id2 = convert_MGI_ID(r2id, i5, i7, run_id, instrument_id)
                    out1.write("@%s\n%s\n+\n%s\n"%(ro_id1, r1seq, r1qual))
                    out2.write("@%s\n%s\n+\n%s\n"%(ro_id2, r2seq, r2qual))
        else:
            for (r1id, r1seq, r1qual) in FastqGeneralIterator(handle1):
                ro_id1 = convert_MGI_ID(r1id, i5, i7, run_id, instrument_id)
                out1.write("@%s\n%s\n+\n%s\n"%(ro_id1, r1seq, r1qual))
    
    print(msg_ts("Finished writing."))
