import mturk_first_sentence
import mturk_vote_sentence
import mturk_middle_sentence
import mturk_end_sentence
import mturk_vote_story
import mturk_wordpress
import time
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer

"""
Constant values
"""

ACCESS_ID ='replace with ACCESS_ID'
SECRET_KEY = 'replace with SECRET_KEY'
HOST = 'mechanicalturk.sandbox.amazonaws.com'


WORDPRESS_USERNAME = 'replace with USERNAME'
WORDPRESS_PASSWORD = 'replace with PASSWORD'
WORDPRESS_HOST = 'http://turkeystories.wordpress.com/xmlrpc.php'


NUM_MIDDLE_SENTECES = 1

BEG_NUM_ASSIGNMENTS = 2
BEG_HIT_DURATION = 60*5
BEG_HIT_REWARD = 0.01

MIDDLE_NUM_ASSIGNMENTS = 1
MIDDLE_HIT_DURATION = 60*5
MIDDLE_HIT_REWARD = 0.01

END_NUM_ASSIGNMENTS = 1
END_HIT_DURATION = 60*5
END_HIT_REWARD = 0.01

VOTE_NUM_ASSIGNMENTS = 2
VOTE_HIT_DURATION = 60*5
VOTE_HIT_REWARD = 0.01

VOTE_STORY_NUM_ASSIGNMENTS = 1
VOTE_STORY_HIT_DURATION = 60*5
VOTE_STORY_HIT_REWARD = 0.01


'''
Function for obtaining all hits that have been completed or that have expired
'''
def get_all_reviewable_hits(mtc):
	page_size = 100
	hits = mtc.get_reviewable_hits(page_size=page_size)
	print "Total results to fetch %s " % hits.TotalNumResults
	print "Request hits page %i" % 1
	total_pages = float(hits.TotalNumResults)/page_size
	int_total= int(total_pages)
	if(total_pages-int_total>0):
		total_pages = int_total+1
	else:
		total_pages = int_total
	pn = 1
	while pn < total_pages:
		pn = pn + 1
		print "Request hits page %i" % pn
		temp_hits = mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
		hits.extend(temp_hits)
	return hits

'''
Function for waiting
'''
def wait() :
	while True:
		hits = get_all_reviewable_hits(mtc)
		if len(hits) == 1 :
			break
		else:
			time.sleep(60)
	return hits

"""
This main function is responsable for generating hits,
"""
if __name__=="__main__":

	'''
	Specify connection
	'''
	mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
						  aws_secret_access_key=SECRET_KEY,
						  host=HOST)	   
	'''
	Story Starters
	'''
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
	
	#story1_sentence_choices is the list off the resulting sentences from the beg_hits (right now just dummy data)
	#story1_sentence_choices = ['She lived a castle surrounded by jagged mountains and cool flowing rivers.', 'She wore a brown skirt.', 'The cat jumped out the window.']
	story1_sentence_choices = []
	hits = wait()
	for hit in hits:
		assignments = mtc.get_assignments(hit.HITId)
		for assignment in assignments:
			print "Answers of the worker %s" % assignment.WorkerId
			values_list = [];
			for question_form_answer in assignment.answers[0]:
				for value in question_form_answer.fields:
					print value
					values_list.append(value)
			if values_list[0] == starter_sentence1 :
				mtc.approve_assignment(assignment.AssignmentId)
				story1_sentence_choices.append(values_list[1])
			else:
				mtc.reject_assignment(assignment.AssignmentId)
			print "--------------------"
		mtc.disable_hit(hit.HITId)

	#story1 is the list of one ore more sentences that constitute the story
	story1 = [starter_sentence1]
	vote_hit1 = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story1, story1_sentence_choices)
	vote_hit1.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)

	'''
	Wait for hit completion
	Gather best sentence choice results and append them to the story
	'''
	hits = wait()
	for hit in hits:
		assignments = mtc.get_assignments(hit.HITId)
		list_of_votes = []
		for assignment in assignments:
			print "Answers of the worker %s" % assignment.WorkerId
			values_list = [];
			for question_form_answer in assignment.answers[0]:
				for value in question_form_answer.fields:
					print value
					values_list.append(value)
			if values_list[0] == starter_sentence1 :
				mtc.approve_assignment(assignment.AssignmentId)
				list_of_votes.append(values_list[1])
			else:
				mtc.reject_assignment(assignment.AssignmentId)
			print "--------------------"
		print list_of_votes
		story1_best_choice_num = max(list_of_votes, key=values_list.count)
		print story1_best_choice_num
		story1_best_choice = story1_sentence_choices[int(story1_best_choice_num)]
		print story1_best_choice
		mtc.disable_hit(hit.HITId)

	story1.append(story1_best_choice)

"""

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
	

"""

	# Publish story
	wpp = mturk_wordpress.WordPressPoster(WORDPRESS_USERNAME, WORDPRESS_PASSWORD, WORDPRESS_HOST)
	wpp.post_to_wordpress(story1)
	# TODO: edit ^ to post the story that was voted best
