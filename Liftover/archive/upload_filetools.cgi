#!/usr/bin/env python3

import cgi
import os
from pyliftover import LiftOver
import pysam
import subprocess

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
if 'file' in form:
    fileitem = form['file']

    if fileitem.filename:
        # Strip leading path from file name
        filename = os.path.basename(fileitem.filename)
        filepath = '/var/www/html/Liftover/input/' + filename
        open(filepath, 'wb').write(fileitem.file.read())

        # Create a LiftOver object
        lo = LiftOver('hg19ToHg38.over.chain.gz')

        # Create a new VCF file
        vcf_out_path = '/var/www/html/Liftover/input/data2.vcf'
        vcf_out = pysam.VariantFile(vcf_out_path, "w")

        # Add required header lines and fields
        vcf_out.header.add_line('##fileformat=VCFv4.2')
        vcf_out.header.add_sample('Sample_1')
        vcf_out.header.add_meta('INFO', items=[('ID', '.'), ('Number', '.'), ('Type', 'String'), ('Description', 'Description here')])
        vcf_out.header.formats.add('GT', '1', 'String', 'Genotype')

        # Read the uploaded file and lift over the coordinates
        with open(filepath, 'r') as file:
            for line in file:
                if line.startswith('#') or line.strip() == '':
                    continue
                rsid, chromosome, position, genotype = line.strip().split('\t')
                lifted = lo.convert_coordinate('chr' + str(chromosome), int(position))
                if lifted:
                    chrom, pos = lifted[0][0], lifted[0][1]
                    ref, alt = genotype[0], genotype[1]
                    record = vcf_out.new_record(contig=chrom, start=pos, stop=pos+1, id=rsid, alleles=(ref, alt))
                    record.samples["Sample_1"]['GT'] = (0, 0)  # Example genotype
                    vcf_out.write(record)

        # Close the file
        vcf_out.close()

        # Path to the PharmCAT VCF Preprocessor script
        preprocessor_script_path = '/var/html/preprocessor/preprocessor/pharmcat_vcf_preprocessor.py'

        # Command to run the preprocessor
        command = f'python3 {preprocessor_script_path} -vcf {vcf_out_path}'

        # Run the command
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the process was successful
        if process.returncode == 0:
            message = 'The file "' + filename + '" was uploaded, processed, and preprocessed successfully'
        else:
            message = 'Preprocessing failed with exit code {}: {}'.format(process.returncode, process.stderr.decode())
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
