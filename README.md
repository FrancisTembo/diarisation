# DIARISATION👶🏿👶🏾  

 This repository contains tools that enable diarisation for child language environment analysis.

 ## Dependancies
 These tools have been developed and tested in an Ubuntu 20 enviroment using Python 3.8.
```
 pip install -r requirements.txt
```
## Running speech extractor 
```
 python run.py -s CHI -w False
```
The argument -s determines the target speaker. The available choices are MOT for mother and CHI for child. The argument -w determines whether to save the spectrogram for the extracted speech utterance or not.
Without saving the spectrogram: 
```
 python run.py -s CHI
```
To save the spectogram: 
```
 python run.py -s CHI -w True
```
## Repository structure
#### dataset
* Contains a .cha transcript and the corresponding audio file for demonstration.  
#### output
* Holds the results when running experiments with scripts. The extracted utterances and spectrograms are stored under this directory in seperate folders.  
#### run.py
* Script to extract speech utterances for a given speaker according to the timestamps provided on the .cha.   
#### spectrogrammer.py
* Helper script for producing spectograms.
#### utils.py
* Helper script with various utility functions.