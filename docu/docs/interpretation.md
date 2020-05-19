# Interpretation Guide

The success of a small RNA sequencing run depends on many different factors including RNA quality, quantity and purity of the sample, an optimized library processing protocol and sequencing among others. However, it is not always easy or even possible to relate features measured from sequencing data directly to any of the possible technical artefacts. 

To explain this, let's consider the percentage of reads assigned to known microRNAs and the number of detected microRNAs. Very often the focus of small RNA-seq experiments is on microRNAs so high values of parameters related to miRNAs abundance should indicate high quality. However, virtually all technical artefacts can affect these measurements. 

* Size selection step: If the bands are not cut precisely, a higher number of other RNA species might be sequenced, thus lowering the number of sequenced miRNAs

* Contamination: If samples get contaminated by other biological material, the fraction of reads assigned to miRNAs will drop 

* RNA quality: Degraded RNA will generally lead to the detection of a higher amount of fragments from longer RNA molecules, and therefore automatically the number of miRNA reads gets lower.   

Therefore, the number of microRNA reads is clearly a quality criterion, which however  cannot be attributed directly to a concrete technical artefact or experimental parameter.  
