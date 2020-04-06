import sqlite3
import atexit
import re
import os
import pkg_resources


def _regexp(pattern, string):
    """Simple custom regex search function

    SQLite does not come with a predefined regular expression function.
    We define our own in order to access Python's powerful regex module.

    Parameters
    ----------
    pattern : str
        Regular expression to match against
    string : str
        String in which to find `pattern`

    Returns
    -------
    match : bool
    """
    if string is not None:
        reg = re.compile(pattern)
        return reg.search(string) is not None
    else:
        return False


class Kengdic(object):
    """kengdic Korean/English Dictionary

    kengdic is a large Korean/English dictionary database created by Joe
    Speigle. It was originally hosted at ezkorean.com, and was made
    available by Garfield Nate (<https://github.com/garfieldnate/kengdic>)
    because it was no longer available anywhere else. This implementation
    provides serverless access via a convenient SQLite API. The dictionary is
    released under MPL 2.0.

    Details
    -------

    From Garfield Nate (<https://github.com/garfieldnate>):
    "I found a note from Joe Speigle at http://www.perapera.org/korean/
    last year (2013):

        the lowdown is that my dictionary has about 90,000 words in it of
        which 70,000 have been human-verified by me, and has about 20,000
        hanja which are linked to the correct definition though the word is
        the same (and the hanja are different). This is more than either
        English wiktionary (which has K as a definition) or the K-K
        wiktionary. I have never found a more complete dictionary online or
        anywhere for korean-English that is opensource as mine. That is why
        I made it, people. I'm not into reduplicating the wheel as they
        say. I have spent thousands of hours on this project. was it worth
        it? ... Anybody can contact me about this, I am extremely willing
        to     share all knowledge I have about it. My email address is at
        the bottom of the page for ezcorean.com

    Unfortunately, it was my sad finding that Joe Speigle passed away last
    year. The Wayback machine indexed ezkorean.com, but did not index
    kengdic, his amazing dictionary. After quite a bit of searching, I
    found that Maran Emil Cristian had obtained and stored a copy. He was
    kind enough to copy it for me, and so now I am able to provide it here."
    """

    try:
        __sqlite_path = pkg_resources.resource_filename(
            "kengdic", os.path.join("sqlite", "kengdic_2011.sqlite"))
    except ModuleNotFoundError:
        __sqlite_path = os.path.join(os.path.dirname(__file__),
                                     "sqlite", "kengdic_2011.sqlite")

    @classmethod
    def load_sqlite(cls, mode='ro', **kwargs):
        """Load the kengdic database SQLite connection

        Use of this method is only advised if you are an experienced SQL user.

        Parameters
        ----------
        mode : {'ro', 'rw', 'rwc', 'memory'}, optional (default: 'ro')
            The mode query parameter determines if the new database is opened
            read-only, read-write, read-write and created if it does not exist,
            or that the database is a pure in-memory database that never
            interacts with disk, respectively.
        kwargs : keyword arguments
            Other keyword arguments to include in the uri. See
            <https://www.sqlite.org/uri.html> for details.

        Returns
        -------
        conn : sqlite3.Connection
            Connection to the kengdic database
        """
        assert mode in ['ro', 'rw', 'rwc', 'memory']
        uri = "file:{}?mode={}".format(cls.__sqlite_path, mode)
        for key, value in kwargs.items():
            uri = uri + "&{}={}".format(key, value)
        conn = sqlite3.connect(uri, uri=True)
        atexit.register(conn.close)
        return conn

    def __init__(self):
        self._last_search = None
        self._last_result = None

    @property
    def _conn(self):
        try:
            return self._sqlite_conn
        except AttributeError:
            self._sqlite_conn = self.load_sqlite()
            self._sqlite_conn.create_function("REGEXP", 2, _regexp)
            return self._sqlite_conn

    @property
    def _cursor(self):
        return self._conn.cursor()

    def _search(self, match_clause, **search_terms):
        """Search the dictionary for an exact match

        Parameters
        ----------
        match_clause : {'==', 'LIKE', 'REGEXP', 'GLOB'}
            Choose the kind of search to be performed
        search_terms : additional arguments
            Key-value pairs of fields to be searched

        Returns
        -------
        result : list
            List of `KengdicResult`s, one for each match
        """
        if self._last_search == (match_clause, search_terms):
            return self._last_result
        else:
            self._last_search = match_clause, search_terms
        where_clause = []
        for key, value in search_terms.items():
            where_clause.append("{} {} '{}'".format(key, match_clause, value))
        if where_clause != "":
            where_clause = " where " + " and ".join(where_clause)
        result = list(self._cursor.execute(
            'select * from kengdic' + where_clause))
        self._last_result = [KengdicResult(r) for r in result]
        return self._last_result

    def search(self, **search_terms):
        """Search the dictionary for an exact match

        Parameters
        ----------
        korean : str
            Korean word
        english : str
            English translation
        hanja : str or `None`
            Hanja, if available
        synonym : str or `None`
            Synonym: turned into a placeholder for a strange note about the word
        part_of_speech_number : int
            Number representing part of speech. Currently unused.
        part_of_speech : str
            Text describing part of speech. Currently unused.
        submitter : str
            Name of user who submitted the word
        date_of_entry : str
            Date the entry was submitted
        word_id : int
            Unique identifier for the entry
        word_id2 : int
            Purpose unclear
        word_size : int
            Size of the Korean word
        extra_data : str
            Additional information included in the dictionary entry

        Returns
        -------
        result : list
            List of `KengdicResult`s, one for each match
        """
        return self._search(match_clause="==", **search_terms)

    def search_like(self, **search_terms):
        """Search the dictionary for an partial match using SQL syntax

        There are two wildcards used in conjunction with the LIKE operator:

        * `%` - The percent sign represents zero, one, or multiple characters
        * `_` - The underscore represents a single character

        LIKE is not case sensitive.

        Parameters
        ----------
        korean : str
            Korean word
        english : str
            English translation
        hanja : str or `None`
            Hanja, if available
        synonym : str or `None`
            Synonym: turned into a placeholder for a strange note about the word
        part_of_speech_number : int
            Number representing part of speech. Currently unused.
        part_of_speech : str
            Text describing part of speech. Currently unused.
        submitter : str
            Name of user who submitted the word
        date_of_entry : str
            Date the entry was submitted
        word_id : int
            Unique identifier for the entry
        word_id2 : int
            Purpose unclear
        word_size : int
            Size of the Korean word
        extra_data : str
            Additional information included in the dictionary entry

        Returns
        -------
        result : list
            List of `KengdicResult`s, one for each match
        """
        return self._search(match_clause="LIKE", **search_terms)

    def search_regex(self, **search_terms):
        """Search the dictionary for a regular expression match

        You can read about Python regular expressions at
        <https://docs.python.org/3/library/re.html#regular-expression-syntax>

        Parameters
        ----------
        korean : str
            Korean word
        english : str
            English translation
        hanja : str or `None`
            Hanja, if available
        synonym : str or `None`
            Synonym: turned into a placeholder for a strange note about the word
        part_of_speech_number : int
            Number representing part of speech. Currently unused.
        part_of_speech : str
            Text describing part of speech. Currently unused.
        submitter : str
            Name of user who submitted the word
        date_of_entry : str
            Date the entry was submitted
        word_id : int
            Unique identifier for the entry
        word_id2 : int
            Purpose unclear
        word_size : int
            Size of the Korean word
        extra_data : str
            Additional information included in the dictionary entry

        Returns
        -------
        result : list
            List of `KengdicResult`s, one for each match
        """
        return self._search(match_clause="REGEXP", **search_terms)

    def search_glob(self, **search_terms):
        """Search the dictionary for a partial match using Unix syntax

        There are three wildcards used in conjunction with the GLOB operator:

        * A '?' (not between brackets) matches any single character.
        * A '*' (not between brackets) matches any string, including the empty string.
        * Brackets '[' match ranges or character classes: see <http://man7.org/linux/man-pages/man7/glob.7.html>


        Parameters
        ----------
        korean : str
            Korean word
        english : str
            English translation
        hanja : str or `None`
            Hanja, if available
        synonym : str or `None`
            Synonym: turned into a placeholder for a strange note about the word
        part_of_speech_number : int
            Number representing part of speech. Currently unused.
        part_of_speech : str
            Text describing part of speech. Currently unused.
        submitter : str
            Name of user who submitted the word
        date_of_entry : str
            Date the entry was submitted
        word_id : int
            Unique identifier for the entry
        word_id2 : int
            Purpose unclear
        word_size : int
            Size of the Korean word
        extra_data : str
            Additional information included in the dictionary entry

        Returns
        -------
        result : list
            List of `KengdicResult`s, one for each match
        """
        return self._search(match_clause="GLOB", **search_terms)


