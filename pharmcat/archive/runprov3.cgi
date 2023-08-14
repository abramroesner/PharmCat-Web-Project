#!/usr/bin/env python3

import cgi
import os
import subprocess

def main():
    print("Content-Type: text/html\n")


    try:

        # Step 1: Receive the Uploaded File
        form = cgi.FieldStorage()
        if 'file' not in form:
            print("<p>Error: Missing file input.</p>")
            return

        file_item = form['file']
        uploaded_filename = os.path.basename(file_item.filename)
        file_path = os.path.join('/var/www/html/Liftover/input', uploaded_filename)

        # Validate and write the uploaded file
        with open(file_path, 'wb') as f:
            f.write(file_item.file.read())

        # Step 2: Convert 23andMe to BCF
        with open('/var/www/html/log.txt', 'w') as log_file:
    	    subprocess.run(['bcftools', 'convert', '--tsv2vcf', file_path, '-f', '/var/www/html/Liftover/GRCh3.fa', '-s', 'SampleName', '-o', '/var/www/html/Liftover/input/sample.vcf'], stdout=log_file, stderr=log_file)
	
        with open('/var/www/html/log.txt', 'a') as log_file:
            subprocess.run(['python3', '/var/www/html/Liftover/lifter.py'])

        # Step 4: Preprocess with PharmCAT Preprocessor
            subprocess.run(['python3', '/var/www/html/preprocessor/pharmcat_vcf_preprocessor.py', '-vcf', '/var/www/html/Liftover/input/lifted_sample.vcf'])

        # Step 5: Run PharmCAT
            result = subprocess.run([
                'java', '-jar', '/var/www/html/pharmcat/pharmcat.jar', '-vcf', '/var/www/html/Liftover/input/lifted_sample.vcf.bgz', '-o', '/var/www/html/output'
            ], stdout=log_file, stderr=log_file)

            if result.returncode != 0:
                print("<p>Error running PharmCAT. Check log for details.</p>")
                return


        output_file_url = '/output/lifted_sample.report.html'
        print("Status: 302 Found")
        print(f"Location: {output_file_url}\n\n")
        return

    except Exception as e:
        print("<p>An unexpected error occurred:</p>")
        print("<pre>" + str(e) + "</pre>")

if __name__ == "__main__":
    main()
