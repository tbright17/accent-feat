import textgrid, syllabifier, sys
import numpy as np
from phn_info import vowels, consonants

def nPVI(durations):
    """
    Calculate normalized pairwise variability index
    :param durations:
    :return:
    """
    if not durations:
        sys.exit("Empty durations. Exit!")
    s = []
    for idx in range(1,len(durations)):
        s.append(float(durations[idx-1]-durations[idx])/float((durations[idx-1]+durations[idx])/2))

    return 100 / float(len(durations)-1) * np.sum(np.abs(s))

def rPVI(durations):
    """
    Calculate raw pairwise variability index
    :param durations:
    :return:
    """
    if not durations:
        sys.exit("Empty durations. Exit!")
    s = []
    for idx in range(1,len(durations)):
        s.append(float(durations[idx-1]-durations[idx]))

    return np.sum(np.abs(s)) / (len(durations)-1)

def rhythmic_feat(tg_file, threshold = 0.8):
    """
    Return rhythmic features from analysis of alignment file (.textgrid)
    :param tg_file: textgrid file
    :param threshold: duration threshold that a phoneme will be considered as bad alignment
    :return:
    """

    my_tg_file = textgrid.TextGrid()
    my_tg_file.read(tg_file)
    phn_seq = ""
    for intervals in my_tg_file.tiers[1]:
        if intervals.mark is not None:
            if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                phn_seq += " " + intervals.mark

    language = syllabifier.English
    syllables = syllabifier.syllabify(language, str(phn_seq))

    vowel_interval, consonants_interval, syllable_interval, sil_interval = [], [], [], []

    syllable_idx = 0 # determine which syllable current phoneme is in
    syllable_phn_dur = []
    for intervals in my_tg_file.tiers[1]:

        # vowels and consonants
        if intervals.mark is not None:
            if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                if intervals.mark in vowels:
                    if intervals.maxTime - intervals.minTime < threshold:
                        vowel_interval.append(float(intervals.maxTime) - float(intervals.minTime))
                elif intervals.mark in consonants:
                    if intervals.maxTime - intervals.minTime < threshold:
                        consonants_interval.append(float(intervals.maxTime) - float(intervals.minTime))
                else:
                    continue
            else:
                sil_interval.append(float(intervals.maxTime) - float(intervals.minTime))

        #syllables
        if syllable_idx < len(syllables):
            current_syllable = syllables[syllable_idx][1] + syllables[syllable_idx][2] + syllables[syllable_idx][3]
            if intervals.mark is not None:
                if intervals.mark != 'SIL' and intervals.mark != 'SPN':
                    if intervals.mark in current_syllable:
                        if intervals.maxTime - intervals.minTime < threshold:
                            syllable_phn_dur.append(float(intervals.maxTime) - float(intervals.minTime))
                    if intervals.mark == current_syllable[-1]:
                        syllable_idx += 1
                        syllable_interval.append(sum(syllable_phn_dur))
                        syllable_phn_dur = []

    # remove onset and offset silence
    sil_interval_true = sil_interval[1:-1]

    return [np.mean(vowel_interval), np.mean(consonants_interval), np.mean(syllable_interval), # average duration of vowels, consonants and syllables
            np.std(vowel_interval), np.std(consonants_interval), np.std(syllable_interval), # standard deviation of vowels, consonants and syllables
            np.std(vowel_interval)/np.mean(vowel_interval), np.std(consonants_interval)/np.mean(consonants_interval),
            np.std(syllable_interval)/np.mean(syllable_interval), # standard deviation normalized by average
            np.sum(vowel_interval)/float(my_tg_file.maxTime-my_tg_file.minTime),
            np.sum(consonants_interval)/float(my_tg_file.maxTime-my_tg_file.minTime),
            np.sum(syllable_interval)/float(my_tg_file.maxTime-my_tg_file.minTime), # percentage of duration of vowels, consonants and syllables
            float(len(syllable_interval))/float(my_tg_file.maxTime-my_tg_file.minTime), # number of syllables per second
            np.sum(sil_interval_true) / float(float(my_tg_file.maxTime) - float(my_tg_file.minTime) - sil_interval[0]-sil_interval[-1]),
            np.mean(sil_interval_true), np.std(sil_interval_true), # proportion, average and std of silence duration
            rPVI(vowel_interval), rPVI(consonants_interval), rPVI(syllable_interval), # raw PVI of vowels, consonants and syllables
            nPVI(vowel_interval), nPVI(consonants_interval), nPVI(syllable_interval) # normalized PVI of vowels, consonants and syllables
            ], [ "avgV","avgC","avgSyl", "stdV","stdC","stdSyl", "VacroV","VacroC","VacroSyl",
              "perV","perC","perSyl","SylPerSec","perSil","avgSil","stdSil",
              "rPVIV","rPVIC","rPVISyl","nPVIV","nPVIC","nPVISyl"
            ]

# testing
if __name__ == "__main__":

    feats, descrip = rhythmic_feat('/home/ming/Work_Ming/Dissertation/exp_folder/feat_extract/english/align_feat/aligned_textgrid/english32.TextGrid')

    print ("Done")