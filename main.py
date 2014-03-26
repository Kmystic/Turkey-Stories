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


NUM_MIDDLE_SENTENCES = 1
NUM_SAME_STORY = 2

BEG_NUM_ASSIGNMENTS = 3
BEG_HIT_DURATION = 60*10
BEG_HIT_REWARD = 0.01

MIDDLE_NUM_ASSIGNMENTS = 3
MIDDLE_HIT_DURATION = 60*10
MIDDLE_HIT_REWARD = 0.01

END_NUM_ASSIGNMENTS = 3
END_HIT_DURATION = 60*10
END_HIT_REWARD = 0.01

VOTE_NUM_ASSIGNMENTS = 3
VOTE_HIT_DURATION = 60*10
VOTE_HIT_REWARD = 0.01

VOTE_STORY_NUM_ASSIGNMENTS = 3
VOTE_STORY_HIT_DURATION = 60*10
VOTE_STORY_HIT_REWARD = 0.01


'''
Function for obtaining all hits that have been completed or that have expired
'''
def get_all_reviewable_hits(mtc):
	page_size = 100
	hits = mtc.get_reviewable_hits(page_size=page_size)
	print "\t Total results to fetch %s " % hits.TotalNumResults
	print "\t Request hits page %i" % 1
	total_pages = float(hits.TotalNumResults)/page_size
	int_total= int(total_pages)
	if(total_pages-int_total>0):
		total_pages = int_total+1
	else:
		total_pages = int_total
	pn = 1
	while pn < total_pages:
		pn = pn + 1
		print "\t Request hits page %i" % pn
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
			time.sleep(10)
	return hits

def verify_story_sentences(mtc, hits, verify_sentence):
	story_sentence_choices = []
	for hit in hits:
		assignments = mtc.get_assignments(hit.HITId)
		for assignment in assignments:
			values_list = [];
			# Get question form answers
			for question_form_answer in assignment.answers[0]:
				for value in question_form_answer.fields:
					values_list.append(value)
			# Verfify the 'verifiable' copy question answer and approve if correct and reject if not
			if values_list[0] == verify_sentence :
				mtc.approve_assignment(assignment.AssignmentId)
				story_sentence_choices.append(values_list[1])
			else:
				mtc.reject_assignment(assignment.AssignmentId, 'Your submission was rejected because you did not copy the stated sentence correctly.')
		mtc.disable_hit(hit.HITId)
	return story_sentence_choices

def verify_best_choices(mtc, hits, verify_sentence):
	for hit in hits:
		assignments = mtc.get_assignments(hit.HITId)
		list_of_votes = []
		for assignment in assignments:
			values_list = [];
			for question_form_answer in assignment.answers[0]:
				for value in question_form_answer.fields:
					values_list.append(value)
			if values_list[0] == verify_sentence :
				mtc.approve_assignment(assignment.AssignmentId)
				list_of_votes.append(values_list[1])
			else:
				mtc.reject_assignment(assignment.AssignmentId, 'Your submission was rejected because you did not copy the stated sentence correctly.')
		story_best_choice_num = max(list_of_votes, key=list_of_votes.count)
		mtc.disable_hit(hit.HITId)
	return story_best_choice_num

