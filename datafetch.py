import requests
from bs4 import BeautifulSoup
from myds import Stack, Graph
# import analysis


graph = Graph()


def get_url(username):
	url = 'https://github.com/'
	follower_tail = '?tab=follower'
	following_tail = '?tab=following'

	return url + username + follower_tail, url + username + following_tail


def fetch(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
	resp = requests.get(url, headers=headers)

	return resp.text


def get_usrlist(url):
	soup = BeautifulSoup(fetch(url), 'lxml')
	usrs = soup.find_all('div', attrs={'class':'d-table table-fixed col-12 width-full py-4 border-bottom border-gray-light'})

	usrlist = []
	for usr in usrs:
		usrlist.append(usr.find('span', attrs={'class':'link-gray pl-1'}).string)

	return usrlist


def get_relation(username):
	print('Getting', username + '...')
	global graph
	if graph.has_node(username):
		return [], []
	graph.add_node(username)

	follower_url, following_url = get_url(username)
	followers = get_usrlist(follower_url)
	for p in followers:
		graph.add_edge(p, username)
	followings = get_usrlist(following_url)
	for p in followings:
		graph.add_edge(username, p)

	return followers, followings


def regularize_ml(ml):
	if ml < 0:
		ml = 1
	elif ml > 10:
		ml = 10

	return ml


def main():
	username = input('Plz input username: ')
	max_layer = input('Plz input max relation layers: ')
	max_layer = regularize_ml(int(max_layer))

	stack = Stack()
	stack.push(username)
	layer = 0
	while not stack.is_empty() and layer < max_layer:
		user = stack.pop()
		followers, followings = get_relation(user)
		for f in followers + followings:
			stack.push(f)
		layer += 1

	# analysis.showGraph(graph)
	graph.display()
	# some fuckin analysis of graph here


if __name__ == '__main__':
	main()