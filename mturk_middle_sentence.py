from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 
"""
The purpose of this class is to generate a HIT that provides the turker with a set of one or more sentences that form an incomplete story
Then prompts the turker to add an additional sentece to the provided story.
"""
class MiddleSentenceHit(object):

  def __init__(self, _access_id, _secret_key, _host, _story_sentences):
      """
      Purpose: Initialize the HIT
      Parameters: _access_id, _secret_key and _host to connect to MTurk, _story_sentences is a list of sentences that make up the story 
      """
      self.access_id = _access_id
      self.secret_key = _secret_key
      self.host = _host
      self.story_sentences = _story_sentences
      self.title = 'Continue a story by adding a sentence to provided incomplete story.'
      self.description = ('An incomplete story is provided, add a sentence to continue the story')
      self.keywords = 'story, sentence, writing, creative'

  """
  This function connects to Mturk and generates the hit corresponding to the given story
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

    overview.append_field('Title', 'The following sentences constitute an incomplete story.')
    story = ""
    for sentence in self.story_sentences:
      story += sentence + " "
    overview.append(FormattedContent(story))
  
    # BUILD QUESTION 1: Copy the first sentence of the story 
     
    qc1 = QuestionContent()
    qc1.append_field('Title','Copy verbatim the first sentence of the provided incomplete story. Please keep all capitalization and punctuation as given.')
    fta1 = FreeTextAnswer()
    q1 = Question(identifier='verify_sentence', content = qc1, answer_spec = AnswerSpecification(fta1), is_required = True)

    # BUILD QUESTION 2: Create new sentence 

    qc2 = QuestionContent()
    qc2.append_field('Title','Type a single sentence to continue the story.')
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