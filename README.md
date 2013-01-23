pymdb
=====

Python module to retrieve IMDB movie info from <http://www.imdbapi.com>

## Examples

### Usage as module:

    $ python
    >>> import pymdb
    >>> m = pymdb.Movie('zeitgeist')
    # access by movie attribute (first access will retrieve all data)
    >>> m.year
    u'2007'
    # there is a dict() info you can explore
    >>> m.info.keys()
    [u'plot', u'rated', u'title', u'poster', u'writer', u'imdbrating', u'director',
    u'released', u'actors', u'year', u'genre', u'imdbid', u'runtime', u'response',
    u'imdbvotes']
    # some nice people...
    >>> m.info['actors']
    u'Osama bin Laden, George W. Bush, George Carlin, Tim Galloway'

### Usage as command-line app:

Output is formated for humans:

    $ python pymdb.py 'true lies'
    Title:      True Lies (1994)
    Genre:      Action, Thriller
    Rating:     7.2 (107,213 votes)
    Director:   James Cameron
    Writer:     Claude Zidi, Simon Michaël
    Plot:       Harry Tasker leads a double life. At work he is a government agent with a license to do just about anything, while at home he pretends to be a dull computer salesman. He is on the trail of stolen nuclear weapons that are in the hands of fanatic terrorists when something more important comes up. Harry finds his wife is seeing another man because she needs some adventure in her life. Harry decides to give it to her, juggling pursuit of terrorists on one hand and an adventure for his wife on the other while showing he can Tango all at once.
    Rated:      R
    Poster:     http://ia.media-imdb.com/images/M/MV5BMTM4OTIzNjcxM15BMl5BanBnXkFtZTcwMjc2MzE2MQ@@._V1_SX640.jpg
    Released:   15 Jul 1994
    Actors:     Arnold Schwarzenegger, Jamie Lee Curtis, Tom Arnold, Bill Paxton
    Imdbid:     tt0111503
    Runtime:    2 h 21 min
    Response:   True

## Bugs

Any bug you found, please inform it here <https://github.com/caruccio/pymdb/issues>.
Patches are welcome.

## Boring stuff

    Copyright 2012 Mateus Caruccio, all rights reserved,
    Mateus Caruccio <mateus@caruccio.com>
    Permission is given under the terms of the DWTFYW License (see file LICENSE.txt).
    NO WARRANTY IS EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

### Disclaimer

I have nothing to do with IMDBAPI <http://www.imdbapi.com>.
If they are down, please be patient.
