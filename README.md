Turkey-Stories
==============

CSCE 438 Project

Instructions:
- In main.py:
	- Replace the placeholders for the ACCESS_ID and SECRET_KEY in main.py and run main.
		- Make sure there are no existing HITs in your account
	- Replace the HOST with the host name of your choice default is mechanical turk sandbox
	- Replace Wordpress credentials with your wordpress credentials or use ours
		- Username: turkeystories
		- The password is the same the class password for accessing the slides. Hint, it had to do with napster
	- Replace constant values with your own choices:
		- Default (for testing purposes):
			- 1 Stories starting with same sentence
			- 1 Assignments for all types of hits
			- 1 Middle sentence
- Compile the and run main.py 'python main.py'
	- It will prompt you to enter a sentence to begin the turker process. Either type in a custom sentence, or type 0 to use one of our defaults.
	- The program will continually run until the entire process is completed, and print out statements to console regarding its status.
	- The progam will also produce a file 'output_file.txt' at the end with the results of the program

Files:
- main.py
	- This file contains an end to end process of generating turker stories, voting on stories, and publishing them to wordpress
		- For each story 
			- Issues first sentence hits
				- Verifies results
			- Issues voting for those hits
				- Verifies results
				- Appends results to story
			- For each middle sentence
				- Issues middle sentence hits
					- Verify results
				- Issues voting for those hits
					- Verifies results
					- Appends results to story
			- Issues end sentence hits
				- Verfiy results
			- Issues voting for those hits
				- Verifies results
				- Appends results to story
		- Issues voting for stories
			- Verifiies results
		- Publishes highest voted story to wordpress
- mturk_wordpress.py
	- Contains a WordPressPoster class which both connencts to WordPress and posts given story
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

