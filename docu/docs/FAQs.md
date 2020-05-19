# FAQs (Frquently Asked Questions)


+  Q: Which percentiles indicate good quality?<br>
A: For some attributes, low values are good (adapter dimers or percentage of ribosomal RNA fragments) while for others higher numbers are better (microRNA yield, percentage of reads in the analysis, Phred Scores). For each attribute and sample we provide the percentile the value has in the background distribution (the reference corpus). Therefore, for adapter-dimers, lower quartile values are good, while for microRNA yield upper quartile values would be desired. However, in order to keep the color code coherent the ‘good quartile’ will always be displayed in green while ‘the bad quartile’ will appear in red.

+ Q: How is the heatmap generated?<br>
A: In order to generate a unique colour scheme in the heatmap, the percentiles need to be transformed so that the lower quartile indicates good performance while the upper quartile indicates bad results (see also What are the good percentiles? above for more information).

+ Q: Is SOLID data supported?<br>
A: mirnaQC was conceptually designed for Illumina (nucleotide space) data. That implies that the pipeline can process SOLID data but many attributes will be meaningless. This is because to analyse SOLID data, colour space reads are mapped to the genome first in order to perform the conversion to nucleotide space. This means that the percentage of mapped reads or even adapter dimers cannot be assessed. Other attributes like the number of miRNAs, percentage of short reads, library complexity can be correctly analysed and compared.