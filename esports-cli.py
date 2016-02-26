import argparse
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

	args = parser.parse_args()
	return args


def handle_csgo(args):
	c = AnsiColors()
	parser = CsParser()
	printer = CsPrinter()
	(live_matches, upcoming_matches, recent_matches) = parser.get_matches()

	if args.show in ['all', 'live']:
		print("\nLive matches")
		printer.print_live_matches(live_matches, filter=args.filter)

	if args.show in ['all', 'upcoming']:
		print("\nUpcoming matches")
		printer.print_upcoming_matches(upcoming_matches, filter=args.filter)

	if args.show in ['all', 'recent']:
		print("\nRecent matches")
		printer.print_recent_matches(recent_matches, filter=args.filter)


def main():
	args = parse_arguments()
	c = AnsiColors()
	
	if args.game == 'csgo':
		handle_csgo(args)
	else:
		print("%sERROR:%s %s is not yet supported" %(c.red, c.endc, args.game.upper()))


if __name__ == '__main__':
	main()