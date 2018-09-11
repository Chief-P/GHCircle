import requests
from bs4 import BeautifulSoup
# from myds import Queue, Graph
from myds import Queue
import networkx as nx
import matplotlib.pyplot as plt


dg = nx.DiGraph()
visited_list = []


def get_url(username):
	url = 'https://github.com/'
	followers_tail = '?tab=followers'
	following_tail = '?tab=following'

	return url + username + followers_tail, url + username + following_tail


def fetch(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
	resp = requests.get(url, headers=headers)

	return resp.text


def get_usrlist(url):
	soup = BeautifulSoup(fetch(url), 'lxml')
	usrs = soup.find_all('div', attrs={'class':'d-table table-fixed col-12 width-full py-4 border-bottom border-gray-light'})

	usrlist = []
	# usrs = usrs[:10]
	for usr in usrs:
		usrlist.append(usr.find('span', attrs={'class':'link-gray pl-1'}).string)

	return usrlist


def get_relation(username):
	print('Getting', username + '...')
	global dg, visited_list
	if username in visited_list: # visited
		print('Visited')
		return [], []
	visited_list.append(username)

	followers_url, following_url = get_url(username)

	followers = get_usrlist(followers_url)
	if len(followers) == 50: # Too Many followers
		print('Too Many Followers')
		return [], []
	for p in followers:
		dg.add_edge(p, username)

	followings = get_usrlist(following_url)
	for p in followings:
		dg.add_edge(username, p)

	return followers, followings


def regularize_ml(ml):
	if ml < 0:
		ml = 1
	elif ml > 10:
		ml = 10

	return ml


def remove_duplicates(l):
	ans = []
	for i in l:
		if i not in ans:
			ans.append(i)
	return ans


def remove_redundance():
	global dg
	delete_list = []
	for n in dg.nodes:
		if dg.in_degree(n) == 1 and dg.out_degree(n) == 0 or dg.out_degree(n) == 1 and dg.in_degree(n) == 0:
			delete_list.append(n)
	for n in delete_list:
		dg.remove_node(n)


def count_layer(src):
	global dg
	bt = nx.bfs_tree(dg, src)

	return nx.dag_longest_path_length(bt)


def display(g, username):
	plt.subplot(111)
	nx.draw(g, with_labels=True)
	plt.savefig(username + ".png")
	plt.show()


def main():
	username = input('Plz input username: ')
	max_layer = input('Plz input max relation layers: ')
	max_layer = regularize_ml(int(max_layer))

	q = Queue()
	q.enqueue(username)
	dg.add_node(username)
	while not q.is_empty() and count_layer(username) < max_layer:
		user = q.dequeue()
		followers, followings = get_relation(user)
		for f in remove_duplicates(followers + followings):
			print(f)
			q.enqueue(f)

	remove_redundance()
	if max_layer < 3:
		display(dg, username)
	# some fuckin analysis of dg here


if __name__ == '__main__':
	main()