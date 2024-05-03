# Fastq Read ID Converter
The Fastq Read ID converter is a tool to convert read IDs (fastq read headers). It converts read headers from MGI format to Illumina format (which is compatible with most pipelines).

The conversion process between MGI and Illumina read headers is summarized in the figure below:

![Alt text](images/read-header.png?raw=true "Read ID conversion overview")
*Source: [https://sagc-bioinformatics.github.io/mgikit/demultiplex](https://sagc-bioinformatics.github.io/mgikit/demultiplex)*

## Setting up

The tool depends on
  - Python >= 3.7
  - pyfastx = 2.1.0
  
You may use the conda-env.yml file to create a conda environment with the dependencies by executing

```
conda env create -f conda-env.yml
```

from the cloned reposistory. Upon activating the created **fastq_convert** environment, you should be able to run the tool.

## Usage

Fastq Read ID Converter accepts the following arguments:

        -h, --help                                  Show this help message and exit.
        -i FASTQ_IN                                 Path to the FASTQ file. REQUIRED
        -o FASTQ_OUT                                Path to the output file. REQUIRED
        -i5 I5, --i5-barcode I5                     i5 barcode of the sample. REQUIRED
        -i7 I7, --i7-barcode I7                     i7 barcode of the sample. REQUIRED
        -r RUN_ID, --run-id RUN_ID                  Run ID. REQUIRED
        -x INSTRUMENT_ID, --instrument-id           Instrument ID of the instrument used. REQUIRED

An example sequence of commands of how to execute read conversion for Single Read sequencing mode using the defaults for i5, i7, Run ID and Instrument ID:
```
python convert_readid.py -i FASTQ_R1.fastq.gz -o FASTQ_converted_R1.fastq.gz -i5 TTTTTT -i7 AAAAAA -r MY_RUN_ID -x MY_INSTRUMENT_ID
```




