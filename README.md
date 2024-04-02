# Fastq Read ID Converter
The Fastq Read ID converter is a tool to convert read IDs formats the MGI read headers to be compatible with most pipelines.

The conversion process between MGI and Illumina read headers is summarized in the figure below:

![Alt text](images/read-header.png?raw=true "Read ID conversion overview")

## Setting up

The tool depends on
  - Python >= 3.7
  - Biopython >= 1.6
  
You may use the conda-env.yml file to create a conda environment with the dependencies by executing

```
conda env create -f conda-env.yml
```

from the cloned reposistory. Upon activating the created **fastq_convert** environment, you should be able to run the tool.

## Usage

Fastq Read ID Converter accepts the following arguments:

        -h, --help                                  show this help message and exit
        --R1 R1IN, -1 R1IN                          Path to input R1 FASTQ file
        --R2 R2IN, -2 R2IN                          Path to input R2 FASTQ file. Only use for paired-end (PE) mode.
        --Rout-prefix OUT_PREFIX, -o OUT_PREFIX     Output prefix to the output file. It will append _C_(R1 or R2).fastq.gz to the prefix. 
                                                    Default is ./FASTQ_OUT creating FASTQ_OUT_C_R1(or R2).fastq.gz in the current directory.
        -i5 I5, --i5-barcode I5                     i5 barcode of the sample. If not given a random sequence will be generated.
        -i7 I7, --i7-barcode I7                     i7 barcode of the sample. If not given a random sequence will be generated.
        -r RUN_ID, --run-id RUN_ID                  Run ID. If not given, a new will be generated based on the time of the execution start.
        -x INSTRUMENT_ID, --instrument-id           Instrument ID of the instrument used. If not given a random ID will be generated.

An example sequence of commands of how to execute read conversion for Single Read sequencing mode using the defaults for i5, i7, Run ID and Instrument ID:
```
conda activate fastq_convert
python convert_readid.py -1 FASTQ_R1.fastq.gz -o FASTQ_converted_R1.fastq.gz
```
For PE mode only R2 has to be added
```
python convert_readid.py -1 FASTQ_R1.fastq.gz -2 FASTQ_R2.fastq.gz -o FASTQ_converted_R1.fastq.gz
```
Provided the i5, i7, Run ID, Instrument ID is known (TTTTTT, AAAAA, MY_RUN_ID, and MY_INSTRUMENT_ID, respectively) and one needs to convert paired-end reads:
```
python convert_readid.py -1 FASTQ_R1.fastq.gz -2 FASTQ_R2.fastq.gz -o FASTQ_converted_R1.fastq.gz -i5 TTTTTT -i7 AAAAAA -r MY_RUN_ID -x MY_INSTRUMENT_ID
```




