#!/usr/bin/env python3

import cgi, cgitb
import os, sys
from pyliftover import LiftOver
import pandas as pd
import subprocess

# Path to the reference genome file (please update this accordingly)
reference_genome_path = "/var/www/html/Liftover/hg19.fa"

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
if 'file' in form:
    fileitem = form['file']

    if fileitem.filename:
        # Strip leading path from file name to avoid directory traversal attacks
        filename = os.path.basename(fileitem.filename)
        input_path = '/var/www/html/Liftover/input/' + filename
        open(input_path, 'wb').write(fileitem.file.read())

        # Convert 23andMe data to VCF format using bcftools
        output_bcf_path = '/var/www/html/Liftover/input/sample.bcf'
        convert_command = f"bcftools convert --tsv2vcf {input_path} -f {reference_genome_path} -s SampleName -Ob -o {output_bcf_path}"
        subprocess.run(convert_command, shell=True, check=True)

        # Convert BCF to VCF for further processing
        output_vcf_path = '/var/www/html/Liftover/input/sample.vcf'
        subprocess.run(f"bcftools view {output_bcf_path} > {output_vcf_path}", shell=True)

        # Load VCF data
        # Load 23andMe data, skipping comment lines
        data = pd.read_csv('/var/www/html/Liftover/input/' + filename, sep='\t', skiprows=19, names=['rsid', 'chromosome', 'position', 'genotype'])


        # Create a LiftOver object
        lo = LiftOver('hg19ToHg38.over.chain.gz')

        # Apply the LiftOver to the chromosome and position
        data['lifted'] = data.apply(lambda row: lo.convert_coordinate('chr' + str(row['#CHROM']), row['POS']), axis=1)

        # Separate the lifted coordinates into chromosome and position
        data[['#CHROM', 'POS']] = data['lifted'].apply(lambda x: pd.Series([int(x[0][0][3:]), x[0][1]] if x else [None, None]))

        # Drop the lifted column and rows where the liftover failed
        data = data.drop(columns='lifted').dropna()

        # Save the lifted VCF data
        lifted_vcf_path = '/var/www/html/Liftover/input/data2.vcf'
        data.to_csv(lifted_vcf_path, sep='\t', index=False)

        message = 'The file "' + filename + '" was uploaded, converted to VCF, and lifted over successfully'
    else:
        message = 'No file was uploaded'
else:
    message = 'No file was uploaded'

print("Content-Type: text/html\n")
print("<html>")
print("<body>")
print("<p>%s</p>" % message)
print("</body>")
print("</html>")
