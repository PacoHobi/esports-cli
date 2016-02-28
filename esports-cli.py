import argparse, sys
from parsers import CsParser
from printers import CsPrinter, AnsiColors


def parse_arguments():
	# main parser parameters
	description = None
	epilog = None

	parser = argparse.ArgumentParser(
		description=description,
		epilog=epilog
	)

	# game argument
	parser.add_argument(
		'-g', '--game',
		default = 'csgo',
		choices = ['dota', 'csgo', 'hs', 'hots', 'lol'],
		help = 'game to use'
	)

	# show argument
	parser.add_argument(
		'-s', '--show',
		default = 'all',
		choices = ['all', 'live', 'upcoming', 'recent'],
		help = 'what matches to show'
	)

	# filter argument
	parser.add_argument(
		'-f', '--filter',
		help = 'filter to use on team names'
	)

	# match argument
	parser.add_argument(
		'-m', '--match',
		metavar = 'ID',
		help = 'specify a match ID to show detailed information',
	)	

	args = parser.parse_args()
	return args


def handle_csgo(args):
	c = AnsiColors()
	parser = CsParser()
	printer = CsPrinter()
	(live_matches, upcoming_matches, recent_matches) = parser.get_matches()
	all_matches = live_matches[:]
	all_matches.extend(upcoming_matches)
	all_matches.extend(recent_matches)

	# match details
	if args.match:
		# get all match_id->match_url pairs
		match_ids = [x['match_id'] for x in live_matches]
		match_ids.extend([x['match_id'] for x in upcoming_matches])
		match_ids.extend([x['match_id'] for x in recent_matches])

		# check if the given ID is known
		if args.match not in match_ids:
			# check for a unique partial match
			matches = []
			for id in match_ids:
				if args.match in id:
					matches.append(id)
			# unique partial match
			if len(matches) == 1:
				args.match = matches[0]
			# a few partial matches, make suggestion
			elif len(matches) in range(2,11):
				matches = [m for m in all_matches if m['match_id'] in matches]
				for i,m in enumerate(matches):
					matches[i] = "\t%s - %s vs %s (%s)" %(m['match_id'], m['team1'], m['team2'], m['type'])
				msg = "\n".join(sorted(matches))
				msg = "Match %s not found.\n\nDid you mean one of these matches?\n" %(args.match) + msg
				print_error(msg)
			# none or to many matches, just give an error
			else:
				print_error("Match %s not found" %(args.match))

		# parse match details an print them out
		match_details = parser.get_match_details(args.match)
		printer.print_match_details(match_details)
		return

	if args.show in ['all', 'live']:
		print("\nLive matches")
		printer.print_live_matches(live_matches, filter=args.filter)

	if args.show in ['all', 'upcoming']:
		print("\nUpcoming matches")
		printer.print_upcoming_matches(upcoming_matches, filter=args.filter)

	if args.show in ['all', 'recent']:
		print("\nRecent matches")
		printer.print_recent_matches(recent_matches, filter=args.filter)

def print_info(msg):
	c = AnsiColors()
	print("%sINFO%s: %s" %(c.blue, c.endc, msg))

def print_warning(msg):
	c = AnsiColors()
	print("%sWARNING%s: %s" %(c.blue, c.endc, msg))

def print_error(msg):
	c = AnsiColors()
	print("%sERROR%s: %s" %(c.red, c.endc, msg))
	sys.exit(0)


def main():
	args = parse_arguments()
	c = AnsiColors()
	
	if args.game == 'csgo':
		handle_csgo(args)
	else:
		print_error("%s is not yet supported" %(c.red, c.endc, args.game.upper()))


if __name__ == '__main__':
	main()