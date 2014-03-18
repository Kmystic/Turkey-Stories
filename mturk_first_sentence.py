from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 
"""
The purpose of this class is to generate a HIT that provides the turker with a starter_sentence
Then prompts them to copy the given starter_sentence, and provide a sentence to continue the story began by the starter_sentence 
"""
class FirstSentenceHit(object):

  def __init__(self, _access_id, _secret_key, _host, _starter_sentence):
      """
      Purpose: Initialize the HIT
      Parameters: access_id, secret_key and host to connect to MTurk, and a starter_sentence to begin the story
      """
      self.access_id = _access_id
      self.secret_key = _secret_key
      self.host = _host
      self.starter_sentence = _starter_sentence
      self.title = 'Continue a story by adding a sentence to provided introduction sentence.'
      self.description = ('A sentence is given that begins a story, continue the story with a single sentence.')
      self.keywords = 'story, sentence, writing, creative'

  """
  This function connects to Mturk and generates the hit correspodning to the starter_sentence
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
    overview.append_field('Title', 'The sentence below constitues the beginning of a story.')
    overview.append(FormattedContent(self.starter_sentence))
     
    # BUILD QUESTION 1: Copy given sentence 
     
    qc1 = QuestionContent()
    qc1.append_field('Title','Copy verbatim the provided sentence. Please keep all capitalization and punctuation as given.')
    fta1 = FreeTextAnswer()
    q1 = Question(identifier='verify_sentence', content = qc1, answer_spec = AnswerSpecification(fta1), is_required = True)

    # BUILD QUESTION 2: Create new sentence 

    qc2 = QuestionContent()
    qc2.append_field('Title','Type a single sentence to continue the story begun by the given sentence.')
    fta2 = FreeTextAnswer()
    q2 = Question(identifier='create_sentence', content = qc2, answer_spec = AnswerSpecification(fta2), is_required = True)

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


