from parsers import CsParser
from printers import CsPrinter


def main():
	parser = CsParser()
	printer = CsPrinter()
	(live_matches, upcoming_matches, recent_matches) = parser.get_matches()
	printer.print_upcoming_matches(upcoming_matches)


if __name__ == '__main__':
	main()