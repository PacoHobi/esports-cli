# esports-cli
A command line interface to view all esports matches and scores.

## Demo
![](http://i.imgur.com/KxHSHas.gif)

## Requirements
[Python 2.7](https://www.python.org/downloads/)

## Supported games
Currently the following games are supported:
+ Counter-Strike: Global Offensive
+ Dota 2

More games will be supported in the future.

## Usage
```
$ python esports-cli.py -h
usage: esports-cli.py [-h] [-g {dota,csgo,hs,hots,lol}]
                      [-s {all,live,upcoming,recent}] [-f FILTER] [-m ID]

optional arguments:
  -h, --help            show this help message and exit
  -g {dota,csgo,hs,hots,lol}, --game {dota,csgo,hs,hots,lol}
                        game to use
  -s {all,live,upcoming,recent}, --show {all,live,upcoming,recent}
                        what matches to show
  -f FILTER, --filter FILTER
                        filter to use on team names
  -m ID, --match ID     specify a match ID to show detailed information
```

## Examples
#### Show all Dota 2 matches:
```
$ python esports-cli.py -g dota
```

#### Show only live Dota 2 matches:
```
$ python esports-cli.py -g dota -s live
```

#### Show all CSGO matches, filtering for `cloud`:
```
$ python esports-cli.py -g csgo -f cloud
```

#### Show only upcoming CSGO matches, filtering for `liquid`:
```
$ python esports-cli.py -g csgo -s upcoming -f liquid
```

#### Show CSGO match details for partial ID `87`:
Writing part of an ID is enough, as long as it only matches one ID (e.g. you can type `87` instead of `2301087`).
```
$ python esports-cli.py -g csgo -m 87
```

## Contributing
Open issues on the [issues page](https://github.com/PacoHobi/esports-cli/issues) or create pull request. You can also send me an [email](mailto:hey@pacohobi.com).

All contributions and feedback is appreciated.

## License
Released under the [MIT License](https://github.com/PacoHobi/esports-cli/blob/master/LICENSE).
