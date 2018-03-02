[![Build Status](https://travis-ci.org/austinmeier/ontology-of-plant-stress.svg?branch=master)](https://travis-ci.org/austinmeier/ontology-of-plant-stress)
[![DOI](https://zenodo.org/badge/13996/austinmeier/ontology-of-plant-stress.svg)](https://zenodo.org/badge/latestdoi/13996/austinmeier/ontology-of-plant-stress)

# ontology-of-plant-stress

This ontology contains stresses that a plant encounters, both biotic and abiotic.

## Versions

### Stable release versions

The latest version of the ontology can always be found at:

http://purl.obolibrary.org/obo/oops.owl

(note this will not show up until the request has been approved by obofoundry.org)

### Editors' version

Editors of this ontology should use the edit version, [src/ontology/oops-edit.owl](src/ontology/oops-edit.owl)

## Contact
Please use this GitHub repository's [Issue tracker](https://github.com/austinmeier/ontology-of-plant-stress/issues) to request new terms/classes or report errors or specific concerns related to the ontology.

Run pattern apply ---> direct into 'ontology-of-plant-stress.owl'


change Makefile to use 'ontology-of-plant-stress.owl' as the input.


output of >make should be:  oops.owl, oops.obo


cat ontology-of-plant-stress.owl | grep Class:\ NCBITaxon
#this returns all the NCBI taxon IDs that are in the .owl file
#copy paste these into the NCBITaxon_imports.txt and add the root http://purl.obolibrary.org/obo/
