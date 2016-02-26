import urllib2, re

class CsParser:

	team_names = {
		'k1ck eSports...': 'k1ck eSports Club',
		'Counter...': 'Counter Logic Gaming.CS',
		'Ninjas in...': 'Ninjas in Pyjamas',
		'ex-Astral...': 'ex-Astral Authority'
	}

	def __init__(self):
		pass

	def get_matches(self):
		response = urllib2.urlopen('http://www.gosugamers.net/counterstrike/gosubet')
		html = response.read()
		boxes = re.findall(r'<div class="box">[\s\S]+?(?:<div[^>]+?>[\s\S]+?<\/div>)', html)
		html_live_matches = boxes[0]
		html_upcoming_matches = boxes[1]
		html_recent_matches = boxes[2]

		# live matches
		rows = re.findall(r'<tr>[\s\S]+?<\/tr>', html_live_matches)
		live_matches = []
		for row in rows:
			m = re.search(r'<a href="(?P<url>.+?)"[\s\S]+?opp1">[^>]+>(?P<team1>.+?)<[\s\S]+?bet1">\((?P<bet1>\d+)[\s\S]+?bet2">\((?P<bet2>\d+)[\s\S]+?<span>(?P<team2>.+?)<', row)
			dic = m.groupdict()
			dic['team1'] = self.clean_team_name(dic['team1'])
			dic['team2'] = self.clean_team_name(dic['team2'])
			live_matches.append(dic)

		# upcoming matches
		rows = re.findall(r'<tr>[\s\S]+?<\/tr>', html_upcoming_matches)
		upcoming_matches = []
		for row in rows:
			m = re.search(r'<a href="(?P<url>.+?)"[\s\S]+?opp1">[^>]+>(?P<team1>.+?)<[\s\S]+?bet1">\((?P<bet1>\d+)[\s\S]+?bet2">\((?P<bet2>\d+)[\s\S]+?<span>(?P<team2>.+?)<[\s\S]+?live-in">[^0-9]+(?P<live_in>[^m]+m)', row)
			dic = m.groupdict()
			dic['team1'] = self.clean_team_name(dic['team1'])
			dic['team2'] = self.clean_team_name(dic['team2'])
			upcoming_matches.append(dic)

		# recent matches
		rows = re.findall(r'<tr>[\s\S]+?<\/tr>', html_recent_matches)
		recent_matches = []
		for row in rows:
			m = re.search(r'<a href="(?P<url>.+?)"[\s\S]+?opp1">[^>]+>(?P<team1>.+?)<[\s\S]+?bet1">\((?P<bet1>\d+)[\s\S]+?bet2">\((?P<bet2>\d+)[\s\S]+?<span>(?P<team2>.+?)<[\s\S]+?score[^->]+>(?P<score1>\d+)[\s\S]+?score[^>]+>(?P<score2>\d+)', row)
			dic = m.groupdict()
			dic['team1'] = self.clean_team_name(dic['team1'])
			dic['team2'] = self.clean_team_name(dic['team2'])
			if int(dic['score1']) > int(dic['score2']):
				dic['winner'] = 1
			else:
				dic['winner'] = 2
			recent_matches.append(dic)
		
		return (live_matches, upcoming_matches, recent_matches)

	def clean_team_name(self, name):
		if name in self.team_names.keys():
			return self.team_names[name]
		else:
			return name