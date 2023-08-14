#!/usr/bin/env python3

import cgi, cgitb
import os, sys
from pyliftover import LiftOver
import pandas as pd
import subprocess

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
if 'file' in form:
    fileitem = form['file']

    if fileitem.filename:
        # Strip leading path from file name to avoid directory traversal attacks
        filename = os.path.basename(fileitem.filename)
        open('/var/www/html/Liftover/input/' + filename, 'wb').write(fileitem.file.read())

        # Load 23andMe data, skipping header rows
        data = pd.read_csv('/var/www/html/Liftover/input/' + filename, sep='\t', skiprows=20, names=['rsid', 'chromosome', 'position', 'genotype'])

        # Create a DataFrame for VCF
        vcf_data = pd.DataFrame({
            '#CHROM': data['chromosome'],
            'POS': data['position'],
            'ID': data['rsid'],
            'REF': data['genotype'].str[0],
            'ALT': data['genotype'].str[1],
            'QUAL': '.',
            'FILTER': '.',
            'INFO': '.',
	    'FORMAT': 'GT',
	    'Sample_1': '0/0'
        })

        # Save the VCF data
        vcf_data.to_csv('/var/www/html/Liftover/input/data.vcf', sep='\t', index=False)

        # Create a LiftOver object
        lo = LiftOver('hg19ToHg38.over.chain.gz')

        # Apply the LiftOver to the chromosome and position
        vcf_data['lifted'] = vcf_data.apply(lambda row: lo.convert_coordinate('chr' + str(row['#CHROM']), row['POS']), axis=1)

        # Separate the lifted coordinates into chromosome and position
        vcf_data[['#CHROM', 'POS']] = vcf_data['lifted'].apply(lambda x: pd.Series([int(x[0][0][3:]), x[0][1]] if x else [None, None]))

        # Drop the lifted column and rows where the liftover failed
        vcf_data = vcf_data.drop(columns='lifted').dropna()

        # Save the lifted VCF data
        vcf_data.to_csv('/var/www/html/Liftover/input/data2.vcf', sep='\t', index=False)

        # Path to the PharmCAT VCF Preprocessor script
        '''preprocessor_script_path = '/var/html/preprocessor/preprocessor/pharmcat_vcf_preprocessor.py'

        # Command to run the preprocessor
        command = f'python3 {preprocessor_script_path} -vcf /var/www/html/Liftover/input/data2.vcf'

        # Run the command
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the process was successful
        if process.returncode == 0:
            message = 'The file "' + filename + '" was uploaded, processed, and preprocessed successfully'
        else:
            message = 'Preprocessing failed: ' + process.stderr.decode()'''
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
