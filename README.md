# PharmCat-Web-Project
This repository is dedicated to the development of a genomic tool powered by PharmCat to allow the general public to evaluate their genomic data at little to no cost. 
Currently the large alignment files have been removed from this repository due to size constraints. 
Without these files the program will not work - that said they are readily accessable online at the pharmcat repo and the Ensembl assembly file for GRCH37

The accessable_types.txt file is the test file that outputs all avaliable annotations according to the file conditions allowed by 23andme. 
You can use it on the html to show sample output. 
Some older versions of the 23andme format don't work - i'm looking at updating this at some point. 

It's pretty straightforward to run - access the IP:form.html from the google compute server and upload your file and the report will output in the following screen.

Authorship for the preprocessing unit and the pharmcat tool itself go to their respective authors. 

I merely built an intake device with liftover, conversion, realignment and various beningn features. 
This project will most likely turn into a website at some point. 

Thanks!
-AR
