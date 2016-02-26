class AnsiColors:
	defaults = {
		'red': '\033[31m',
		'green': '\033[32m',
		'yellow': '\033[33m',
		'blue': '\033[34m',
		'magenta': '\033[35m',
		'cyan': '\033[35m',
		'endc': '\033[m'
	}

	def __init__(self):
		self.__dict__.update(AnsiColors.defaults)


class CsPrinter:
	def __init__(self):
		pass

	def print_live_matches(self, upcoming_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['Team 1', 'Bets','Team 2']
		rows = []
		for match in upcoming_matches:
			if filter and filter not in match['team1'].lower() and filter not in match['team2'].lower():
				continue
			team1 = match['team1']
			bets = "{:>3} % {}".format(match['bet1'], match['bet2'])
			team2 = match['team2']
			row = [team1, bets, team2]
			rows.append(row)
		alignments = ['>', '^', '<']
		self.print_table(header, rows, alignments=alignments)

	def print_upcoming_matches(self, upcoming_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['Team 1', 'Bets', 'Team 2', 'Live in']
		rows = []
		for match in upcoming_matches:
			if filter and filter not in match['team1'].lower() and filter not in match['team2'].lower():
				continue
			team1 = match['team1']
			bets = "{:>3} % {}".format(match['bet1'], match['bet2'])
			team2 = match['team2']
			live_in = match['live_in']
			row = [team1, bets, team2, live_in]
			rows.append(row)
		alignments = ['>', '^', '<', '^']
		self.print_table(header, rows, alignments=alignments)

	def print_recent_matches(self, recent_matches, filter=None):
		c = AnsiColors()
		if filter:
			filter = filter.lower()
		header = ['Team 1', 'Score', 'Team 2', 'Bets']

		# generate rows
		rows = []
		for match in recent_matches:
			if filter and filter not in match['team1'].lower() and filter not in match['team2'].lower():
				continue
			team1 = match['team1']
			bets = "{:>3} % {}".format(match['bet1'], match['bet2'])
			team2 = match['team2']
			score = "{:>2} - {}".format(match['score1'], match['score2'])
			# score = match['score1'] + " - " + match['score2']
			row = [team1, score, team2, bets]
			rows.append(row)

		# generate colors
		colors = [["" for y in range(len(header))] for x in range(len(rows))]
		for i, row in enumerate(rows):
			score1 = int(row[1].split('-')[0])
			score2 = int(row[1].split('-')[1])
			if score1 > score2:
				colors[i][0] = c.green
				colors[i][2] = c.red
			elif score1 == score2:
				colors[i][0] = c.yellow
				colors[i][2] = c.yellow
			else:
				colors[i][0] = c.red
				colors[i][2] = c.green

		# alignments
		alignments = ['>', '^', '<', '^']

		self.print_table(header, rows, alignments=alignments, colors=colors)

	def print_table(self, header, rows, alignments=None, align_titles=True, colors=None, compact=True):
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