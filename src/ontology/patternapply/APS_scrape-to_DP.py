import csv
import pandas as pd
import numpy as np





 # desired header order:
 # iri	iri label	pathogen	pathogen label	host	host label	plantstructure	plantstructure label

 # iri  (OOPS:xxx)
 # iri_label (disease common name)
 # pathogen (NCBITaxon:xxxxxx)
 # pathogen_label ( pathogen name )
 # host (NCBITaxon:xxxxxx)
 # host_label (host common name)
 # plantstructure (PO:xxx)
 # plantstructure_label (common name)

raw_scrape_file = 'aps_with_po_mappings'
# raw_scrape_file = 'xaa'

twelve = 0
fourteen = 0
other = 0


def disease_name_formatter(rawname,host,pathogen,part):
    short_name = rawname.split('(')[0].strip()
    print('{} {} of {}'.format(pathogen, short_name, host))


with open(raw_scrape_file,'r') as infile:
    for line in infile:
        # print(len(line.split('\t')))
        l = line.split('\t')
        # print(l[0])
        disease_name_formatter(l[0],l[2],l[1],"leaf")
        if len(line.split('\t')) == 12:
            twelve += 1
        elif len(line.split('\t')) == 14:
            fourteen += 1
        else:
            other += 1

print('twelve = {}\nfourteen = {}\nother = {}'.format(twelve,fourteen, other))

df = pd.read_csv(raw_scrape_file, sep='\t')

print(len(list(df)))

headers = list(df)

df['plant_part_name'].fillna('whole plant', inplace=True)
df['plant_part_id'].fillna('http://purl.obolibrary.org/obo/PO_0000003', inplace=True)

print(df['plant_part_name'], df['plant_part_id'])
