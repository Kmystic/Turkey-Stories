from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 
ACCESS_ID ='InputAccessID'
SECRET_KEY = 'InputSecretKey'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

title = 'Continue a story by adding a sentence to provided introduction sentence.'
description = ('A sentence is given that begins a story, continue the story with a single sentence.')
keywords = 'story, sentence, writing, creative'

 
#---------------  BUILD OVERVIEW -------------------
 
overview = Overview()
overview.append_field('Title', 'The sentence below constitues the beginning of a story.')
overview.append(FormattedContent('Once upon a time in a land very far away there lived a princess.'))
 
#---------------  BUILD QUESTION 1 -------------------
 
qc1 = QuestionContent()
qc1.append_field('Title','Copy verbatim the provided sentence. Please keep all capitalization and punctuation as given.')
 
fta1 = FreeTextAnswer()
 
q1 = Question(identifier='verify_sentence', content = qc1, answer_spec = AnswerSpecification(fta1), is_required = True)

 
#---------------  BUILD QUESTION 2 -------------------

qc2 = QuestionContent()
qc2.append_field('Title','Type a single sentence to continue the story begun by the given sentence.')
 
fta2 = FreeTextAnswer()

q2 = Question(identifier='verify_sentence', content = qc2, answer_spec = AnswerSpecification(fta2), is_required = True)

#--------------- BUILD THE QUESTION FORM -------------------
 
question_form = QuestionForm()
question_form.append(overview)
question_form.append(q1)
question_form.append(q2)
 
#--------------- CREATE THE HIT -------------------
 
mtc.create_hit(questions=question_form,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)

#--------------- BUILD THE QUESTION FORM -------------------
 
question_form = QuestionForm()
question_form.append(overview)
question_form.append(q1)
question_form.append(q2)
 
#--------------- CREATE THE HIT -------------------
 
mtc.create_hit(questions=question_form,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)