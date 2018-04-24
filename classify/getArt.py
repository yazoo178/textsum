from Bio import Entrez

Entrez.email = "wbriggs2@sheffield.ac.uk"


#id is a string list with pubmed IDs
#two of have a public PMC article, one does not
handle = Entrez.efetch("pubmed", id="19304878,19088134", retmode="xml")

records = Entrez.read(handle)
#print(records)
#checks for all records if they have a PMC identifier
#prints the URL for downloading the PDF
for record in records:
    if record.get('MedlineCitation'):
        if record['MedlineCitation'].get('OtherID'):
           for other_id in record['MedlineCitation']['OtherID']:
               if other_id.title().startswith('Pmc'):
                   print('http://www.ncbi.nlm.nih.gov/pmc/articles/%s/pdf/' % (other_id.title().upper()))