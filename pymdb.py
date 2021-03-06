#!/usr/bin/env python
# coding: utf-8
__doc__ = """
Python module to retrieve IMDB movie info from <http://www.imdbapi.com>

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

    $ python ./pymdb.py 'true lies'
    ---- query:  ['true lies']
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

Print only specific fields:

    $ python ./pymdb.py 'true lies' -f year,genre
    ---- query:  ['true lies']
    ---- fields: ['year', 'genre']
    Year:  1994
    Genre: Action, Thriller

Be quiet about parameters:

    $ python ./pymdb.py 'true lies' -f year,genre -q
    Year:  1994
    Genre: Action, Thriller

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
"""

__title__ = 'pymdb'
__version__ = '0.0.1'
__license__ = 'BSD'
__author__ = """Mateus Caruccio <mateus@caruccio.com>"""
__copyright__ = 'Copyright 2012 Mateus Caruccio'

__all__ = [ 'Movie', 'MovieError' ]

import sys, requests
import json
try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO

DEFAULT_TIMEOUT = 15

class MovieError(Exception):
	'''There was an error while retrieving movie information'''

class Movie(object):
	'''
	Retrieve information from IMDBAPI (http::/www.imdbapi.com, please support them).

	To use it, simply instanciate an object and access the movie attributes.

	>>> import pymdb
	>>> m=pymdb.Movie('true')
	>>> m.year
	u'2010'
	>>> m.title
	u'True Grit'

	The first time a movie attribute is accessed, if needed, it trigger a
	fetch()ed from IMDBAPI. To refresh the data simply call fetch() again.
	All attributes will be fetch()ed at once, not one by one.

	A list of available movie attributes is available in Movie.fields, but
	its content may vary since depends on implementation from http://www.imdbapi.com.

	If download is supplied with a list of field names, those fields will be
	treated as URLs to download. Its content will be stored in 'download' dict() where
	key is the name of th field and value is the fetched content stored as a file-like
	object. If download is set to 'all', then all fields containing
	URLs are download. Failling downloads are stored as None.
	'''

	# this attribute may and probably will vary
	fields = [ 'title', 'genre', 'rating', 'director', 'writer' 'plot',
	           'rated', 'poster', 'released', 'actors', 'imdbid', 'runtime' ]

	def __init__(self, title, url=None, params=None, timeout=DEFAULT_TIMEOUT, download=None):
		self.req_title = title
		self.req_url = url if url else 'http://www.imdbapi.com/'
		self.req_params = params if params else { 'r': 'json', 'plot': 'full', 't': self.req_title }
		self.req_timeout = timeout
		self._info = None
		if download == 'all' or not download:
			pass
		elif isinstance(download, str):
			download = [ download ]
		elif isinstance(download, (list, tuple)):
			for d in download:
				if not isinstance(d, str):
					raise TypeError('Invalid parameter: download expects str() or a list of str()')
		else:
			raise TypeError('Invalid parameter: download expects str() or a list of str()')
		self._ret_fields = download
		self.download = {}

	def fetch(self):
		'''Performs an HTTP request to IMDBAPI and store movie info as a dict() in self.content.
			Movie attributes will also be available as self.<keys_name> attribute (ex: self.actors).
			The original return data is available in self.json as an str()

			Attribute names are lower-case, so it's self.actors, not self.Actors.'''

		try:
			self.json = requests.get(self.req_url, timeout=self.req_timeout, params=self.req_params).content
		except (requests.ConnectionError, requests.RequestException), ex:
			raise MovieError('Movie error: <%s> %s' % (ex.__class__.__name__, ex))

		# there must be an easy way to lower() all keys of a dict
		info = dict()
		res = json.loads(self.json)
		for k, v in res.iteritems():
			k = k.lower()
			if k == 'response':
				if v == 'false' or not v:
					raise MovieError('Error retrieving movie: %s' % res.get('Error', 'Unknown'))
			elif k in [ 'genre', 'actors', 'director', 'writer' ]:
				info[k] = [ x.strip() for x in v.split(',') ]
			elif k == 'year':
				info[k] = int(v)
			elif k == 'imdbrating':
				info[k] = float(v)
			else:
				info[k] = v

			if self._ret_fields:
				if self._ret_fields == 'all' or k in self._ret_fields:
					try:
						if v.startswith('http://') or v.startswith('https://'):
							self.download[k] = StringIO(requests.get(v.strip(), timeout=self.req_timeout).content)
					except (requests.ConnectionError, requests.RequestException):
						pass

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
	import optparse

	parser = optparse.OptionParser()

	parser.add_option('-f', '--fields', dest='fields', type='str',
		help='print comma separated fields only ("?" print available fields)',
		metavar='FIELDS', default='all')

	parser.add_option('-t', '--timeout', dest='timeout', type='int',
		help='set networking timeout', metavar='SECS', default=DEFAULT_TIMEOUT)

	parser.add_option("-i", "--ignore-error",
		action="store_true", dest="ignore_error", default=False,
		help='ignore errors and try next movie')

	parser.add_option("-q", "--quiet",
		action="store_false", dest="verbose", default=True,
		help='do not print header with original request')

	options, movies = parser.parse_args()

	if options.fields == '?':
		print 'Available fields:'
		for f in Movie.fields:
			print f
		sys.exit(0)

	def print_entry(sz, name, value):
		print '%s:%s %s' % (name.lower().capitalize(), ' '*(sz-len(name)), value)

	def tabular(movie, fields):
		if options.verbose:
			print '---- query:  [\'%s\']' % movie.req_title
			if fields is not Movie.fields:
				print '---- fields: %s' % fields
		movie.fetch()
		sz = len(reduce(lambda x, y: x if len(x) > len(y) else y, fields))

		if fields is Movie.fields:
			print_entry(sz, 'title', '%s (%i)' % (movie.title, int(movie.year)))
			print_entry(sz, 'genre', ','.join(movie.genre))
			print_entry(sz, 'rating', '%s (%s votes)' % (movie.imdbrating, movie.imdbvotes))
			print_entry(sz, 'director', ','.join(movie.director))
			print_entry(sz, 'writer', ','.join(movie.writer))
			print_entry(sz, 'actors', ','.join(movie.actors))

			first = [ 'title', 'year', 'genre', 'imdbrating', 'imdbvotes', 'writer', 'director', 'actors' ]
			for k, v in movie.info.iteritems():
				if k not in first:
					print_entry(sz, k, v)
		else:
			for f in fields:
				print_entry(sz, f, movie.info[f])

	if options.fields == 'all':
		fields = Movie.fields
	else:
		fields = [ f.strip().lower() for f in options.fields.split(',') ]

	for title in movies:
		try:
			tabular(Movie(title, timeout=options.timeout), fields)
		except MovieError, ex:
			print ex
			if not options.ignore_error:
				sys.exit(1)
