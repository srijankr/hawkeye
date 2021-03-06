'''This script is used to collect the results for the Birdwatch system.'''

import pandas as pd
from tqdm import tqdm
import random
import math
import pickle

notes = pd.read_csv("..//data//notes-00000-13-04-21.tsv", sep='\t')
ratings = pd.read_csv("..//data//ratings-00000-13-04-21.tsv", sep='\t')

'''This function is used to get the top-ranked notes for the tweet that satisfy the criteria'''
def getCurrentlyRatedHelpfulNotesForTweet(ratingsWithNotesForTweet,maxCurrentlyRatedHelpfulNotes = None,minRatingsNeeded = None,minHelpfulnessRatioNeeded = None):
    
    scoredNotes = ratingsWithNotesForTweet.groupby('noteId').sum()
    scoredNotes['helpfulnessRatio'] = scoredNotes['helpful']/scoredNotes['numRatings']
    filteredNotes = scoredNotes[(scoredNotes['numRatings'] >= minRatingsNeeded) & (scoredNotes['helpfulnessRatio'] >= minHelpfulnessRatioNeeded)]
    return filteredNotes.sort_values(by='helpfulnessRatio', ascending=False)[:maxCurrentlyRatedHelpfulNotes]

'''This function is used to find the minimum number of fake accounts needed 
for the note to become the top ranked note and meet all the criteria.'''

def findNumberOfAccountsNeeded(ratingsWithNotesForTweet,candidateNotes,currentlyRatedHelpfulNotesIds,insertion=None,replacement=None):
    
    scoredNotes = ratingsWithNotesForTweet.groupby('noteId').sum()
    scoredNotes['helpfulnessRatio'] = scoredNotes['helpful']/scoredNotes['numRatings']

    #For a random note, do a run through of all the possible number of accounts one can use 
    #to rate this note helpful and bring it to "Currently Rated Helpful" 
    #i.e. top-ranked note in Birdwatrch system(if it is currently not) 
      
    randomNoteId = random.choice(list(candidateNotes))
    numberOfAccounts = 1
    while(True):

        scoredNotesDummy = scoredNotes.copy(deep=True)

        '''We iteratively add fake accounts, which give fake 'helpful' 
        ratings to the note and 'not helpful' 
        ratings to notes currently ranked at the top.''' 
        if insertion:
            #add helpful ratings to random note id
            scoredNotesDummy.loc[randomNoteId, 'helpful'] += numberOfAccounts
            scoredNotesDummy.loc[randomNoteId, 'numRatings'] += numberOfAccounts

        if replacement:
            for top3NoteId in currentlyRatedHelpfulNotesIds:
                scoredNotesDummy.loc[top3NoteId, 'numRatings'] += numberOfAccounts
                scoredNotesDummy.loc[top3NoteId, 'notHelpful'] += numberOfAccounts

        scoredNotesDummy['helpfulnessRatio'] = scoredNotesDummy['helpful']/scoredNotesDummy['numRatings']
        filteredNotesAboveThreshold = scoredNotesDummy[(scoredNotesDummy['numRatings'] >= minRatingsNeeded) & (scoredNotesDummy['helpfulnessRatio'] >= minHelpfulnessRatioNeeded)]
        currentlyRatedHelpfulNotesIdsNew = set(filteredNotesAboveThreshold.sort_values(by='helpfulnessRatio', ascending=False)[:maxCurrentlyRatedHelpfulNotes].index)

        #Does our (current note) occur in the top ranked notes?
        if randomNoteId in currentlyRatedHelpfulNotesIdsNew:
            return numberOfAccounts

        numberOfAccounts += 1  
        #allow a maximum of 10 fake accounts to be used by the attacker (for computational reasons)     
        if numberOfAccounts > 10:
            return 10

'''The variables can be changed according to requirements of your experiments'''

maxCurrentlyRatedHelpfulNotes = 1 #NUMBER OF TOP-RANKED NOTES
minRatingsNeeded = 5 
minHelpfulnessRatioNeeded = 0.84

numberOfAccountsTakenToMakeRandomNoteCurrrentlyRatedHelpful = {}
insertion_bw,replacement_bw = {},{}
default_bw = set()
rem = set()

totalTweets = list(set(notes['tweetId']))
for tweetId in tqdm(totalTweets):
    
    #Get all notes for this tweet
    notesForTweet = notes[notes['tweetId']==tweetId]
    allNotesSet = set(notesForTweet['noteId'])

    #Currently Helpful Notes
    ratingsWithNotesForTweet = notesForTweet.set_index('noteId').join(ratings.set_index('noteId'), lsuffix="_note", rsuffix="_rating", how='left')
    ratingsWithNotesForTweet['numRatings'] = ratingsWithNotesForTweet.apply(lambda x: 0 if math.isnan(x['helpful']) else 1, axis=1)
    currentlyRatedHelpfulNotes = getCurrentlyRatedHelpfulNotesForTweet(ratingsWithNotesForTweet,maxCurrentlyRatedHelpfulNotes = maxCurrentlyRatedHelpfulNotes,minRatingsNeeded = minRatingsNeeded,minHelpfulnessRatioNeeded = minHelpfulnessRatioNeeded)
    currentlyRatedHelpfulNotesIds = set(currentlyRatedHelpfulNotes.index)
   
    #Candidate Notes
    candidateNotes = allNotesSet - currentlyRatedHelpfulNotesIds

    limit = maxCurrentlyRatedHelpfulNotes
    #CASE 1:
    if len(candidateNotes)==0:
        default_bw.add(tweetId)
        continue
        
    #CASE 2:
    elif len(candidateNotes)>0 and len(currentlyRatedHelpfulNotesIds)<limit:
        insertion_bw[tweetId] = findNumberOfAccountsNeeded(ratingsWithNotesForTweet,candidateNotes,currentlyRatedHelpfulNotesIds,insertion=True,replacement=False)    
        
    #CASE 3: 
    elif len(allNotesSet)>limit and len(currentlyRatedHelpfulNotesIds)==limit:
        replacement_bw[tweetId] = findNumberOfAccountsNeeded(ratingsWithNotesForTweet,candidateNotes,currentlyRatedHelpfulNotesIds,insertion=True,replacement=True)
        
    else:
        rem.add(tweetId)

'''The results are stored in the results folder. 
You will need to create an empty results folder if it does not exist.'''

with open('results/bw-insertion.pickle', 'rb') as handle:
        pickle.dump(insertion_bw, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('results/bw-replacement.pickle', 'rb') as handle:
        pickle.dump(replacement_bw, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('results/bw-default.pickle', 'rb') as handle:
        pickle.dump(replacement_bw, handle, protocol=pickle.HIGHEST_PROTOCOL)