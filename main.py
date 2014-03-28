import mturk_first_sentence
import mturk_vote_sentence
import mturk_middle_sentence
import mturk_end_sentence
import mturk_vote_story
import mturk_vote_end_sentence
import mturk_wordpress
import time
import random
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer

"""
Constant values
"""
ACCESS_ID ='Replace Me'
SECRET_KEY = 'Replace Me'
HOST = 'mechanicalturk.sandbox.amazonaws.com'

WORDPRESS_USERNAME = 'Replace Me'
WORDPRESS_PASSWORD = 'Replace Me'
WORDPRESS_HOST = 'http://turkeystories.wordpress.com/xmlrpc.php'


NUM_MIDDLE_SENTENCES = 1 # Number of middle sentences the story will contain
NUM_SAME_STORY = 1 # Number of stories to produce for the same starter sentence

# Beginning sentence HIT constants
BEG_NUM_ASSIGNMENTS = 1 # Number of turkers to work on this type of assignment
BEG_HIT_DURATION = 60*10 # How long to give the turker before HIT ends
BEG_HIT_REWARD = 0.01 # How much to reward the turker

# Middle sentence HIT constants
MIDDLE_NUM_ASSIGNMENTS = 1
MIDDLE_HIT_DURATION = 60*10
MIDDLE_HIT_REWARD = 0.01

# End sentence HIT constants
END_NUM_ASSIGNMENTS = 1
END_HIT_DURATION = 60*10
END_HIT_REWARD = 0.01

# Vote sentence HIT constants
VOTE_NUM_ASSIGNMENTS = 1
VOTE_HIT_DURATION = 60*10
VOTE_HIT_REWARD = 0.01

# Vote stories HIT constants
VOTE_STORY_NUM_ASSIGNMENTS = 1
VOTE_STORY_HIT_DURATION = 60*10
VOTE_STORY_HIT_REWARD = 0.01

# A list of backup sentences to use in the case where no assignments are accepted
backup_sentences = ['Ya know?', 
                    'Or whatever.',
                    'So...',
                    'Literally.',
					'It was a beautiful sunny day.',
					'It was a very dark day.',
					'The end was near.',
					'It was indeed a tragedy.',
					'It was just the beginning.',
					'No one would have guessed it.',
					'It will never be the same.',
					'Thats right.']

# Returns a list of 3 random sentence choices
def get_random_sentence_choices():
	random_sentence_choices = []
	randNumberList = random.sample(range(len(backup_sentences)),3)
	sentence1 = backup_sentences[randNumberList[0]]
	sentence2 = backup_sentences[randNumberList[1]]
	sentence3 = backup_sentences[randNumberList[2]]
	random_sentence_choices.append(sentence1)
	random_sentence_choices.append(sentence2)
	random_sentence_choices.append(sentence3)
	return random_sentence_choices #list of 3 random sentence choices
		

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
			time.sleep(10) # Time to wait before checking for results in seconds
	return hits

'''
Function to verify the 'verifiable' question in the HITS that add a sentence
Approves or rejects hit if verifiable question correct / incorrect based on sentenced passed in
Returns a list of sentences called story_sentence_choices that contains
the results of all approved HITS 
'''
def verify_story_sentences(mtc, hits, verify_sentence):
	story_sentence_choices = []
	for hit in hits:
		assignments = mtc.get_assignments(hit.HITId)
		assignmentsRejectedCount = 0
		assignmentsCount = 0
		for assignment in assignments:
			assignmentsCount += 1
			values_list = []
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
				assignmentsRejectedCount += 1
		#if all assignments are rejected select a random list of story sentence choices
		if assignmentsRejectedCount == assignmentsCount : 
			story_sentence_choices = list(get_random_sentence_choices())
		mtc.disable_hit(hit.HITId)
	return story_sentence_choices

