'''
requires python-wordpress-xmlrpc
Install from PyPI using 'easy_install python-wordpress-xmlrpc' or 
						'pip install python-wordpress-xmlrpc'
http://python-wordpress-xmlrpc.readthedocs.org/en/latest/overview.html
'''
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


class WordPressPoster(object):

	def __init__(self, _username, _password, _host):
		self.username = _username
		self.password = _password
		self.host = _host
		# Connect to WordPress
		print('Connecting to WordPress')
		self.wp = Client(_host, _username, _password)


	def post_to_wordpress(self, story):
		# Get number of posts to number the story title, i.e. if this is the 6th story
		# that will get posted the title will be "Story 6"
		print "Retrieving posts"

		# get pages in batches of 20
		num_of_post = 0
		offset = 0
		increment = 20
		while True:
				posts_from_current_batch = self.wp.call(posts.GetPosts({'number': increment, 'offset': offset}))
				if len(posts_from_current_batch) == 0:
						break  # no more posts returned
				else:
					num_of_post += len(posts_from_current_batch)
				offset = offset + increment
		print num_of_post

		# Create new post
		print "Creating new post..."
		post = WordPressPost()
		post.title = 'Story %d' % (num_of_post + 1) # incrementing the number of post by 1
		# convert each sentence to string, and join separated by a space.
		post.content = " ".join(map(str, story))
		post.id = self.wp.call(posts.NewPost(post))

		# publish it
		print "Publishing"
		post.post_status = 'publish'
		self.wp.call(posts.EditPost(post.id, post))
		print "Done!"
