#!/usr/bin/env python3

#Author Abram Roesner 8/12/23

from pyliftover import LiftOver

lo = LiftOver('/var/www/html/Liftover/hg19ToHg38.over.chain.gz')

input_vcf_path = '/var/www/html/Liftover/input/sample.vcf'
output_vcf_path = '/var/www/html/Liftover/input/lifted_sample.vcf'

with open(input_vcf_path, 'r') as infile, open(output_vcf_path, 'w') as outfile:
    for line in infile:
        #Skip header lines
        if line.startswith('#'):
            outfile.write(line)
            continue

        #Split the VCF line into fields
        fields = line.strip().split('\t')
        chrom, pos = fields[0], int(fields[1])

        #Perform the liftover
        lifted_pos = lo.convert_coordinate('chr' + chrom, pos)

        #Check if the liftover was successful
        if lifted_pos:
            new_chrom, new_pos, _, _ = lifted_pos[0]
            new_chrom = new_chrom.replace('chr', '')

            #Update the VCF line with the new coordinates
            fields[0] = new_chrom
            fields[1] = str(new_pos)
            outfile.write('\t'.join(fields) + '\n')
        else:
            #Handle unlifted coordinates as needed
            pass
