#!/usr/bin/env python3
import cgi
import os
import subprocess

print("Content-Type: text/html") # or text/html; charset=utf-8
print("") # Empty line to end headers


# Step 1: Receive the Uploaded File
form = cgi.FieldStorage()
file_item = form['file']
uploaded_filename = os.path.basename(file_item.filename)
file_path = os.path.join('/var/www/html/Liftover/input', uploaded_filename)

with open(file_path, 'wb') as f:
    f.write(file_item.file.read())

# Step 2: Convert 23andMe to BCF
subprocess.run([
    'bcftools', 'convert', '--tsv2vcf', file_path, '-f', '/var/www/html/Liftover/GRCh3.fa', '-s', 'SampleName', '-o', '/var/www/html/Liftover/input/sample.vcf'
])

# Step 3: Perform Liftover
subprocess.run(['python3', '/var/www/html/Liftover/lifter.py'])  # Replace with actual path to lifter.py

# Step 4: Preprocess with PharmCAT Preprocessor
subprocess.run([
    'python3', '/var/www/html/preprocessor/pharmcat_vcf_preprocessor.py', '-vcf', '/var/www/html/Liftover/input/lifted_sample.vcf'
])

# Step 5: Run PharmCAT
subprocess.run([
    'java', '-jar', '/var/www/html/pharmcat/pharmcat.jar', '-vcf', '/var/www/html/Liftover/input/lifted_sample.vcf.bgz', '-o', '/var/www/html/output'
])

# Step 6: Display the Results (assuming the result is an HTML file)
print("Content-Type: text/html") # or text/html; charset=utf-8
print("") # Empty line to end headers

output_file_path = '/var/www/html/output/lifted_sample.report.html'
with open(output_file_path, 'r') as f:
    html_content = f.read()
print(html_content)
