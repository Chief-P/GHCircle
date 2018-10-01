import requests
from bs4 import BeautifulSoup
from myds import LayerQueue, DirectedGraph


# Data fetch
def get_url(username):
	url = 'https://github.com/'
	followers_tail = '?tab=followers'
	following_tail = '?tab=following'

	return url + username + followers_tail, url + username + following_tail


def fetch(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
	resp = requests.get(url, headers=headers)

	return resp.text


def get_userlist(url):
	soup = BeautifulSoup(fetch(url), 'lxml')
	users = soup.find_all('div', attrs={'class':'d-table table-fixed col-12 width-full py-4 border-bottom border-gray-light'})

	userlist = []
	# users = users[:10]
	for user in users:
		userlist.append(user.find('span', attrs={'class':'link-gray pl-1'}).string)

	return userlist


def get_relation(username, digraph):
	print('Getting', username + '...')
	if digraph.is_visited(username): # visited
		print('Visited')
		return [], []
	digraph.append_visited_list(username)

	followers_url, following_url = get_url(username)

	followers = get_userlist(followers_url)
	if len(followers) == 50: # Too Many followers
		print('Too Many Followers')
		return [], []
	for p in followers:
		digraph.add_edge(p, username)

	followings = get_userlist(following_url)
	for p in followings:
		digraph.add_edge(username, p)

	return followers, followings


# Regularizations
def regularize_max_layer(ml):
	if ml < 0:
		ml = 1
	elif ml > 10:
		ml = 10

	return ml


# Remove duplicates in l and items in the intersection of l and n
def remove_duplicates(l, n=None):
	if n == None:
		n = []
	else:
		n = n.get_visited_list()

	simplist = []
	for i in l:
		if i not in simplist and i not in n:
			simplist.append(i)

	return simplist