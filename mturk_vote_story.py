from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 
"""
The purpose of this class is to generate a HIT that provides the turker with a set of one or more sentences that form an incomplete story
It also provides them with a list of continueing sentences in which they are required to vote on the best fitting
"""
class VotingStoryHit(object):

  def __init__(self, _access_id, _secret_key, _host, _vote_stories):
      """
      Purpose: Initialize the HIT
      Parameters: _access_id, _secret_key and _host to connect to MTurk, _vote_stories is a list stories (represented as a list of sentences) i.e. a list of lists
      """
      self.access_id = _access_id
      self.secret_key = _secret_key
      self.host = _host
      self.vote_stories = _vote_stories
      self.title = 'Vote on the best short story'
      self.description = ('A set of stories will be provided, choose the best story')
      self.keywords = 'story, sentence, writing, creative'

  """
  This function connects to Mturk and generates the hit corresponding to the given stories
  """
  def generate_hit(self, num_assignments, hit_duration, hit_reward):
    """
    Purpose: Generate and publish the HIT
    Parameters: num_assignments is the number of avaliable assignments for hit, 
                hit_duration is the duration of the hit in seconds (60*5 for 5 minutes),
                hit_reward is the reward given per hit in dollars (0.05 is 5 cents)
    """
    # CONNECT TO MTURK

    mtc = MTurkConnection(aws_access_key_id = self.access_id,
                      aws_secret_access_key = self.secret_key,
                      host = self.host)

    # BUILD OVERVIEW 
     
    overview = Overview()

    overview.append_field('Title', 'There are several stories below.')
    for i, story in enumerate (self.vote_stories):
      story_string = ""
      for sentence in story:
        story_string += sentence + " "
      overview.append(FormattedContent("Story "+ str(i+1) + ": " + story_string ))
  
    # BUILD QUESTION 1: Copy the first sentence of the story 2
     
    qc1 = QuestionContent()
    qc1.append_field('Title','Copy verbatim the second sentence of Story 1. Please keep all capitalization and punctuation as given. Your sumbission will automatically be rejected if any character is incorrect.')
    fta1 = FreeTextAnswer()
    q1 = Question(identifier='verify_sentence', content = qc1, answer_spec = AnswerSpecification(fta1), is_required = True)

    # BUILD QUESTION 2: Vote on the best story
  
    story_options = []
    for i, story in enumerate (self.vote_stories):
      selection = ("Story " + str(i+1), str(i))
      story_options.append(selection)
    qc2 = QuestionContent()
    qc2.append_field('Title','Choose the best story.')
    fta2 = SelectionAnswer(min=1, max=1,style='radiobutton',
                      selections=story_options,
                      type='text',
                      other=False)
    q2 = Question(identifier='vote_story', content = qc2, answer_spec = AnswerSpecification(fta2), is_required = True)

    # BUILD THE QUESTION FORM 
     
    question_form = QuestionForm()
    question_form.append(overview)
    question_form.append(q1)
    question_form.append(q2)
     
    # CREATE THE HIT 
     
    mtc.create_hit(questions = question_form,
                   max_assignments = num_assignments,
                   title = self.title,
                   description = self.description,
                   keywords = self.keywords,
                   duration = hit_duration,
                   reward = hit_reward)