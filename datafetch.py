import requests
from bs4 import BeautifulSoup
# from myds import Stack, Graph
from myds import Stack
import networkx as nx
import matplotlib.pyplot as plt


dg = nx.DiGraph(layer=0)


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
	usrs = usrs[:10]
	for usr in usrs:
		usrlist.append(usr.find('span', attrs={'class':'link-gray pl-1'}).string)

	return usrlist


def get_relation(username):
	print('Getting', username + '...')
	global dg
	if username in dg and dg.out_degree(username) != 0: # visited
		return [], []
	dg.add_node(username, layer=dg.graph['layer'])

	is_deeper = False
	follower_url, following_url = get_url(username)
	followers = get_usrlist(follower_url)
	if len(followers) < 100: # U may not know him, relationship analysis
		for p in followers:
			dg.add_edge(p, username)
			dg.nodes[p]['layer'] = dg.nodes[username]['layer'] + 1
			is_deeper = True
	followings = get_usrlist(following_url)
	for p in followings:
		dg.add_edge(username, p)
		dg.nodes[p]['layer'] = dg.nodes[username]['layer'] + 1
		is_deeper = True

	if is_deeper:
		dg.graph['layer'] += 1

	return followers, followings


def regularize_ml(ml):
	if ml < 0:
		ml = 1
	elif ml > 10:
		ml = 10

	return ml


def display(g, username):
	plt.subplot(111)
	nx.draw(g, with_labels=True, font_weight='bold')
	plt.savefig(username + ".png")
	plt.show()
	


def main():
	username = input('Plz input username: ')
	max_layer = input('Plz input max relation layers: ')
	max_layer = regularize_ml(int(max_layer))

	stack = Stack()
	stack.push(username)
	while not stack.is_empty() and dg.graph['layer'] < max_layer:
		user = stack.pop()
		followers, followings = get_relation(user)
		print(followers + followings)
		for f in followers + followings:
			print(f)
			stack.push(f)

	display(dg, username)
	# some fuckin analysis of dg here


if __name__ == '__main__':
	main()