# About mirnaQC


mirnaQC is an attempt to extend quality control of small RNA sequencing which is frequently restricted to PhredScore-based filters. It defines 34 relevant quality measures that can be obtained from miRNA-seq datasets profiled with sRNAbench (link to 2019 NAR publication). 
Included quality attributes cover a broad range of aspects such as sequencing and microRNA yield, estimation of RNA degradation through rRNA and mRNA fragments or library preparation. To improve their interpretability, quality attributes are ranked using a reference distribution generated with over 36,000 publicly available miRNA-seq datasets. Accepted input formats include FASTQ and SRA accessions (link to the corresponding section). 

mirnaQC can be useful in at least 3 different ways: i) external quality assessment of the provided amples  ii) detection of specific quality issues, which might be especially relevant for pilot studies that aim to optimize the protocol prior to run a high number of samples and iii) detection of samples that might bias downstream results and therefore should be eliminated or treated separately. 
One of the future goals will be to relate the provided quality features better with both, upstream (sample preparation) and downstream (differential expression, functional analysis) decisions which will allow to provide more exact automated recommendations. 

Please note that mirnaQC was developed and tested using Google Chrome and Mozilla Firefox. Using other (older) browsers will likely result in some features not working properly. Please contact us to try to solve them.

mirnaQC was developed by the Computational Epigenomics Group at University of Granada