'''
Function to verify the 'verifiable' question in the HITS that vote on sentences / stories
Approves or rejects hit if verifiable question correct / incorrect based on sentenced passed in
Appends the answer choices together and returns the answer choice with the most votes
(Returns the result as the index of the choice in the list of available choices)
'''
def verify_best_choices(mtc, hits, verify_sentence):
	for hit in hits:
		assignments = mtc.get_assignments(hit.HITId)
		list_of_votes = []
		assignmentsRejectedCount = 0
		assignmentsCount = 0
		for assignment in assignments:
			assignmentsCount += 1
			values_list = [];
			for question_form_answer in assignment.answers[0]:
				for value in question_form_answer.fields:
					values_list.append(value)
			if values_list[0] == verify_sentence :
				mtc.approve_assignment(assignment.AssignmentId)
				list_of_votes.append(values_list[1])
			else:
				mtc.reject_assignment(assignment.AssignmentId, 'Your submission was rejected because you did not copy the stated sentence correctly.')
				assignmentsRejectedCount += 1
		#if all assignments are rejected select the first sentence as the best choice
		if assignmentsRejectedCount == assignmentsCount : 
			story_best_choice_num = 0
		else :
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
	print 'Welcome to Turkey Stories!'
	user_sentence = raw_input('Enter a sentence to begin the story or enter 0 to use a random sentence from our list: ')
	starter_sentence = ""
	if user_sentence == '0':
		starter_sentence_list = ["Once upon a time in a land far away there lived princess with skin as pale as snow and hair as red as fire.",
								"A short time ago, in a land not so far away, there lived an evil professor named Schmaverlee.",
								"Tim looked around nervously before reaching his hand into the cookie jar."]
		starter_sentence = starter_sentence_list[random.randrange(0, len(starter_sentence_list))] #random starter sentence selection
	else:
		starter_sentence = user_sentence
	print 'Turkey Stories will now begin with the following sentence:'
	print starter_sentence
	# Write results to file
	output_file = open('output_file.txt', 'w+')
	output_file.write('Starter sentence: ' + starter_sentence + '\n')


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
		output_file.write('---------------------------------------' + '\n')
		output_file.write('Results for story number ' + str(story_count+1) + ':' + '\n')
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
		output_file.write('Beginning hit assignment verified results:' + '\n')
		output_file.write('\t ' + str(story_sentence_choices) + '\n')
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
		output_file.write('Vote hit assignment verfied best choice result:' + '\n')
		output_file.write('\t' + story_best_choice + '\n')

		

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
			output_file.write('---------------------------------------' + '\n')
			output_file.write('Results for middle hit ' + str(middle_count+ 1) + ':' + '\n')
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
			output_file.write('Middle hit assignment verified results:' + '\n')
			output_file.write('\t ' + str(story_sentence_choices) + '\n')

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
			output_file.write('Vote hit assignment verfied best choice result:' + '\n')
			output_file.write('\t' + story_best_choice + '\n')

			middle_count += 1

		''' 
		Issue hits for ending sentence
		'''
		print '---------------------------------------'
		print 'Issuing ending hit for story number ' + str(story_count+1) + '...'
		output_file.write('---------------------------------------' + '\n')
		output_file.write('Results for ending hit for story number ' + str(story_count+1) + ':' + '\n')
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
		output_file.write('Ending hit assignment verified results:'+ '\n')
		output_file.write('\t ' + str(story_sentence_choices)+ '\n')
		print 'Issuing vote hit for ending assignments...'
		vote_hit = mturk_vote_end_sentence.VotingSentenceHit(ACCESS_ID, SECRET_KEY, HOST, story, story_sentence_choices)
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
		output_file.write('Vote hit assignment verfied best choice result:')
		output_file.write('\t' + story_best_choice + '\n')
		output_file.write('---------------------------------------' + '\n')
		print '---------------------------------------'
		print 'Story ' + str(story_count+1) + '...' + ' turker generation complete.'
		print 'Resulting Story:'
		output_file.write('Resulting Story: '+ '\n' + '\t')
		for sentence in story:
			print '\t ' + sentence
		 	output_file.write(sentence + ' ')
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
		output_file.write('Best voted story: ' + '\n')
		output_file.write('\t' + str(best_story) + '\n')
	else:
		best_story = list_of_stories[0]

	# Close output file
	output_file.close()
	'''
	Publish best voted story to WordPress
	'''
	
	print 'The highest voted story of ' + str(NUM_SAME_STORY) + ' stories has been published at http://turkeystories.wordpress.com'
	wpp = mturk_wordpress.WordPressPoster(WORDPRESS_USERNAME, WORDPRESS_PASSWORD, WORDPRESS_HOST)
	wpp.post_to_wordpress(best_story)
	
