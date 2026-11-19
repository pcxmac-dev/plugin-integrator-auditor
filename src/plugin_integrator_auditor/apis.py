"""What the auditor attaches to (plugin API 2.2, liminal_libs.apis; the user, 2026-11-11: "each plugin should reflect
the the API its attached to, and present links that provide documentation ... it should also expose more of what the
API is about"). Nothing outside this machine: the auditors ask no server anything. They use two things Liminal does
not make.

SQLite: the copy audit's comparison runs inside it. A cache file's rows are put into a temporary table of the feed's
own connection and held against `bars` with IS, the comparison the write itself uses, so both sides are in the stored
form. Python's standard library: the cache's files are gzip, each with a SHA-256 of what it holds, and a rows file is
one JSON document whose numbers Python writes and reads back as the same numbers.

Every address is one of SQLite's own pages (sqlite.org) or Python's (docs.python.org), each read on 2026-11-18
(`VERIFIED`). What a page was found to say is what the card says of it; where a page does not say something, the card
does not put it in its mouth (CREATE TABLE's page says a TEMP table is made in the temp database, no more)."""
from __future__ import annotations

from liminal_libs.apis import Api, Area, Call, Link

VERIFIED = "2026-11-18"
SQLITE_SITE = "https://www.sqlite.org/"
EXPRESSIONS = SQLITE_SITE + "lang_expr.html"
DATATYPES = SQLITE_SITE + "datatype3.html"
CREATE_TABLE = SQLITE_SITE + "lang_createtable.html"
WITHOUT_ROWID = SQLITE_SITE + "withoutrowid.html"
PYTHON = "https://docs.python.org/3/"
HASHLIB = PYTHON + "library/hashlib.html"
GZIP = PYTHON + "library/gzip.html"
JSON = PYTHON + "library/json.html"
FLOATS = PYTHON + "tutorial/floatingpoint.html"

SQLITE = Api(
    name="SQLite",
    maker="The SQLite project (sqlite.org)",
    about=("The copy audit compares inside SQLite. A cache file's rows go into a temporary table on the feed's own "
           "connection and are held against the feed's bars with IS: every key, every value, in the stored form. "
           "Nothing is sent anywhere."),
    kind="sdk",
    base="a feed's own file in the data folder (feeds/<feed>.db), through the connection the app already holds",
    version="SQLite 3, as this Python carries it",
    auth="none of its own: the file's rights on its system",
    limits="one writer at a time on a file; the comparison reads, and writes only its own temporary table",
    costs="",
    links=(
        Link("SQL Language Expressions", EXPRESSIONS, "docs"),
        Link("Datatypes In SQLite", DATATYPES, "reference"),
        Link("CREATE TABLE", CREATE_TABLE, "reference"),
        Link("Clustered Indexes and the WITHOUT ROWID Optimization", WITHOUT_ROWID, "guide"),
    ),
    areas=(
        Area("The IS and IS NOT operators", "Like = and != for values; with a NULL on either side they still answer "
             "true or false: two NULLs are the same, a NULL and a value are not.", EXPRESSIONS,
             "the comparison of each value of a cached row with the stored one, as the write's own rule has it"),
        Area("Type affinity", "A column of REAL affinity keeps an integer as a floating point number; one of INTEGER "
             "affinity keeps a floating point number that is exactly an integer as an integer; an INTEGER and a REAL "
             "are compared as numbers.", DATATYPES,
             "the temporary table declares its columns as `bars` does, so a cached value is converted as the stored "
             "one was before the two are compared"),
        Area("Temporary tables", "A table made with TEMP is made in the temp database.", CREATE_TABLE,
             "`pull_rows`: a cache file's rows, on the feed's connection, emptied after each file"),
        Area("WITHOUT ROWID tables", "A table kept in the order of its primary key.", WITHOUT_ROWID,
             "`pull_rows` is keyed as `bars` is (ticker, timespan, multiplier, ts)"),
        Area("The rest of SQL", "The statements, functions and keywords of SQL as SQLite understands it.",
             SQLITE_SITE + "lang.html", ""),
    ),
    calls=(
        Call("a IS b / a IS NOT b", "Two values the same, a NULL counted as a value.", "The IS and IS NOT operators",
             "a cached bar's open, high, low, close, volume, vwap and transactions against the stored bar's", EXPRESSIONS),
        Call("CREATE TEMP TABLE pull_rows (...) WITHOUT ROWID", "A temporary table of bar rows.", "Temporary tables",
             "made once on a feed's connection, for the rows of the cache file being audited", CREATE_TABLE, writes=True),
        Call("INSERT OR REPLACE INTO temp.pull_rows", "Rows into the temporary table, a key's later row kept.",
             "Temporary tables", "a cache file's rows, in the order a write stored them", CREATE_TABLE, writes=True),
        Call("INSERT INTO bars ... SELECT ... FROM temp.pull_rows WHERE NOT EXISTS (...)", "Rows of one table into "
             "another, where they are not there.", "The rest of SQL",
             "a bar the cache holds and the database does not, put in from the cache (On a mismatch: repair)",
             SQLITE_SITE + "lang_insert.html", writes=True),
        Call("UPDATE, DELETE", "Rows changed or removed.", "The rest of SQL", "", SQLITE_SITE + "lang_update.html",
             writes=True),
    ),
    verified=VERIFIED,
)