'''
This main function is responsable for generating hits,
'''
if __name__=="__main__":

	'''
	Specify connection
	'''
	mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
						  aws_secret_access_key=SECRET_KEY,
						  host=HOST)	   
	'''
	Starter sentence
	'''
	starter_sentence = "Once upon a time in a land far away there lived princess with skin as pale as snow and hair as red as fire."
	#starter_sentence2 = "A gust of wind blew the bangs from his face as he galloped down the hill."
	#starter_sentence3 = "Tim looked around nervously before reaching his hand into the cookie jar."

	# Stores the resulting stories for the same starter sentence as a list of string lists
	list_of_stories = []
	story_count = 0
	''' 
	Generate NUM_SAME_STORY stories for the same starter sentence 
	'''
	while(story_count != NUM_SAME_STORY):
		'''
		Issue beginning hit
		'''
		print '---------------------------------------'
		print 'Issuing beginning hit for story number ' + str(story_count+1) + '...'
		beg_hit = mturk_first_sentence.FirstSentenceHit(ACCESS_ID, SECRET_KEY, HOST, starter_sentence)
		beg_hit.generate_hit(BEG_NUM_ASSIGNMENTS, BEG_HIT_DURATION, BEG_HIT_REWARD)
		
		''' 
		Wait for hit completion then gather hit data 
		Verify first sentence additions and if valid add them to the list of sentences to be voted on
		Issue hit for voting on first sentences
		'''
		print 'Waiting on beginning hit completion...'
		story_sentence_choices = []
		hits = wait()
		story_sentence_choices = verify_story_sentences(mtc, hits, starter_sentence)
		print 'Beginning hit complete'
		print 'Beginning hit assignment verified results:'
		print '\t ' + str(story_sentence_choices)
		#story is the list of one or more sentences that constitute the story
		story = [starter_sentence]
		print 'Issuing vote hit for beginning assignments...'
		vote_hit = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story, story_sentence_choices)
		vote_hit.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)

		'''
		Wait for hit completion
		Gather best sentence choice results and append them to the story
		'''
		print 'Waiting on vote hit completion...'
		hits = wait()
		story_best_choice = story_sentence_choices[int(verify_best_choices(mtc, hits, starter_sentence))]
		story.append(story_best_choice)
		print 'Vote hit complete'
		print 'Vote hit assignment verfied best choice result:'
		print '\t' + story_best_choice

		

		'''
		Continue issuing hits for creating new sentences and voting until num_middle_sentences is met
		'''
		middle_count = 0
		while(middle_count != NUM_MIDDLE_SENTENCES):
			'''
			Issue hit for adding middle sentence
			'''
			print '---------------------------------------'
			print 'Issuing middle hit number ' + str(middle_count+ 1) + '...'
			middle_hit = mturk_middle_sentence.MiddleSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story)
			middle_hit.generate_hit(MIDDLE_NUM_ASSIGNMENTS, MIDDLE_HIT_DURATION, MIDDLE_HIT_REWARD)
			'''
			Wait on hit completion
			Verify middle sentence additions and if valid add them to the list of sentences to be voted on
			Issue hits for voting on middle sentence
			'''
			print 'Waiting on middle hit completion...'
			story_sentence_choices = []
			hits = wait()
			story_sentence_choices = verify_story_sentences(mtc, hits, starter_sentence)
			print 'Middle hit complete'
			print 'Middle hit assignment verified results:'
			print '\t ' + str(story_sentence_choices)

			print 'Issuing vote hit for middle assignments...'
			vote_hit = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story, story_sentence_choices)
			vote_hit.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)
			'''
			Wait on hit completion
			Gather best sentence choice results and append them to the story
			'''
			print 'Waiting on vote hit completion...'
			hits = wait()
			story_best_choice = story_sentence_choices[int(verify_best_choices(mtc, hits, starter_sentence))]
			story.append(story_best_choice)
			print 'Vote hit complete'
			print 'Vote hit assignment verfied best choice result:'
			print '\t' + story_best_choice

			middle_count += 1

		''' 
		Issue hits for ending sentence
		'''
		print '---------------------------------------'
		print 'Issuing ending hit for story number ' + str(story_count+1) + '...'
		end_hit = mturk_end_sentence.EndSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story)
		end_hit.generate_hit(END_NUM_ASSIGNMENTS, END_HIT_DURATION, END_HIT_REWARD)

		'''
		Wait on hit completion
		Verify end sentence additions and if valid add them to the list of sentences to be voted on
		Issue hits for final voting
		'''
		print 'Waiting on ending hit completion...'
		story_sentence_choices = []
		hits = wait()
		story_sentence_choices = verify_story_sentences(mtc, hits, starter_sentence)
		print 'Ending hit complete'
		print 'Ending hit assignment verified results:'
		print '\t ' + str(story_sentence_choices)
		print 'Issuing vote hit for ending assignments...'
		vote_hit = mturk_vote_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story, story_sentence_choices)
		vote_hit.generate_hit(VOTE_NUM_ASSIGNMENTS, VOTE_HIT_DURATION, VOTE_HIT_REWARD)
		'''
		Wait on hit completion
		Gather best sentence choice results and append them to the story
		'''
		print 'Waiting on vote hit completion...'
		hits = wait()
		story_best_choice = story_sentence_choices[int(verify_best_choices(mtc, hits, starter_sentence))]
		story.append(story_best_choice)
		print 'Vote hit complete'
		print 'Vote hit assignment verfied best choice result:'
		print '\t' + story_best_choice
		print '---------------------------------------'
		print 'Story ' + str(story_count+1) + '...' + ' turker generation complete.'
		print 'Resulting Story:'
		for sentence in story:
			print '\t ' + sentence
		 
		story_count += 1
		list_of_stories.append(story)

	best_story = []
	'''
	If multiple stories for the same starter sentence wanted, issue voting on stories
	'''
	if (NUM_SAME_STORY > 1):
		print 'Issuing final hit to vote on ' + str(NUM_SAME_STORY) + ' number of turker genenerated stories...'    
		vote_story_hit = mturk_vote_story.VotingStoryHit(ACCESS_ID, SECRET_KEY, HOST, list_of_stories)
		vote_story_hit.generate_hit(VOTE_STORY_NUM_ASSIGNMENTS, VOTE_STORY_HIT_DURATION, VOTE_STORY_HIT_REWARD)
		print 'Waiting on vote hit completion...'
		hits = wait()
		best_story = list_of_stories[int(verify_best_choices(mtc, hits, list_of_stories[0][1]))]
		print 'Vote hit complete'
		print 'Vote hit assignment verfied best choice result:'
		print '\t' + str(best_story)
	else:
		best_story = list_of_stories[0]

	'''
	Publish best voted story to WordPress
	'''
	print 'The highest voted story of ' + str(NUM_SAME_STORY) + ' stories has been published at http://turkeystories.wordpress.com'
	wpp = mturk_wordpress.WordPressPoster(WORDPRESS_USERNAME, WORDPRESS_PASSWORD, WORDPRESS_HOST)
	wpp.post_to_wordpress(best_story)
