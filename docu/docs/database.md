# Database

## Database generation

To generate the ranking for a given quality attribute (for example ‘total number of reads’) we
first obtain the corresponding values of all samples from a reference corpus. Note that we
use different reference corpus: same kingdom, same sample protocol, same sample species and same
species and protocol. The obtained values are sorted into ascending order and the
corresponding percentile of the observed value is calculated. 

Therefore, each variable can hold desired values either when the percintiles are low (percentage of adapter-dimers or ribosomal RNA for example) or when they are high (number of reads or detected microRNAs). Either way, the quartile-based colour code is always asigned taking the nature of the feature into account, i.e. the ‘best’ quartile will always be displayed in green while the ‘worst’ quartile will be red. 

To represent the heatmap we had to make all percentiles coherent as the colors are programmatically filled. To achieve this, we internally calculate (100-Percentile) for those attributes for which high percentiles indicate good quality.

## Database contents

|Species|Samples|Studies|total number of raw reads|
| --- | --- | --- | --- |
|Human|17745|850|2.32244E+11|
|Mouse|7303|460|1.01064E+11|
|Arabidopsis thaliana|1863|199|40669870610|
|Bos taurus|1753|82|23052849107|
|Rattus norvegicus|1662|80|13839004606|
|Drosophila melanogaster|1514|163|36856287588|
|Caenorhabditis elegans|1255|99|21744837798|
|Sus scrofa|751|80|9338528047|
|Zea mays|603|52|14216151487|
|Equus caballus|480|21|6354331280|
|Danio rerio|268|32|4146066655|
|Solanum lycopersicum|244|47|4169714559|
|Gallus gallus |242|35|3708335610|
|Aedes aegypti |232|24|4514242092|
|Canis lupus familiaris|165|11|1869150079|
|Apis mellifera |71|13|827627067|
|Oryctolagus cuniculus|54|8|556118648|
|Other|133||3919986171|


