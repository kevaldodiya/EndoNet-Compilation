# EndoNet-Compilation
EndoNet has information about the endocrine system in humans. It is an inter-cellular network. It includes information about hormones, receptors and cells. furthermore, It has relations like the binding of a hormone to the receptor, transportation medium. This whole data manually annotated from the scientific literature. The web version of this dataset can be found at  http://endonet.sybig.de/. 
We have extract gene-gene relation out of the inter-cellular network, which will be at the final_resolve_3 file.

 1) Codes:
              This repository contains all tag extraction files in order to create a final dataset. files are the resolution of secretion, receptor, hormone, cell, influence. Information about those elements can be found here http://endonet.sybig.de/. We have also include UniProt in the official gene symbol mapping as a uni_to_name file.
              
2) Dataset:
              This repository contains all extraction information of various elements mentioned in the codes section. The final compiled file named final_resolve_3.csv that contains secretion hormone cell name and id, secretion hormone id and name, associate gene UniProt, Ensembl, official gene name(HGNC) to receptor hormone cell name and id,  receptor id and name, associate gene UniProt, Ensembl, official gene name(HGNC). 
