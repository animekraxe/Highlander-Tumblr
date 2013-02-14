from django.core.files.storage import default_storage

from blog.models import TextPost, PhotoPost, VideoPost, AudioPost, QuotePost, LinkPost, ChatPost

import threading

amazon_url = "https://s3-us-west-1.amazonaws.com/highlander-tumblr-test-bucket/"

# Upload to s3 using filepath starting from bucket root
def upload_to_s3(file, filepath):
	destination = default_storage.open(filepath, 'wb+')
	for chunk in file.chunks():
		destination.write(chunk)
	destination.close()

def s3_thread(file, filepath):
	thread = threading.Thread(target=upload_to_s3,args=(file, filepath))
	thread.daemon = True
	thread.start()

# Delete from s3 using filepath starting from bucket root
def delete_from_s3(filepath):
	if default_storage.exists(filepath):
		default_storage.delete(filepath)

# Deletes post and remove from s3 if it is a media post
def delete_post(post):
	classname = post.classname()
	if classname == "PhotoPost" or classname == "VideoPost" or classname == "AudioPost":
		filepath = post.url.replace(amazon_url,'')
		delete_from_s3(filepath)
		post.delete()
	else:
		post.delete()

#Gets every post type from a particular author and returns them in a list
#Not garunteed to be sorted
def get_user_posts(author):
	textposts = list(author.textpost_set.all())
	photoposts = list(author.photopost_set.all())
	videoposts = list(author.videopost_set.all())
	audioposts = list(author.audiopost_set.all())
	quoteposts = list(author.quotepost_set.all())
	linkposts = list(author.linkpost_set.all())
	chatposts = list(author.chatpost_set.all())
	return textposts + photoposts + videoposts + audioposts + quoteposts + linkposts + chatposts

# gets all the posts from all people a user has followed
def get_followed_posts(user):
	following = user.userprofile.following.all()
	posts = []
	for author in following:
		posts += get_user_posts(author.user)
	return posts

def get_user_posts_by_tag(author,tag):
	textposts = list(author.textpost_set.filter(tags__name__in=[tag]))
	photoposts = list(author.photopost_set.filter(tags__name__in=[tag]))
	videoposts = list(author.videopost_set.filter(tags__name__in=[tag]))
	audioposts = list(author.audiopost_set.filter(tags__name__in=[tag]))
	quoteposts = list(author.quotepost_set.filter(tags__name__in=[tag]))
	linkposts = list(author.linkpost_set.filter(tags__name__in=[tag]))
	chatposts = list(author.chatpost_set.filter(tags__name__in=[tag]))
	return textposts + photoposts + videoposts + audioposts + quoteposts + linkposts + chatposts

def get_followed_posts_by_tag(user,tag):
	following = user.userprofile.following.all()
	posts = []
	for author in following:
		posts += get_user_posts_by_tag(author.user,tag)
	return posts

def sort_posts_by_oldest(posts):
	posts = sorted(posts, key=lambda post: post.post_date)
	return posts

def sort_posts_by_newest(posts):
	posts = reversed(sorted(posts, key=lambda post: post.post_date))
	return posts

def get_tag_list(tags):
	tag_tokens = []
	tmp = ""
	for i in range(0, len(tags)):
		if (tags[i] == ','):
			tmp = tmp.strip()
			if (len(tmp) > 0):
				tag_tokens.append(tmp)
				tmp = ""
		elif (i == len(tags)-1):
			tmp = tmp + tags[i]
			tmp = tmp.strip()
			if (len(tmp) > 0):
				tag_tokens.append(tmp)
				tmp = ""
		else:
			tmp = tmp + tags[i]

	return tag_tokens

# post is a taggable object
# tags is a string that contains tag_tokens
def save_tags (post, tags):
	tag_tokens = get_tag_list(tags)

	for i in range(0, len(tag_tokens)):
		post.tags.add(tag_tokens[i]);
		
	post.save();


