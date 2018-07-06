# accent-feat
Python 2.X based feature extraction code for accented speech or pathological speech from forced alignment and Goodness of Pronunciation (GOP), including following features
1. Minimum, mean, standard deviation and mean-normalizd standard deviation of GOP values of vowels, consonants and syllables
2. Mean, standard deviation and mean-normalizd standard deviation of durations of vowels, consonants and syllables
3. Mean, standard deviation of durations of silence (begining and closing silence removed)
4. Percentage of vowels, consonants, syllables and silences intervals.
5. Syllables per second
6. Raw and normalized pairwise varibility index (PVI) of durations of vowels, consonants and syllables

Forced alignment files (Praat format .textgrid) and GOP files need to be generated beforehand. Please refer to this repo: [kaldi-dnn-ali-gop](https://github.com/tbright17/kaldi-dnn-ali-gop)

syllabifier.py is retrieved from https://svn.code.sf.net/p/p2tk/code/python/syllabify/syllabifier.py

## Install
Direct download

## Usage
Please refer to test code

## Citation

Please kindly cite the following paper if you find this repo useful in your research:

M. Tu, A. Grabek, J. Liss and V. Berisha, "Investigating the role of L1 in automatic pronunciation evaluation of L2 speech", to appear in proceedings of Interspeech 2018
