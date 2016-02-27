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

	# match details
	if args.match:
		# get all match_id->match_url pairs
		match_ids = [x['match_id'] for x in live_matches]
		match_ids.extend([x['match_id'] for x in upcoming_matches])
		match_ids.extend([x['match_id'] for x in recent_matches])

		# check if the given ID is known
		if args.match not in match_ids:
			error("Match %s not found" %(args.match))

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

def error(msg):
	c = AnsiColors()
	print("%sERROR%s: %s" %(c.red, c.endc, msg))
	sys.exit(0)


def main():
	args = parse_arguments()
	c = AnsiColors()
	
	if args.game == 'csgo':
		handle_csgo(args)
	else:
		print("%sERROR:%s %s is not yet supported" %(c.red, c.endc, args.game.upper()))


if __name__ == '__main__':
	main()