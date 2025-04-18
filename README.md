# EECS 486, Team 27
## Using LLMs to Identify and Neutralize Biased Information in News Media


# Overview
### This project aims to address the pervasive issue of biased reporting in news media. Biased language not only distorts public perception but also deepens political and social polarization. By developing a system that identifies and neutralizes biased language, we seek to empower readers with more balanced and objective information, ultimately fostering critical thinking and reducing polarization. Our approach combines sentiment analysis, source verification, and Large Language Model (LLM)-based text rewriting to detect and neutralize biased language. This work contributes to the ongoing effort to mitigate the spread of misinformation and encourage more constructive dialogue by providing a neutral perspective on news coverage.


# Installation
#### IMPORTANT NOTE: The installation/training of the model below takes anywhere from 2-5 hours. 

#### For demonstration/testing purposes, please refer to [this section.](#for-demo-purposes)

#### This setup assumes a Linx platform.

## Step 0: Clone the repository.
```bash
git clone https://github.com/rkmaxhero/eecs486-group.git
```
## Step 1: Venv Setup

1. **Move to root directory**  
```bash
cd eecs486-group
```
2. **Create venv**
```bash
python3 -m venv venv
```
3. **Activate venv**
```bash
source venv/bin/activate
```
4. **Install requirements**
```bash
pip install -r requirements.txt
```
5. **Download spacy core**
```bash
python3 -m spacy download en_core_web_sm
```
6. **Move to venv**
```bash
cd venv
```
7. **Prepare VADER**
```bash
python3 lib/python3.13/site-packages/vaderSentiment/vaderSentiment.py
```

#### If you have issues with this, it is likely with nltk package. Try
```bash
python3
# in python3 terminal
import(nltk)
nltk.download()
# when prompted, select option d, and type in "all"
exit

Rerun step 7.
```

## Step 2: Neutralizer Setup
0. **You should still be in the venv...**
1. **Move to root directory**  
```bash
cd eecs486-group/neutralizing-bias-master
```
3. **Install requirements**
```bash
pip install -r requirements.txt
```
4. **Move to src**
```bash
cd src
```
5. **Download model + dataset (this takes forever....)**
```bash
sh download_data_ckpt_and_run_interface.sh
```
#### If you have issues with this, it is likely with punk_tab package. Try
```bash
python3
# in python3 terminal
import(nltk)
nltk.download("punkt_tab")
exit
```

# Running the model
## For Development
1. **Add documents to src/parsed_articles folder**  
	Note: These files must match the format: 1 sentence per line
2. **Move to src directory and run:**  
	Note: This can also take some time depending on the size of your corpus.
```bash
sh train_complete.sh {parsed_articles_directory}
```
3. **Clean output from VADER**
```bash
python3 cleanoutput.py
```
4. **Create score files**
```bash
python3 library/score.py
```
5. **Create score files**
```bash
python3 scoreFinal.py
```

## For Demo Purposes
1. **Create score files**
```bash
python3 library/score.py
```
2. **Create score files**
```bash
python3 scoreFinal.py
```
Final scores will be saved to training_ouput/{source}_final_bias.txt

## Additional Tools
Vader often creates some grammatical errors. If you would like to run your output files through a cleaner before computing the bias score you can do the following:
1. **Install openjdk if not on your system already (needed for packages)**
```bash
sudo apt install openjdk-17-jre
```
2. **Move to /cleaning and created in and out directories**
```bash
cd cleaning
mkdir in
mkdir out
```
3. **To clean all files**
```bash
python3 batchclean.py
```
3. **To clean specific file**
```bash
python3 singleclean.py
```

# References
## Sentinment analysis (https://github.com/cjhutto/vaderSentiment.git)
## Neutralizing bias (https://github.com/rpryzant/neutralizing-bias.git)