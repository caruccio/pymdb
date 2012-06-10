#!/usr/bin/env python
# coding: utf-8
__doc__ = """
Python module to retrieve IMDB movie info from <http://www.imdbapi.org>

## Examples

### Usage as module:

    $ python
    >>> import pymdb
    >>> movie = pymdb.Movie('zeitgeist')
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

I have nothing to do with IMDBAPI <http://www.imdbapi.org>.
If they are down, please be patient.
"""

__title__ = 'pymdb'
__version__ = '0.0.1'
__license__ = 'BSD'
__author__ = """Mateus Caruccio <mateus@caruccio.com>"""
__copyright__ = 'Copyright 2012 Mateus Caruccio'

__all__ = [ 'Movie' ]

import sys, requests
import json

class Movie(object):
	'''Retrieve information from IMDBAPI (http::/www.imdbapi.com, please support them).

	To use it, simply instanciate an object and access the movie attributes.

	>>> import pymdb
	>>> m=pymdb.Movie('true')
	>>> m.year
	u'2010'
	>>> m.title
	u'True Grit'

	The first time you access a movie attribute, if necessary, it will be
	fetch()ed from IMDBAPI. To refresh the data simply call fetch(). All attributes
	will be fetch()ed at once, not one by one.'''

	def __init__(self, title, url=None, params=None, timeout=15):
		self.req_title = title
		self.req_url = url if url else 'http://www.imdbapi.com/'
		self.req_params = params if params else { 'r': 'json', 'plot': 'full', 't': self.req_title }
		self.req_timeout = timeout
		self._info = None

	def fetch(self):
		'''Performs an HTTP request to IMDBAPI and store movie info as a dict() in self.content.
			Movie attributes will also be available as self.<keys_name> attribute (ex: self.actors).
			The original return data is available in self.json as an str()

			Attribute names are lower-case, so it's self.actors, not self.Actors.'''

		self.json = requests.get(self.req_url, timeout=self.req_timeout, params=self.req_params).content

		# there must be an easy way to lower() all keys of a dict
		info = dict()
		for k, v in json.loads(self.json).iteritems():
			lk = k.lower()
			info[lk] = v

		self._info = info
		return self._info

	def __getattr__(self, name):
		'''Movie atributes can be accessed by its corresponding class attribute:
		>>> m = Movie('true lies')
		>>> m.fetch()
		>>> m.year
		>>> u'1994'
		'''
		name = name.lower()
		if name not in self.info:
			raise AttributeError(name)
		return self._info.get(name)

	@property
	def info(self):
		return self._info if self._info else self.fetch()

	def __str__(self):
		return str(self.info)

if __name__ == '__main__':
	def tabular(movie):
		movie.fetch()
		sz = len(reduce(lambda x, y: x if len(x) > len(y) else y, movie.info))

		def print_entry(sz, name, value):
			print '%s:%s %s' % (name.capitalize(), ' '*(sz-len(name)), value)

		print_entry(sz, 'title', '%s (%i)' % (movie.title, int(movie.year)))
		print_entry(sz, 'genre', movie.genre)
		print_entry(sz, 'rating', '%s (%s votes)' % (movie.imdbrating, movie.imdbvotes))
		print_entry(sz, 'director', movie.director)
		print_entry(sz, 'writer', movie.writer)

		first = [ 'title', 'year', 'genre', 'imdbrating', 'imdbvotes', 'writer', 'director' ]
		for k, v in movie.info.iteritems():
			if k not in first:
				print_entry(sz, k, v)

	for title in sys.argv[1:]:
		tabular(Movie(title))
