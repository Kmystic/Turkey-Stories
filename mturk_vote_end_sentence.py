from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 
"""
The purpose of this class is to generate a HIT that provides the turker with a set of one or more sentences that form an incomplete story
It also provides them with a list of continueing sentences in which they are required to vote on the best fitting
"""
class VotingSentenceHit(object):

  def __init__(self, _access_id, _secret_key, _host, _story_sentences, _vote_sentences):
      """
      Purpose: Initialize the HIT
      Parameters: _access_id, _secret_key and _host to connect to MTurk, _story_sentences is a list of sentences that make up the story 
                  _vote_sentences is a list of sentences on which the turker should vote
      """
      self.access_id = _access_id
      self.secret_key = _secret_key
      self.host = _host
      self.story_sentences = _story_sentences
      self.vote_sentences = _vote_sentences
      self.title = 'Vote on the best sentence to end the given story.'
      self.description = ('An incomplete story is provided, vote on a set of given sentences to best continue the story.')
      self.keywords = 'story, sentence, writing, creative'

  """
  This function connects to Mturk and generates the hit corresponding to the given story and sentence choices
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

    overview.append_field('Title', 'The following one or more sentences constitute an incomplete story.')
    story = ""
    for sentence in self.story_sentences:
      story += sentence + " "
    overview.append(FormattedContent(story))
  
    # BUILD QUESTION 1: Copy the first sentence of the story 
     
    qc1 = QuestionContent()
    qc1.append_field('Title','Copy verbatim the first sentence of the provided incomplete story. Please keep all capitalization and punctuation as given. Your sumbission will automatically be rejected if any character is incorrect.')
    fta1 = FreeTextAnswer()
    q1 = Question(identifier='verify_sentence', content = qc1, answer_spec = AnswerSpecification(fta1), is_required = True)

    # BUILD QUESTION 2: Vote on the best sentence to continue the story
    
    sentence_options = []
    for i, sentence in enumerate (self.vote_sentences):
      selection = (sentence, str(i))
      sentence_options.append(selection)
    qc2 = QuestionContent()
    qc2.append_field('Title','Choose the best sentence to end the story.')
    fta2 = SelectionAnswer(min=1, max=1,style='radiobutton',
                      selections=sentence_options,
                      type='text',
                      other=False)
    q2 = Question(identifier='vote_sentence', content = qc2, answer_spec = AnswerSpecification(fta2), is_required = True)

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