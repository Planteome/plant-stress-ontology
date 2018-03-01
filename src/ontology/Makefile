OBO=http://purl.obolibrary.org/obo
ONT=oops
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
RELEASEDIR=../..
ROBOT= robot
OWLTOOLS= owltools
USECAT= --use-catalog

all: all_imports $(ONT).owl $(ONT).obo
test: $(ONT).owl $(ONT).obo
prepare_release: all
	cp $(ONT).owl $(ONT).obo $(RELEASEDIR) &&\
	mkdir -p $(RELEASEDIR)/imports &&\
	cp imports/*{owl,obo} $(RELEASEDIR)/imports &&\
	git add $(RELEASEDIR)/imports/*{obo,owl} &&\
	(test -f subsets/*owl && cp subsets/*{owl,obo} $(RELEASEDIR)/subsets && git add $(RELEASEDIR)/subsets/* || echo "no subsets") &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

$(ONT).owl: $(SRC)
	$(ROBOT)  reason -e none -i $< -r ELK relax reduce -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
$(ONT).obo: $(ONT).owl
	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@


IMPORTS = ncbitaxon ro peco chebi
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_import.obo,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

ROBOT_JAVA_ARGS = -Xmx5G
# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	ROBOT_JAVA_ARGS=$(ROBOT_JAVA_ARGS) $(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

imports/%_import.obo: imports/%_import.owl
	$(OWLTOOLS) $(USECAT) $< -o -f obo $@

# clone remote ontology locally, perfoming some excision of relations and annotations
mirror/%.obo: $(SRC)
	wget --no-check-certificate $(OBO)/$*.obo -O $@
.PRECIOUS: mirror/%.obo

mirror/%.owl: mirror/%.obo
	$(OWLTOOLS) $< --remove-annotation-assertions -l -s -d -r --remove-dangling-annotations  -o $@
.PRECIOUS: mirror/%.owl

release: $(ONT).owl $(ONT).obo
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

##### patterns
PATTERNS_DISEASE_OWL = $(patsubst patternapply/formatted_tables/diseases/%.tsv, patternapply/ontology_files/%.owl, $(wildcard patternapply/formatted_tables/diseases/*.tsv)) $(patsubst patternapply/formatted_tables/diseases/%.tsv, patternapply/ontology_files/%.obo, $(wildcard patternapply/formatted_tables/diseases/*.tsv))
PATTERNS_DEFICIENCY_OWL = $(patsubst patternapply/formatted_tables/deficiencies/%.tsv, patternapply/ontology_files/%.owl, $(wildcard patternapply/formatted_tables/deficiencies/*.tsv)) $(patsubst patternapply/formatted_tables/deficiencies/%.tsv, patternapply/ontology_files/%.obo, $(wildcard patternapply/formatted_tables/deficiencies/*.tsv))
PATTERNS_EXCES_OWL = $(patsubst patternapply/formatted_tables/excess/%.tsv, patternapply/ontology_files/%.owl, $(wildcard patternapply/formatted_tables/excess/*.tsv)) $(patsubst patternapply/formatted_tables/excess/%.tsv, patternapply/ontology_files/%.obo, $(wildcard patternapply/formatted_tables/excess/*.tsv))


all_patterns: $(PATTERNS_DISEASE_OWL) $(PATTERNS_DEFICIENCY_OWL) $(PATTERNS_EXCES_OWL)

patternapply/ontology_files/%.owl: patternapply/formatted_tables/diseases/%.tsv
	dosdp-tools --outfile=$@ --obo-prefixes=true --template=patternapply/yaml_patterns/plant_disease_pattern.yaml --ontology=imports/ncbitaxon_import.owl generate --infile=$< &&\
	robot annotate -O "http://purl.obolibrary.org/obo/$*.owl" -i $@ -o $@
	
patternapply/ontology_files/%.obo: patternapply/ontology_files/%.owl
	$(ROBOT) convert -i $< -f obo -o $@

patternapply/ontology_files/%.owl: patternapply/formatted_tables/deficiencies/%.tsv
	dosdp-tools --outfile=$@ --obo-prefixes=true --template=patternapply/yaml_patterns/deficiency_stress_pattern.yaml --ontology=imports/chebi_import.owl generate --infile=$< &&\
	robot annotate -O "http://purl.obolibrary.org/obo/$*.owl" -i $@ -o $@
	
patternapply/ontology_files/%.obo: patternapply/ontology_files/%.owl
	$(ROBOT) convert -i $< -f obo -o $@

patternapply/ontology_files/%.owl: patternapply/formatted_tables/excess/%.tsv
	dosdp-tools --outfile=$@ --obo-prefixes=true --template=patternapply/yaml_patterns/excess_stress_pattern.yaml --ontology=imports/chebi_import.owl generate --infile=$< &&\
	robot annotate -O "http://purl.obolibrary.org/obo/$*.owl" -i $@ -o $@
	
patternapply/ontology_files/%.obo: patternapply/ontology_files/%.owl
	$(ROBOT) convert -i $< -f obo -o $@
