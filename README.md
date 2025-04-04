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


# TODO:
- Everyone get the model up and running
- We want to eventually train our own dataset. But for now, we're just going to use the built in training one...

## We need to:
1.) Python code to "de-bias" article

2.) Python code to compute a "bias score"

3.) Python code to run output to clean up bad grammar.

4.) Create a dataset of articles

5.) Python code to scrape article from url

6.) Python to compile article into array of sentences or other format for processing.






# Time permitting
7.) Basic Site to demonstrate
8.) Additional info like overall leaning of source, reputable source db, etc...


Add the # you will be working on below your name

## Lia
#4, will try #5, will try #6, + report

## Joe

## Nelly

## Rounaq

## Allison
5







  

