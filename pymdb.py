#!/usr/bin/env python
# coding: utf-8
__doc__ = """
Python module to retrieve IMDB movie info from <http://www.imdbapi.org>

## Examples

### Usage as module:

    $ python
    >>> import pymdb
    >>> movie = pymdb.Movie('true lies')
    >>> result = movie.fetch()
    >>> type(result)
    <type 'dict'>
    >>> result.keys()
    ['Plot', 'Rated', 'Title', 'Writer', 'Actors', 'Runtime', 'imdbVotes', 'Poster', 'Response', 'Director', 'Released', 'Year', 'Genre', 'imdbRating', 'imdbID']
    >>> result['Title']
    'True Lies'
    >>> result['Genre']
    'Action, Thriller'
    >>> result['Year']
    '1994'

### Usage as command-line app:

    $ pymdb.py 'true lies'
         Title: True Lies
         Genre: Action, Thriller
          Year: 1994
    imdbRating: 7.2
          Plot: Harry Tasker leads a double life ... showing he can Tango all at once.
         Rated: R
        Writer: Claude Zidi, Simon Michaël
        Actors: Arnold Schwarzenegger, Jamie Lee Curtis, Tom Arnold, Bill Paxton
       Runtime: 2 h 21 min
    imdbVotes: 107,213
        Poster: http://ia.media-imdb.com/images/M/MV5BMTM4OTIzNjcxM15BMl5BanBnXkFtZTcwMjc2MzE2MQ@@._V1_SX640.jpg
      Response: True
      Director: James Cameron
      Released: 15 Jul 1994
       imdbID: tt0111503

## Boring stuff

Copyright 2012 Mateus Caruccio, all rights reserved,
Mateus Caruccio <mateus@caruccio.com>
Permission is given under the terms of the DWTFYW License (see file LICENSE.txt).
NO WARRANTY IS EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
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
	# IMDBAPI is dead slow. Please, donate some nice hardware to them.
	timeout = 15

	def __init__(self, title, url=None, params=None):
		self.title = title
		self.url = url if url else 'http://www.imdbapi.com/'
		self.params = params if params else { 'r': 'json', 'plot': 'full', 't': title }
		self.content = None

	def fetch(self):
		json_content = requests.get(self.url, timeout=self.timeout, params=self.params).content
		self.content = json.loads(json_content)
		return self.content

	def __str__(self):
		if not self.content:
			return '%s' % self.fetch()
		else:
			return self.content

if __name__ == '__main__':
	def tabular(movie):
		sz = len(reduce(lambda x, y: x if len(x) > len(y) else y, movie))
		header = [ 'Title', 'Genre', 'Year', 'imdbRating' ] # print first

		def print_entry(sz, name, value):
			print '%s:%s %s' % (name, ' '*(sz-len(name)), value)

		for h in header:
			v = movie[h]
			print_entry(sz, h, v)
		for k, v in movie.iteritems():
			if k not in header:
				print_entry(sz, k, v)

	for title in sys.argv[1:]:
		tabular(Movie(title).fetch())
