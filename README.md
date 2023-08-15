# PharmCat-Web-Project

We provide a basic pipeline to process 23andMe data, converting it into a format suitable for pharmaceutical annotation using PharmCAT. The entire process is designed to run on a Google Cloud Compute server and cost very little in terms of computation power. 
Currently the large alignment files have been removed from this repository due to size constraints - necessary storage is 5gb for the program.  
Without these files the program will not work - that said they are readily accessable online at the pharmcat repo and the Ensembl assembly file for GRCH37

The accessable_types.txt file is the test file that outputs all avaliable annotations according to the file conditions allowed by 23andme. 
You can use it on the html to show sample output. 
Some older versions of the 23andme format don't work - I'm looking at updating this at some point. 

Authorship for the preprocessing unit and the pharmcat tool itself go to their respective authors. 
I merely built an intake device with liftover, conversion, realignment and various beningn features. 
This project will most likely turn into a website at some point. 

Thanks!
-AR

Overview
File Upload: Accepts 23andMe data in .txt format.
Conversion to VCF: Converts the 23andMe data to VCF (Variant Call Format).
Liftover: Changes genomic coordinates from one assembly to another (e.g., hg19 to hg38).
Realignment: Aligns chromasomes for preprocessing
Preprocessing: Prepares the VCF file for use by PharmCAT.
PharmCAT Processing: Generates pharmaceutical annotations.

Prerequisites
Google Cloud Compute server with sufficient resources (CPU, RAM, storage).
Python 3.x installed.
Required tools: bcftools, bgzip, HTSLIB and tabix.
PharmCAT, preprocessor, and pyliftover libraries.
Reference files: Human Reference Genome (GRCh37 and/or GRCh38), PharmCAT PGx variants, and chain file for liftover.

Installation
Clone the repository or download the project files to your Google Cloud Compute server.

Install the required libraries:

alabaster==0.7.8
attrs==19.3.0
Automat==0.8.0
Babel==2.6.0
blessed==1.20.0
blessings==1.7
blinker==1.4
bpython==0.22.1
certifi==2020.6.20
cffi==1.15.1
chardet==4.0.0
charset-normalizer==3.2.0
click==8.1.6
cloud-init==23.2.1
cloudpickle==2.2.1
colorama==0.4.6
command-not-found==0.3
configobj==5.0.6
constantly==15.1.0
cryptography==3.4.8
curtsies==0.3.10
cwcwidth==0.1.6
Cython==3.0.0
dask==2023.5.0
dbus-python==1.2.16
distro==1.7.0
distro-info==0.23+ubuntu1.1
docker==6.1.3
docopt==0.6.2
docutils==0.16
entrypoints==0.3
feedparser==5.2.1
fsspec==2023.6.0
gitsome==0.8.0
greenlet==1.1.2
httplib2==0.20.2
hyperlink==19.0.0
idna==3.3
imagesize==1.2.0
importlib-metadata==6.8.0
incremental==16.10.1
jedi==0.18.0
jeepney==0.7.1
Jinja2==2.10.1
jsonpatch==1.22
jsonpointer==2.0
jsonschema==3.2.0
keyring==23.5.0
language-selector==0.1
launchpadlib==1.10.16
lazr.restfulclient==0.14.4
lazr.uri==1.0.6
locket==1.0.0
MarkupSafe==1.1.0
more-itertools==8.10.0
netifaces==0.11.0
numpy==1.24.4
numpydoc==0.7.0
oauthlib==3.2.0
olefile==0.46
packaging==23.1
pandas==2.0.3
parso==0.8.1
partd==1.4.0
pexpect==4.6.0
Pillow==7.0.0
ply==3.11
prompt-toolkit==2.0.10
pyasn1==0.4.2
pyasn1-modules==0.2.1
pycparser==2.21
Pygments==2.11.2
PyGObject==3.36.0
PyHamcrest==1.9.0
PyJWT==2.3.0
pyliftover==0.4
pymacaroons==0.13.0
PyNaCl==1.3.0
pyOpenSSL==19.0.0
pyparsing==2.4.7
pyperclip==1.8.2
pyrsistent==0.15.5
pysam==0.21.0
pyserial==3.4
python-apt==2.0.1+ubuntu0.20.4.1
python-dateutil==2.8.2
python-debian==0.1.36+ubuntu1.1
pytz==2023.3
pyxdg==0.27
PyYAML==5.4.1
regex==2023.8.8
requests==2.31.0
requests-unixsocket==0.2.0
roman==2.0.0
scikit-allel==1.3.5
SecretStorage==3.3.1
service-identity==18.1.0
setproctitle==1.1.10
simplejson==3.16.0
six==1.16.0
sos==4.4
Sphinx==1.8.5
ssh-import-id==5.10
systemd-python==234
toolz==0.12.0
Twisted==18.9.0
typing-extensions==3.10.0.2
tzdata==2023.3
ubuntu-advantage-tools==8001
ufw==0.36
unattended-upgrades==0.1
urllib3==1.26.5
wadllib==1.3.6
watchdog==2.1.6
wcwidth==0.2.6
websocket-client==1.6.1
xdg==5.0.0
xonsh==0.9.13
zipp==1.0.0


Support and Contributions
PharmCat Team:
Binglan Li	Stanford University
Katrin Sangkuhl	Stanford University
Mark Woon	Stanford University
Michelle Whirl-Carrillo	Stanford University
Ryan Whaley	Stanford University
Yuki Bradford	University of Pennsylvania
Scott Dudek	University of Pennsylvania
Sony Tuteja	University of Pennsylvania
Anurag Verma	University of Pennsylvania
Shefali Setia Verma	University of Pennsylvania
Karl Keat	University of Pennsylvania

Please report any issues or questions

License
MIT standard
