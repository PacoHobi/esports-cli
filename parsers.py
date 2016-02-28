import urllib2, re
import pprint

class CsParser:

	def __init__(self):
		self.base_url = "http://www.hltv.org"
		self.match_url = self.base_url + '/?pageid=12&matchid=' 
		# http://www.hltv.org//?pageid=113&matchid=2301070&mapdetails=1&gamestatid=28356&half=0&clean=1

	def get_matches(self):
		# get live and upcoming matches
		req = urllib2.Request(self.base_url + '/matches/', headers={'User-Agent': "Magic Browser"}) 
		res = urllib2.urlopen(req)
		html = res.read()
		
		matches_html = re.findall(r'<div class="matchListRow"[^>]*>[\s\S]+?<div style="clear:both;">', html)
		matches_ids = re.findall(r'<a .*?href="(\/match\/(\d+)[^"]+)', " ".join(matches_html))

		matches = []
		for match_html in matches_html:
			match_fields = re.split(r'<[^>]+>', match_html)
			match_fields = [x.strip() for x in match_fields]
			match_fields = [x for x in match_fields if len(x) > 0]
			matches.append(match_fields)
		
		# get recent matches
		req = urllib2.Request(self.base_url + '/results/', headers={'User-Agent': "Magic Browser"}) 
		res = urllib2.urlopen(req)
		html = res.read()
		
		matches_html = re.findall(r'<div class="matchListRow"[^>]*>[\s\S]+?<div style="clear:both;">', html)
		matches_ids.extend(re.findall(r'<a .*?href="(\/match\/(\d+)[^"]+)', " ".join(matches_html)))

		for match_html in matches_html:
			match_fields = re.split(r'<[^>]+>', match_html)
			match_fields = [x.strip() for x in match_fields]
			match_fields = [x for x in match_fields if len(x) > 0]
			matches.append(match_fields)

		live_matches = []
		upcoming_matches = []
		recent_matches = []
		for i,fields in enumerate(matches):
			match_url = matches_ids[i][0]
			match_id = matches_ids[i][1]
			if len(fields) == 6:
				match = {
					'match_id': match_id,
					'match_url': match_url,
					'type': 'upcoming',
					'time': fields[0],
					'team1': fields[1],
					'team2': fields[4],
					'bo': fields[2]
				}
				upcoming_matches.append(match)
			elif len(fields) == 7:
				if fields[0] == 'Finished':
					continue
				match = {
					'match_id': match_id,
					'match_url': match_url,
					'type': 'recent',
					'team1': fields[1],
					'team2': fields[5],
					'score1': fields[2],
					'score2': fields[4],
					'map': fields[0]
				}
				recent_matches.append(match)
			elif len(fields) == 8:
				match = {
					'match_id': match_id,
					'match_url': match_url,
					'type': 'live',
					'team1': fields[1],
					'team2': fields[6],
					'score1': fields[3],
					'score2': fields[5],
					'map': fields[2],
					'wins1': None,
					'wins2': None
				}
				live_matches.append(match)
			elif len(fields) == 9:
				match = {
					'match_id': match_id,
					'match_url': match_url,
					'type': 'live',
					'team1': fields[1],
					'team2': fields[7],
					'score1': fields[3],
					'score2': fields[5],
					'map': fields[2],
					'wins1': fields[6].split(' - ')[0],
					'wins2': fields[6].split(' - ')[1]
				}
				live_matches.append(match)

		return (live_matches, upcoming_matches, recent_matches)

	def get_match_details(self, match_id):
		req = urllib2.Request(self.match_url + match_id, headers={'User-Agent': "Magic Browser"}) 
		res = urllib2.urlopen(req)
		full_html = res.read()

		# default values
		match_details = {
			'match_id': match_id,
			'live': False,
			'team1': {'name':'', 'country':'', 'roster':[]},
			'team2': {'name':'', 'country':'', 'roster':[]},
			'winner': 0,
			'date': '',
			'time': '',
			'event': '',
			'maps': [],
		}

		# teams names
		html = re.findall(r'span style="font-size: 26px">([\s\S]+?)<\/span>', full_html)
		html = "\n".join(html)
		# countries
		images = re.findall(r'<img .*?src="([^"]+)"', html)
		images = "\n".join(images)
		countries = re.findall(r'(\w+)\.\w+(?:\s|$)', images)
		# names
		names = re.findall(r'<a.+?>(.+?)<\/a>', html)
		# insert values
		match_details['team1']['name'] = names[0]
		match_details['team2']['name'] = names[1]
		match_details['team1']['country'] = countries[0]
		match_details['team2']['country'] = countries[1]

		# date
		html = re.search(r'<div style="text-align:center;font-size:[^>]+>([\s\S]+?)<\/div>', full_html)
		html = html.group(1)
		text = re.findall(r'<span[^>]*>([\s\S]+?)<\/span>', html)
		text = [x.strip() for x in text]
		match_details['date'] = text[0]
		match_details['time'] = text[1]

		# live
		# <div .*?id="time">
		html = re.search(r'<div .*?id="time">', full_html)
		match_details['live'] = html != None


		# event
		html = re.search(r'<div style="text-align:center;font-size: 18px;">[\s\n\t\r]*<a.+?>([^<]+)<\/a>', full_html)
		event = html.group(1)
		match_details['event'] = event.strip()

		# maps/scores
		html = re.search(r'<div id="mapformatbox">[\s\S]+?<div style="clear: both"', full_html)
		html = html.group(0)
		# maps
		images = re.findall(r'<img .*?src="([^"]+)"', html)
		map_names = re.findall(r'(\w+)\.\w+(?:\s|$)', "\n".join(images))
		# scores
		divs = re.findall(r'<div class="hotmatchbox"[\s\S]+?<\/div>', html)
		for i,div in enumerate(divs):
			text = re.sub(r'<[^>]+>', '', div)
			text = re.sub(r'[\s+]', '', text)
			nums = re.findall(r'\d+', text)
			nums.extend([0] * (6 - len(nums)))
			score = {
				'map': map_names[i],
				'team1': int(nums[0]),
				'team2': int(nums[1]),
				'half1_1': int(nums[2]),
				'half1_2': int(nums[3]),
				'half2_1': int(nums[4]),
				'half2_2': int(nums[5]),
				'stats': []
			}
			match_details['maps'].append(score)

		# winner
		wins1 = 0
		wins2 = 0
		for map in match_details['maps']:
			if map['team1'] > map['team2']:
				wins1 += 1
			elif map['team1'] < map['team2']:
				wins2 += 1
		if wins1 > wins2:
			match_details['winner'] = 1
		elif wins1 < wins2:
			match_details['winner'] = 2

		# map details
		# get gamestatids
		game_stat_ids = re.findall(r'<span id="map_link_(\d+)"', full_html)
		game_stat_html = []
		# get stat html for each game
		for id in game_stat_ids:
			url = self.base_url + "/?pageid=113&matchid=%s&mapdetails=1&gamestatid=%s&half=0&clean=1" %(match_id, id)
			req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"}) 
			res = urllib2.urlopen(req)

			html = res.read()
			game_stat_html.append(html)
		# extract the information
		for game_n,html in enumerate(game_stat_html):
			fields = re.findall(r'<div class="covSmallHeadline".*?>(.+?)<\/div>', html)
			fields = [re.sub(r'<[^>]+>', '', x) for x in fields]
			fields = [x.strip() for x in fields]
			fields = fields[5:30] + fields[35:]

			stats = []
			for i in range(0, len(fields), 5):
				player = {
					'player': fields[i],
					'k': fields[i+1].split('-')[0],
					'd': fields[i+1].split('-')[1],
					'diff': fields[i+2],
					'hs': fields[i+3],
					'rating': fields[i+4]
				}
				stats.append(player)
			match_details['maps'][game_n]['stats'] = stats

		pp = pprint.PrettyPrinter()
		# pp.pprint(match_details)

		return match_details