#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time as TimeClass


class AnsiColors:
	defaults = {
		'red': '\033[31m',
		'green': '\033[32m',
		'yellow': '\033[33m',
		'blue': '\033[34m',
		'magenta': '\033[35m',
		'cyan': '\033[36m',
		'endc': '\033[m',
		'bold': '\033[1m',
		'blink': '\033[5m',
		'italic': '\033[3m',
		'underline': '\033[4m',
		'negative': '\033[7m'
	}

	def __init__(self):
		self.__dict__.update(AnsiColors.defaults)


class CsPrinter:
	def __init__(self):
		pass

	def print_live_matches(self, live_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['ID', 'Team 1', 'Score','Team 2', 'Map']
		rows = []
		for match in live_matches:
			if filter and filter not in match['team1'].lower() and filter not in match['team2'].lower():
				continue
			match_id = match['match_id'][-3:]
			team1 = match['team1']
			team2 = match['team2']
			score = "{:>2} - {:<2}".format(match['score1'], match['score2'])
			map = match['map']
			if map[:-1] == "Best of ":
				map = "bo" + map[-1:]
			if match['wins1'] and match['wins2']:
				map += " (%s-%s)" %(match['wins1'], match['wins2'])
			row = [match_id, team1, score, team2, map]
			rows.append(row)
		alignments = ['<', '>', '^', '<', '<']
		Utils.print_table(header, rows, alignments=alignments)

	def print_upcoming_matches(self, upcoming_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['ID', 'Team 1', 'Bo', 'Team 2', 'Time']
		rows = []
		for match in upcoming_matches:
			if filter and filter not in match['team1'].lower() and filter not in match['team2'].lower():
				continue
			match_id = match['match_id'][-3:]
			team1 = match['team1']
			team2 = match['team2']
			bo = match['bo']
			if bo == "Best of 1":
				bo = "bo1"
			time = match['time']
			row = [match_id, team1, bo, team2, time]
			rows.append(row)
		alignments = ['<', '>', '^', '<', '^']
		Utils.print_table(header, rows, alignments=alignments)

	def print_recent_matches(self, recent_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['ID', 'Team 1', 'Score', 'Team 2', 'Map']

		# generate rows
		rows = []
		for match in recent_matches:
			if filter and filter not in match['team1'].lower() and filter not in match['team2'].lower():
				continue
			match_id = match['match_id'][-3:]
			team1 = match['team1']
			team2 = match['team2']
			score = "{:>2} - {}".format(match['score1'], match['score2'])
			map = match['map']
			if map[:-1] == "Best of ":
				map = "bo" + map[-1:]
			row = [match_id, team1, score, team2, map]
			rows.append(row)

		# generate colors
		colors = [["" for y in range(len(header))] for x in range(len(rows))]
		for i, row in enumerate(rows):
			score1 = int(row[2].split('-')[0])
			score2 = int(row[2].split('-')[1])
			if score1 > score2:
				colors[i][1] = c.green
				colors[i][3] = c.red
			elif score1 == score2:
				colors[i][1] = c.yellow
				colors[i][3] = c.yellow
			else:
				colors[i][1] = c.red
				colors[i][3] = c.green

		# alignments
		alignments = ['<', '>', '^', '<', '<']

		Utils.print_table(header, rows, alignments=alignments, colors=colors)

	def print_match_details(self, match, match_details):
		c = AnsiColors()

		# heading
		# team names and countries
		if match_details['winner'] == 1:
			color1 = c.green
			color2 = c.red
		elif match_details['winner'] == 2:
			color1 = c.red
			color2 = c.green
		else:
			color1 = c.yellow
			color2 = c.yellow
		team1 = "(%s) %s%s%s" %(
			match_details['team1']['country'],
			color1 + c.bold,
			match_details['team1']['name'],
			c.endc
		)
		team2 = "%s%s%s (%s)" %(
			color2 + c.bold,
			match_details['team2']['name'],
			c.endc,
			match_details['team2']['country']
		)
		header = "%s vs %s" % (team1, team2)
		# live
		live = ''
		if match['type'] == 'live':
			live = '%s(live)%s' %(c.red, c.endc)
		# date
		date_time = "%s @ %s %s" %(match_details['date'], match_details['time'], live)
		# event
		event = match_details['event']
		Utils.print_box([header, date_time, event], alignment='^')

		# map general scores
		header = ['Map', 'Score', '1 Half', '2 Half']
		rows = []
		for map in match_details['maps']:
			map_name = map['map']
			score = "{:>2} - {:<2}".format(map['team1'], map['team2'])
			half1 = "{:>2} - {:<2}".format(map['half1_1'], map['half1_2'])
			half1 = "{:>2} - {:<2}".format(map['half1_1'], map['half1_2'])
			half2 = "{:>2} - {:<2}".format(map['half2_1'], map['half2_2'])
			row = [map_name, score, half1, half2]
			rows.append(row)
		alignments = ['<', '^', '^', '^']
		Utils.print_table(header, rows, alignments=alignments)

		# maps stats
		for map in match_details['maps']:
			team1 = match_details['team1']['name']
			team2 = match_details['team2']['name']
			score1 = map['team1']
			score2 = map['team2']
			map_name = map['map']
			score = "{:>2} - {:<2}".format(map['team1'], map['team2'])
			map_stats = map['stats']

			if score1 > score2:
				color1 = c.green
				color2 = c.red
			elif score1 < score2:
				color1 = c.red
				color2 = c.green
			else:
				color1 = c.yellow
				color2 = c.yellow
			print("\n%s | %s%s%s %s - %s %s%s%s" %(
				map_name,
				color1, team1, c.endc, score1,
				score2, color2, team2, c.endc	
			))

			header = [team1, 'K', 'D', '+/-', 'HS %', 'Rating']
			rows = []
			for i in range(len(map_stats)/2):
				stats = map_stats[i]
				name = stats['player']
				k = stats['k']
				d = stats['d']
				diff = stats['diff']
				hs = stats['hs']
				rating = stats['rating']
				row = [name, k, d, diff, hs, rating]
				rows.append(row)
			Utils.print_table(header, rows)
			header = [team2, 'K', 'D', '+/-', 'HS %', 'Rating']
			rows = []
			for i in range(len(map_stats)/2, len(map_stats)):
				stats = map_stats[i]
				name = stats['player']
				k = stats['k']
				d = stats['d']
				diff = stats['diff']
				hs = stats['hs']
				rating = stats['rating']
				row = [name, k, d, diff, hs, rating]
				rows.append(row)
			Utils.print_table(header, rows)


class DotaPrinter:
	def __init__(self):
		pass

	def print_live_matches(self, live_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['ID', 'Team 1', 'Score','Team 2', 'Bo', 'Event']
		rows = []
		for match in live_matches:
			if filter and filter not in match['team1']['team_name'].lower() and \
						  filter not in match['team2']['team_name'].lower() and \
						  filter not in match['team2']['team_tag'].lower() and \
						  filter not in match['team2']['team_tag'].lower():
				continue
			match_id = match['match_id']
			event = match['league']['name']
			team1 = match['team1']['team_tag']
			team2 = match['team2']['team_tag']
			score = "{:>2} - {:<2}".format(match['team1']['score'], match['team2']['score'])
			bo = "bo" + str(match['series_type'])
			row = [match_id, team1, score, team2, bo, event]
			rows.append(row)
		alignments = ['<', '>', '^', '<', '<', '<']
		Utils.print_table(header, rows, alignments=alignments)

	def print_upcoming_matches(self, upcoming_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['ID', 'Team 1', 'Bo', 'Team 2', 'Event', 'Time']
		rows = []
		for match in upcoming_matches:
			if filter and filter not in match['team1']['team_name'].lower() and \
						  filter not in match['team2']['team_name'].lower() and \
						  filter not in match['team2']['team_tag'].lower() and \
						  filter not in match['team2']['team_tag'].lower():
				continue
			match_id = match['match_id']
			event = match['league']['name']
			team1 = match['team1']['team_tag']
			team2 = match['team2']['team_tag']
			bo = "bo%d" % match['series_type']
			time = TimeClass.localtime(float(match['starttime_unix']))
			time = TimeClass.strftime('%d %b %H:%M', time)
			row = [match_id, team1, bo, team2, event, time]
			rows.append(row)
		alignments = ['<', '>', '^', '<', '<', '<']
		Utils.print_table(header, rows, alignments=alignments)

	def print_recent_matches(self, upcoming_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['ID', 'Team 1', 'Score', 'Team 2', 'Event']

		# generate rows
		rows = []
		for match in upcoming_matches:
			if filter and filter not in match['team1'] and filter not in match['team2']:
				continue
			match_id = match['match_id']
			event = match['league_name']
			team1 = match['team1']['team_name']
			team2 = match['team2']['team_name']
			score = "{} - {}".format(match['score1'], match['score2'])
			bo = "bo%s" % match['bo']
			row = [match_id, team1, score, team2, event]
			rows.append(row)

		# generate colors
		colors = [["" for y in range(len(header))] for x in range(len(rows))]
		for i, row in enumerate(rows):
			score1 = upcoming_matches[i]['score1']
			score2 = upcoming_matches[i]['score2']
			if score1 > score2:
				colors[i][1] = c.green
				colors[i][3] = c.red
			elif score1 == score2:
				colors[i][1] = c.yellow
				colors[i][3] = c.yellow
			else:
				colors[i][1] = c.red
				colors[i][3] = c.green

		# alignments
		alignments = ['<', '>', '^', '<', '<']

		Utils.print_table(header, rows, colors=colors, alignments=alignments)

	def print_match_details(self, match_details):
		c = AnsiColors()

		# heading
		# team names and countries
		try:
			if match_details['team1']['winner']:
				color1 = c.green
				color2 = c.red
			elif match_details['team2']['winner']:
				color1 = c.red
				color2 = c.green
		except:
			color1 = c.yellow
			color2 = c.yellow
		team1 = "(%s) %s%s%s" %(
			match_details['team1']['country_code'].upper(),
			color1 + c.bold,
			match_details['team1']['team_name'],
			c.endc
		)
		team2 = "%s%s%s (%s)" %(
			color2 + c.bold,
			match_details['team2']['team_name'],
			c.endc,
			match_details['team2']['country_code'].upper()
		)
		header = "%s vs %s" % (team1, team2)
		# date
		date_time = TimeClass.localtime(float(match_details['starttime_unix']))
		date_time = TimeClass.strftime('%x @ %X', date_time)
		# event
		if match_details['type'] == 'recent':
			event = match_details['league_name']
		else:
			event = match_details['league']['name']
		Utils.print_box([header, date_time, event], alignment='^')


class Utils:

	@staticmethod
	def print_box(text, alignment='<', decode=None):
		lines = text
		if type(text) is str:
			lines = lines.split('\n')
		raw_lines = lines[:]
		for i,line in enumerate(raw_lines):
			raw_lines[i] = re.sub(r'\x1b[^m]*m', '', line)
		length = max([len(x) for x in raw_lines])

		top_border = u'\u250C' + u'\u2500' * (length + 2) + u'\u2510'
		bottom_border = u'\u2514' + u'\u2500' * (length + 2) + u'\u2518'

		for i,line in enumerate(lines):
			if decode:
				line = line.decode(decode)
			color_length = len(lines[i]) - len(raw_lines[i])
			line_format = u'\u2502 {:%s%d} \u2502' % (alignment, length + color_length)
			lines[i] = line_format.format(line)

		print(top_border)
		for line in lines:
			print(line)
		print(bottom_border)

	@staticmethod
	def print_table(header, rows, alignments=None, align_titles=True, colors=None, compact=True, decode=None):
		c = AnsiColors()
		# calculate columns width
		header_widths = []
		col_widths = []
		if len(rows) > 0:
			for i in range(len(rows[0])):
				widths = [len(x[i]) for x in rows]
				widths.append(len(header[i]))
				col_widths.append(max(widths))
		else:
			for w in header:
				col_widths.append(len(w))
		header_widths = col_widths[:]

		# calculate table width
		table_width = sum(col_widths) + len(header) * 3 - 1

		# check colors
		if colors is None:
			colors = [["" for y in range(len(header))] for x in range(len(rows))]

		# check alignments, default is left
		if alignments is None:
			alignments = ["<" for x in range(len(header))]

		# header alignments
		header_alignments = alignments[:]

		# add colors to rows
		changed = [False] * len(header)
		for i in range(len(rows)):
			for j in range(len(rows[i])):
				rows[i][j] = colors[i][j] + rows[i][j] + c.endc
				# adjust col widths to take into account ansi escape codes
				if not changed[j]:
					changed[j] = True
					col_widths[j] = col_widths[j] + len(colors[i][j]) + len(c.endc)

		# borders text
		top_border = u'\u2552' + u"\u2564".join([u'\u2550' * (x + 2) for x in header_widths]) + u'\u2555'
		border = u'\u251C' + u"\u253C".join([u'\u2500' * (x + 2) for x in header_widths]) + u'\u2524'
		header_border = u'\u255E' + u"\u256A".join([u'\u2550' * (x + 2) for x in header_widths]) + u'\u2561'
		bottom_border = u'\u2558' + u"\u2567".join([u'\u2550' * (x + 2) for x in header_widths]) + u'\u255B'

		# rows text
		row_format = u'\u2502 ' + u" \u2502 ".join(["{0[" + str(i) + "]:" + alignments[i] + str(x) + "}" for i,x in enumerate(col_widths)]) + u' \u2502'
		rows_text = []
		for row in rows:
			if decode:
				print row
				row = [x.decode(decode) for x in row]
				print row
			rows_text.append(row_format.format(row))
			if not compact:
				rows_text.append(border)
		# remove last row border
		if not compact and len(rows_text) > 0:
			rows_text.pop()
		
		# header text
		header_format = u'\u2502 ' + u" \u2502 ".join(["{0[" + str(i) + "]:" + header_alignments[i] + str(x) + "}" for i,x in enumerate(header_widths)]) + u' \u2502'
		header_text = header_format.format(header)

		# print table
		print(top_border)
		print(header_text)
		print(header_border)
		for row in rows_text:
			print(row)
		print(bottom_border)