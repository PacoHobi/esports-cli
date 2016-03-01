# esports-cli
A command line interface for all esports matches and scores.

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
$ esports -h
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
View live, upcoming and recent Dota 2 matches:
```
python esports-cli.py -g dota
```
![](http://i.imgur.com/S5NyLOJ.png)

View live, upcoming and recent CSGO matches, filtering for `cloud`:
```
python esports-cli.py -g csgo -f cloud
```
![](http://i.imgur.com/mi2cpWc.png)

View CSGO match details for partial ID `87`:
```
python esports-cli.py -g csgo -m 87
```
Writing part of an ID is enough, as long as it only matches one ID (e.g. you can type `87` instead of `2301087`).
![](http://i.imgur.com/c8JcJjE.png)
