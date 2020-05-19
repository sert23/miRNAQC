#Quality features

##Sequencing yield

**<u>Raw number of reads</u>** (Raw reads): Total number of raw input reads, i.e. before adapter trimming and filtering

**<u>Number of reads in analysis</u>** (Reads): Number of reads that are used for the analysis, i.e. that are not filtered out due to quality or length criterion

**<u>Number of unique reads</u>** (Unique reads): The number of unique sequence reads after read collapsing

**<u>Number of miRNAs detected</u>** (miRNAs): The number of detected microRNAs (applying single assignment)

**<u>Percentage of miRNA reads</u>** (miRNA reads %): The percentage of effective reads assigned to mature microRNAs

**<u>Number of adapter-trimmed reads</u>** (Trimmed reads): Number of reads for which the adapter was found (and trimmed).  Fail to detect he adapter can have several reasons: i) bad sequencing quality towards the 3' end of the read (sequencing errors impede the detection of the adapter), ii) longer fragments for which the adapter is not sequenced, iii) the wrong adapter sequence was specified

**<u>Percentage of adapter-trimmed reads</u>** (Trimmed reads %): Percentage of reads for which the adapter was found (and trimmed).  Fail to detect he adapter can have several reasons: i) bad sequencing quality towards the 3' end of the read (sequencing errors impede the detection of the adapter), ii) longer fragments for which the adapter is not sequenced, iii) the wrong adapter sequence was specified

**<u>Number of reads per unique read</u>** (Reads per unique): The number of reads in analysis divided by the number of unique reads

##Library complexity


**<u>Percentage of top miRNA reads</u>** (% top miRNA): Percentage of reads assigned to the most expressed miRNA

**<u>Percentage of top 5 miRNA reads</u>** (% top5 miRNA): Percentage of reads assigned to the 5 most expressed miRNAs

**<u>Percentage of top 20 miRNA reads</u>** (% top20 miRNA): Percentage of reads assigned to the 20 most expressed miRNAs

**<u>miRNAs needed to reach 50% miRNA reads</u>** (#miRNA p50): Number of miRNAs needed to reach 50% miRNA reads

**<u>miRNAs needed to reach 75% miRNA reads</u>** (#miRNA p75): Number of miRNAs needed to reach 75% miRNA reads

**<u>miRNAs needed to reach 95% miRNA reads</u>** (#miRNA p95): Number of miRNAs needed to reach 95% miRNA reads

**<u>miRNAs detected per 1kb mapped</u>** (miRNAs per 1000 reads): Number of miRNAs detected per 1kb mapped to miRNAs


##Library quality

**<u>Percentage of adapter dimers</u>** (Dimers %): The percentage of reads that correspond to adapter-dimer, i.e. those that are shorter or equal to 2nt after adapter trimming 

**<u>Percentage of ultra short fragments</u>** (ultra short fragments %): Percentage of reads between 3 and 14 nt. A high number is usually indicative of issues in library preparation or low RNA quality

**<u>Percentage of short fragments</u>** (short fragments %): Percentage of reads between 15 and 17 nt. This range was choosen because tRNA fragments are frequently of 18 nt length.

**<u>Percentage of ribosomal RNA</u>** (ribosomal RNA %): Percentage of ribosome derived reads

##Putative contamination


**<u>Percentage of genome mapping reads</u>** (% ref.genome): Percentage of reads mapped to the reference genome

**<u>Percentage of non genome mapping reads</u>** (% unmapped): Percentage of reads not mapped to the reference genome

**<u>Percentage of bacteria mapping reads</u>** (% bacteria): Percentage of reads mapped to a collection of different bacteria

**<u>Percentage of virus mapping reads</u>** (% virus): Percentage of reads mapped to a collection of different virus


##Read length distribution


**<u>Percentage of reads in miRNA "peak"</u>** (miRNA "peak"): The percentage of miRNA-assigned reads of lengths 21, 22 and 23

**<u>Mean of miRNA mapping reads length</u>** (miRNA mean length): Mean of miRNA mapping reads read length

**<u>miRNA length distribution Std. Dev.</u>** (miRNA SD): The standard deviation of the read lengths of he reads mapped to microRNAs

**<u>miRNA length mode</u>** (miRNA length mode): miRNA length mode

**<u>skewness read length distribution</u>** (skewness): skewness read length distribution

**<u>absolute read length distribution skewness</u>** (|skewness|): absolute read length distribution skewness

##Sequencing quality


**<u>Average mean Phred Score</u>** (Average mean Phred Score): The mean Phred Scores are obtained from FastQC per position, then the average of these values are calculated using positions 1 to 40

**<u>Average Phred Score</u>** (Avg Phred): This is the average Phred Score of the median scores at a given position

**<u>Average percentile 10 Phred Score </u>** (Average percentile 10 Phred Score ): The Phred Scores of percentile 10 are obtained from FastQC per position, then the average of these values are calculated using positions 1 to 40

**<u>Average percentile 25 Phred Score </u>** (Average percentile 25 Phred Score ): The Phred Scores of percentile 25 are obtained from FastQC per position, then the average of these values are calculated using positions 1 to 40

**<u>Average percentile 75 Phred Score </u>** (Average percentile 75 Phred Score ): The Phred Scores of percentile 175 are obtained from FastQC per position, then the average of these values are calculated using positions 1 to 40

**<u>Average percentile 90 Phred Score </u>** (Average percentile 90 Phred Score ): The Phred Scores of percentile 90 are obtained from FastQC per position, then the average of these values are calculated using positions 1 to 40

**<u>Percentage of reads in analysis</u>** (Reads %): Percentage of reads that are used for the analysis, i.e. that are not filtered out due to quality or length criterion

