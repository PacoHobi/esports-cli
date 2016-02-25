from parsers import CsParser
from printers import CsPrinter


def main():
	parser = CsParser()
	printer = CsPrinter()
	(live_matches, upcoming_matches, recent_matches) = parser.get_matches()

	print("\nLive matches")
	printer.print_live_matches(upcoming_matches)
	print("\nUpcoming matches")
	printer.print_upcoming_matches(upcoming_matches)
	print("\nRecent matches")
	printer.print_recent_matches(recent_matches)


if __name__ == '__main__':
	main()