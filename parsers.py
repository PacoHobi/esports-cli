import urllib2, re

class CsParser:
	def __init__(self):
		pass

	def get_matches(self):
		response = urllib2.urlopen('http://www.gosugamers.net/counterstrike/gosubet')
		html = response.read()
		boxes = re.findall(r'<div class="box">[\s\S]+?(?:<div[^>]+?>[\s\S]+?<\/div>)', html)
		html_live_matches = boxes[0]
		html_upcoming_matches = boxes[1]
		html_recent_matches = boxes[2]

		# upcoming matches
		rows = re.findall(r'<tr>[\s\S]+?<\/tr>', html_upcoming_matches)
		upcoming_matches = []
		for row in rows:
			m = re.search(r'<a href="(?P<url>.+?)"[\s\S]+?opp1">[^>]+>(?P<team1>.+?)<[\s\S]+?bet1">\((?P<bet1>\d+)[\s\S]+?bet2">\((?P<bet2>\d+)[\s\S]+?<span>(?P<team2>.+?)<[\s\S]+?live-in">[^0-9]+(?P<live_in>[^m]+m)', row)
			upcoming_matches.append(m.groupdict())
		
		return ([], upcoming_matches, [])

if __name__ == '__main__':
	parser = CsParser()
	(live_matches, upcoming_matches, recent_matches) = parser.get_matches()
	for match in upcoming_matches:
		print match