PYTHON_LIBRARY = Api(
    name="Python standard library",
    maker="The Python Software Foundation (docs.python.org)",
    about=("The fetch cache's files: every file is gzip, has a SHA-256 of what it holds, and a rows file is one JSON "
           "document. An int is written as its digits and a float as the text Python reads back to the same float, "
           "so nothing is rounded between an answer and the database."),
    kind="sdk",
    base="the cache folder beside the main file (cache/<feed>/<pull>/)",
    version="Python 3.10 or newer (the pages read were 3.15's)",
    auth="none",
    limits="",
    costs="",
    links=(
        Link("hashlib: Secure hashes and message digests", HASHLIB, "reference"),
        Link("gzip: Support for gzip files", GZIP, "reference"),
        Link("json: JSON encoder and decoder", JSON, "reference"),
        Link("Floating-Point Arithmetic: Issues and Limitations", FLOATS, "guide"),
    ),
    areas=(
        Area("SHA-256", "A hash of a run of bytes, given as hexadecimal digits.", HASHLIB,
             "kept for each cache file when it is written (an answer's body as received, a rows file's text) and "
             "held against the file again when it is audited"),
        Area("gzip files", "A file packed as gzip; its header's time can be set to 0 so the same content packs to "
             "the same bytes.", GZIP, "every cache file, written under a part name and renamed once it is whole"),
        Area("JSON", "Numbers, text, true, false, null, lists and objects as text. NaN and the infinities are "
             "written by default, though the JSON standard has no such numbers; a value it cannot write is handed "
             "to a function of the caller's.", JSON,
             "a rows file: the exact values a write hands to the database, read back before the write is made"),
        Area("How a float is written", "Python writes a float as the shortest text that reads back to the same "
             "float (on most systems, since Python 3.1).", FLOATS,
             "why a bar's price in a rows file is the price the feed sent, bit for bit"),
        Area("The rest of the library", "Everything else Python ships.", PYTHON + "library/index.html", ""),
    ),
    calls=(
        Call("hashlib.sha256()", "A SHA-256 hash object: update() takes bytes, hexdigest() gives the digits.",
             "SHA-256", "each cache file's hash", HASHLIB),
        Call("gzip.GzipFile(filename, mode, compresslevel, fileobj, mtime)", "A gzip file to read or write.",
             "gzip files", "each cache file, compresslevel 1 and mtime 0", GZIP, writes=True),
        Call("json.dumps(obj, separators=, default=)", "An object as JSON text.", "JSON",
             "a rows file's text; a numpy number goes in as the number it is", JSON),
        Call("json.loads(text)", "JSON text as an object.", "JSON", "a rows file read back", JSON),
        Call("json.dump, json.load", "The same, to and from a file.", "JSON", "", JSON),
    ),
    verified=VERIFIED,
)

APIS = (SQLITE, PYTHON_LIBRARY)
