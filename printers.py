class ansiColors:
	defaults = {
		'red': '\033[31m'
	}

	def __init__(self):
		self.__dict__.update(ansiColors.defaults)


class CsPrinter:
	def __init__(self):
		pass

	def print_upcoming_matches(self, upcoming_matches):
		c = ansiColors()
		header = ['Team 1', 'Bets', 'Team 2', 'Live in']
		rows = []
		for match in upcoming_matches:
			team1 = match['team1']
			bets = match['bet1'] + "% - " + match['bet2'] + "%"
			team2 = match['team2']
			live_in = match['live_in']
			row = [team1, bets, team2, live_in]
			rows.append(row)
		self.print_table(header, rows)

	def print_table(self, header, rows):
		# calculate columns width
		col_widths = []
		for i in range(len(rows[0])):
			widths = [len(x[i]) for x in rows]
			widths.append(len(header[i]))
			col_widths.append(max(widths))

		# calculate table width
		table_width = sum(col_widths) + len(header) * 3 - 1

		# borders text
		top_border = u'\u2554' + u"\u2564".join([u'\u2550' * (x + 2) for x in col_widths]) + u'\u2557'
		border = u'\u255F' + u"\u253C".join([u'\u2500' * (x + 2) for x in col_widths]) + u'\u2562'
		header_border = u'\u2560' + u"\u256A".join([u'\u2550' * (x + 2) for x in col_widths]) + u'\u2563'
		bottom_border = u'\u255A' + u"\u2567".join([u'\u2550' * (x + 2) for x in col_widths]) + u'\u255D'

		# rows text
		row_format = u'\u2551 ' + u" \u2502 ".join(["{0[" + str(i) + "]:<" + str(x) + "}" for i,x in enumerate(col_widths)]) + u' \u2551'
		rows_text = []
		for row in rows:
			rows_text.append(row_format.format(row))
			rows_text.append(border)
		rows_text.pop()
		
		# header text
		header_text = row_format.format(header)

		# print table
		print(top_border)
		print(header_text)
		print(header_border)
		for row in rows_text:
			print(row)
		print(bottom_border)