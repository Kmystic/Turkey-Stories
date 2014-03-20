import mturk_first_sentence
import mturk_vote_sentence
import mturk_middle_sentence
import mturk_end_sentence
import mturk_vote_story
import mturk_wordpress

"""
Constant values
"""

ACCESS_ID ='InputAccessID'
SECRET_KEY = 'InputSecretKey'
HOST = 'mechanicalturk.sandbox.amazonaws.com'

WORDPRESS_USERNAME = CHANGE_ME_TO_USERNAME
WORDPRESS_PASSWORD = CHANGE_ME_TO_PASSWORD
WORDPRESS_HOST = 'http://turkeystories.wordpress.com/xmlrpc.php'

NUM_MIDDLE_SENTECES = 1

BEG_NUM_ASSIGNMENTS = 1
BEG_HIT_DURATION = 60*5
BEG_HIT_REWARD = 0.01

MIDDLE_NUM_ASSIGNMENTS = 1
MIDDLE_HIT_DURATION = 60*5
MIDDLE_HIT_REWARD = 0.01

END_NUM_ASSIGNMENTS = 1
END_HIT_DURATION = 60*5
END_HIT_REWARD = 0.01

VOTE_NUM_ASSIGNMENTS = 1
VOTE_HIT_DURATION = 60*5
VOTE_HIT_REWARD = 0.01

VOTE_STORY_NUM_ASSIGNMENTS = 1
VOTE_STORY_HIT_DURATION = 60*5
VOTE_STORY_HIT_REWARD = 0.01

"""
This main function is responsable for generating hits,
"""
if __name__=="__main__":
	
	starter_sentence1 = "Once upon a time in a land far away there lived princess with skin as pale as snow and hair as red as fire."
	#starter_sentence2 = "A gust of wind blew the bangs from his face as he galloped down the hill."
	#starter_sentence3 = "Tim looked around nervously before reaching his hand into the cookie jar."

	'''
	Issue beginning hits
	'''
	beg_hit1 = mturk_first_sentence.FirstSentenceHit(ACCESS_ID, SECRET_KEY, HOST, starter_sentence1)
	beg_hit1.generate_hit(BEG_NUM_ASSIGNMENTS, BEG_HIT_DURATION, BEG_HIT_REWARD)


	''' 
	Wait for hit completion then gather hit data 
	Verify first sentence additions and if valid add them to the list of sentences to be voted on
	Issue hits for voting on first sentences
	'''
	#story1 is the list of one ore more sentneces that constitute the story
	story1 = [starter_sentence1]
	#story1_sentence_choices is the list off the resulting sentences from the beg_hits (right now just dummy data)
	story1_sentence_choices = ['She lived a castle surrounded by jagged mountains and cool flowing rivers.', 'She wore a brown skirt.', 'The cat jumped out the window.']
	vote_hit1 = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story1, story1_sentence_choices)
	vote_hit1.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)

	'''
	Wait for hit completion
	Gather best sentence choice results and append them to the story
	'''
	# Replace with actual best choice
	story1_best_choice = 'She lived a castle surrounded by jagged mountains and cool flowing rivers.' 
	story1.append(story1_best_choice)

	'''
	Continue issuing hits for creating new sentences and voting until num_middle_sentences is met
	'''
	count = NUM_MIDDLE_SENTECES
	while(count != 0):
		'''
		Issue hits for adding middle sentence
		'''
		middle_hit1 = mturk_middle_sentence.MiddleSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story1)
		middle_hit1.generate_hit(MIDDLE_NUM_ASSIGNMENTS, MIDDLE_HIT_DURATION, MIDDLE_HIT_REWARD)
		'''
		Wait on hit completion
		Verify middle sentence additions and if valid add them to the list of sentences to be voted on
		Issue hits for voting on middle sentence
		'''
		# Replace with actual choices
		story1_sentence_choices = ['One day an avalanche cascaded down the surrounding mountains and swallowed the castle whole.', 'The turtle was scared.']
		vote_hit1 = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story1, story1_sentence_choices)
		vote_hit1.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)
		'''
		Wait on hit completion
		Gather best sentence choice results and append them to the story
		'''
		# Replace with actual best choice
		story1_best_choice = 'One day an avalanche cascaded down the surrounding mountains and swallowed the castle whole.' 
		story1.append(story1_best_choice)

		count -= 1

	''' 
	Issue hits for ending sentence
	'''
	end_hit1 = mturk_end_sentence.EndSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story1)
	end_hit1.generate_hit(END_NUM_ASSIGNMENTS, END_HIT_DURATION, END_HIT_REWARD)

	'''
	Wait on hit completion
	Verify end sentence additions and if valid add them to the list of sentences to be voted on
	Issue hits for final voting
	'''
	# Replace with actual choices
	story1_sentence_choices = ['The villagers wept for their princess who had skin as pale as snow and hair as red as fire.', 'The dog flew over the moon.']
	vote_hit1 = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story1, story1_sentence_choices)
	vote_hit1.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)
	'''
	Wait on hit completion
	Gather best sentence choice results and append them to the story
	'''
	story1_best_choice = 'The villagers wept for their princess who had skin as pale as snow and hair as red as fire.'
	story1.append(story1_best_choice)

	'''
	Publish the story to word press
	'''
	for sentence in story1:
		print sentence

	'''
	Example to vote on several stories:

	story1 = ['First Sentence.','Second Sentence', 'Third Sentence']
	story2 = ['First Sentence.','Second Sentence', 'Third Sentence']
	stories = []
	stories.append(story1)
	stories.append(story2)
	vote_story_hit1 = mturk_vote_story.VotingStoryHit(ACCESS_ID, SECRET_KEY, HOST, stories)
	vote_story_hit1.generate_hit(VOTE_STORY_NUM_ASSIGNMENTS, VOTE_STORY_HIT_DURATION, VOTE_STORY_HIT_REWARD)
	'''

	# Publish story
	wpp = mturk_wordpress.WordPressPoster(WORDPRESS_USERNAME, WORDPRESS_PASSWORD, WORDPRESS_HOST)
	wpp.post_to_wordpress(story1)
	# TODO: edit ^ to post the story that was voted best