class KengdicResult(dict):
    """Korean-English Dictionary Entry

    This class inherits from a regular python dictionary and can be treated as
    such, but also comes with additional properties for each access to defined
    dictionary fields. Changes here are not committed to the database.

    Properties
    ----------
    korean : str
        Korean word
    english : str
        English translation
    hanja : str or `None`
        Hanja, if available
    synonym : str or `None`
        Synonym: turned into a placeholder for a strange note about the word
    part_of_speech_number : int
        Number representing part of speech. Currently unused.
    part_of_speech : str
        Text describing part of speech. Currently unused.
    submitter : str
        Name of user who submitted the word
    date_of_entry : str
        Date the entry was submitted
    word_id : int
        Unique identifier for the entry
    word_id2 : int
        Purpose unclear
    word_size : int
        Size of the Korean word
    extra_data : str
        Additional information included in the dictionary entry
    """

    __fields = ['word_id', 'korean', 'synonym', 'english',
                'part_of_speech_number', 'part_of_speech',
                'submitter', 'date_of_entry', 'word_size',
                'hanja', 'word_id2', 'extra_data']

    def __init__(self, query_result):
        assert len(query_result) == len(self.__fields)
        for i in range(len(self.__fields)):
            self[self.__fields[i]] = query_result[i]

    @property
    def english(self):
        return self['english']

    @property
    def korean(self):
        return self['korean']

    @property
    def hanja(self):
        return self['hanja']

    @property
    def synonym(self):
        return self['synonym']

    @property
    def part_of_speech_number(self):
        return self['part_of_speech_number']

    @property
    def part_of_speech(self):
        return self['part_of_speech']

    @property
    def submitter(self):
        return self['submitter']

    @property
    def date_of_entry(self):
        return self['date_of_entry']

    @property
    def word_size(self):
        return self['word_size']

    @property
    def extra_data(self):
        return self['extra_data']

    @property
    def word_id(self):
        return self['word_id']

    @property
    def word_id2(self):
        return self['word_id2']

    def __str__(self):
        return "\n".join([
            "Korean: {}".format(self.korean),
            "English: {}".format(self.english)
        ] + ([
            "Hanja: {}".format(self.hanja),
        ] if self.hanja else []) + [
            "Synonym: {}".format(self.synonym),
            "Part of Speech: {} ({})".format(self.part_of_speech_number,
                                             self.part_of_speech),
            "Submitted: {} ({})".format(self.submitter, self.date_of_entry)
        ])

    def __repr__(self):
        return "{}:\n{}".format(type(self), dict(self))
