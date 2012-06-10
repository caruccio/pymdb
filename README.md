pymdb
=====

Python module to retrieve IMDB movie info from <http://www.imdbapi.org>.

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

### License

    Copyright 2012 Mateus Caruccio, all rights reserved.
    Mateus Caruccio <mateus@caruccio.com>
    Permission is given under the terms of the DWTFYW License (see file LICENSE).
    NO WARRANTY IS EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
