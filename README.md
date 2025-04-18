# eecs486-group
## sentinment analysis (https://github.com/cjhutto/vaderSentiment.git)
## neutralizing bias (https://github.com/rpryzant/neutralizing-bias.git)


# VENV INSTALL
1.) Clone repo


2.) Move into repo (cd eecs486-group)


3.) Run: 
`python3 -m venv venv`


4.) Run: 
`source venv/bin/activate`


5.) Run: 
`pip install -r requirements.txt`
`python3 -m spacy download en_core_web_sm`


6.) Move to venv 
`cd venv`


7.) Run: 
`python3 lib/python3.13/site-packages/vaderSentiment/vaderSentiment.py`

8.) If you get the nltk error at the end

  1.) Run: python3
  2.) Run: import(nltk)
  3.) Run: nltk.download()
  4.) Select d
  5.) Type in "all"
  6.) q to exit once downloaded
  7.) exit
  8.) Re-run #7

*3 and 4 might be different if you're on windows idk...

# Nuetralizing Bias 
## Installation
Note: you must be in venv before performing the following instructions

enter the ../EECS486-GROUP/neutralizing-bias directory
```
$ pip install -r requirements.txt
$ cd neutralizing-bias-master/src
$ sh download_data_ckpt_and_run_inference.sh
```

if you run into an error involving punk_tab
```
$ python
>> import nltk; nltk.download("punkt_tab")
```

if you have a specific file you want to run bias on, modify runner.sh to utilize your file path in the --test flag

from the src directory
`python3 prepare_sentence.py --file path/to/filename.txt --output path/to/outputdirectory`
`sh runner.sh`


