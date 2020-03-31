OBO=http://purl.obolibrary.org/obo
ONT=pso
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
	$(ROBOT)  merge --input $< reason -e none -r ELK relax reduce -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
$(ONT).obo: $(ONT).owl
	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@


IMPORTS = ncbitaxon ro peco chebi po
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_import.obo,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

imports/%_import.obo: imports/%_import.owl
	$(OWLTOOLS) $(USECAT) $< -o -f obo --no-check $@

# clone remote ontology locally, perfoming some excision of relations and annotations
mirror/%.obo: $(SRC)
	wget --no-check-certificate $(OBO)/$*.obo -O $@ && touch $@
.PRECIOUS: mirror/%.obo

mirror/%.owl: mirror/%.obo
	$(OWLTOOLS) --no-debug $< --remove-annotation-assertions -l -s -d --remove-dangling-annotations --set-ontology-id $(OBO)/$*.owl  -o $@
.PRECIOUS: mirror/%.owl

release: $(ONT).owl $(ONT).obo
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

##### patterns
PATTERNS_DISEASE_OWL = $(patsubst patterns/disease/%.tsv, patterns/ontology_files/%.owl, $(wildcard patterns/disease/*.tsv)) $(patsubst patterns/disease/%.tsv, patterns/ontology_files/%.obo, $(wildcard patterns/disease/*.tsv))
PATTERNS_DEFICIENCY_OWL = $(patsubst patterns/deficiency/%.tsv, patterns/ontology_files/%.owl, $(wildcard patterns/deficiency/*.tsv)) $(patsubst patterns/deficiency/%.tsv, patterns/ontology_files/%.obo, $(wildcard patterns/deficiency/*.tsv))
PATTERNS_EXCESS_OWL = $(patsubst patterns/excess/%.tsv, patterns/ontology_files/%.owl, $(wildcard patterns/excess/*.tsv)) $(patsubst patterns/excess/%.tsv, patterns/ontology_files/%.obo, $(wildcard patterns/excess/*.tsv))


all_patterns: $(PATTERNS_DISEASE_OWL) $(PATTERNS_DEFICIENCY_OWL) $(PATTERNS_EXCESS_OWL)

patterns/ontology_files/%.owl: patterns/disease/%.tsv
	dosdp-tools --outfile=$@ --obo-prefixes=true --template=patterns/disease.yaml --ontology=imports/ncbitaxon_import.owl generate --infile=$< 
	#patterns/apply-pattern.py -P patterns/curie_map.yaml -i patterns/disease/$*.tsv -p patterns/disease.yaml -n $@ > $@ 
	robot annotate -O "http://purl.obolibrary.org/obo/$*.owl" -i $@ -o $@
	
patterns/ontology_files/%.obo: patterns/ontology_files/%.owl
	$(ROBOT) convert -i $< -f obo -o $@

patterns/ontology_files/%.owl: patterns/deficiency/%.tsv
	dosdp-tools --outfile=$@ --obo-prefixes=true --template=patterns/deficiency.yaml --ontology=imports/chebi_import.owl generate --infile=$<
	#patterns/apply-pattern.py -P patterns/curie_map.yaml -i patterns/deficiency/$*.tsv -p patterns/deficiency.yaml -n $@ > $@ 
	robot annotate -O "http://purl.obolibrary.org/obo/$*.owl" -i $@ -o $@
	
patterns/ontology_files/%.obo: patterns/ontology_files/%.owl
	$(ROBOT) convert -i $< -f obo -o $@

patterns/ontology_files/%.owl: patterns/excess/%.tsv
	dosdp-tools --outfile=$@ --obo-prefixes=true --template=patterns/excess.yaml --ontology=imports/chebi_import.owl generate --infile=$<
	#patterns/apply-pattern.py -P patterns/curie_map.yaml -i patterns/excess/$*.tsv -p patterns/excess.yaml -n $@ > $@ 
	robot annotate -O "http://purl.obolibrary.org/obo/$*.owl" -i $@ -o $@
	
patterns/ontology_files/%.obo: patterns/ontology_files/%.owl
	$(ROBOT) convert -i $< -f obo -o $@
