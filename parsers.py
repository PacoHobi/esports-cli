import urllib2, re


class CsParser:

	def __init__(self):
		self.base_url = "http://www.hltv.org"
		self.match_url = self.base_url + '/?pageid=12&matchid=' 

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
			'team1': {'name':'', 'roster':[]},
			'team2': {'name':'', 'roster':[]},
			'date': '',
			'event': '',
			'maps': [],
		}
		
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
			score = {
				'map': map_names[i],
				'team1': nums[0],
				'team2': nums[1],
				'half1_1': nums[2],
				'half1_2': nums[3],
				'half2_1': nums[4],
				'half2_2': nums[5]
			}
			match_details['maps'].append(score)

		return match_details



if __name__ == '__main__':
	from printers import CsPrinter
	parser = HltvCsParser()
	(live_matches, upcoming_matches) = parser.get_matches()
	printer = CsPrinter()
