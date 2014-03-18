Turkey-Stories
==============

CSCE 438 Project

Instructions:
- Replace the placeholders for the ACCESS_ID and SECRET_KEY in main.py and run main.
- It should run without issue and print out the 'completed' story, you can go to https://workersandbox.mturk.com/ and verify that the hits have been created
* Note that only the hit generating portion of this code is complete. I have placed dummy data instead of actual results to test each HIT. 
* We still need to complete gathering the actual data, and also waiting for the hit completion before generating the subsequent hit
* I have sufficiently commented out the main to point these areas out

Files:
- main.py
	- This file contains an end to end process of generating a turker story.
		- Issues first sentence hits
			- Verifies results
		- Issues voting for those hits
			- Appends results
		- For some number of middle sentences wanted
			- Issues middle sentence hits
				- Verify results
			- Issues voting for those hits
				- Appends results
		- Issues end sentence hits
			- Verfiy results
		- Issues voting for thsoe hits
			- Appends results
		- Publishes story

- HIT Classes: 
	- mturk_first_sentence.py
	  - This python code creates a HIT with two questions. 
	    - Question one asks the turker to copy the provided sentence to verify they are reading the sentence. 
	    - Question two asks the turker to add a sentence to continue the story began by the given sentence.
	- mturk_middle_sentence.py
	  - This python code creates a HIT with two questions. 
	    - Question one asks the turker to copy the first sentence of the provided story to verify they are reading the story. 
	    - Question two asks the turker to add a sentence to continue the story.
	- mturk_end_sentence.py
	  - This python code creates a HIT with two questions. 
	    - Question one asks the turker to copy the first sentence of the provided story to verify they are reading the story.
	    - Question two asks the turker to add a sentence to conclude the story.
	- mturk_vote_senctence.py
	  - This python code creates a HIT with two questions. 
	    - Question one asks the turker to copy the first sentence of the provided story to verify they are reading the story.
	    - Question two asks the turker to pick from a set of sentences the best one to continue the story.
	- mturk_vote_story.py
	  - This python code creates a HIT with two questions. 
	    - Question one asks the turker to copy the first sentence of the second story to verify they are reading the story.
	    - Question two asks the turker to pick from a set of stories the best story.

