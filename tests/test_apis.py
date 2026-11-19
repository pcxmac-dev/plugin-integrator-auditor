"""What the auditor attaches to (plugin API 2.2): its cards are sound, every address one of SQLite's own pages or
Python's; they name what the auditors themselves run; and the cards' pages answer (LIMINAL_VENDOR_PAGES=1 only, the
one test that reaches the network)."""
from __future__ import annotations

import inspect
import os

import pytest

from liminal_libs import auditing, spool
from liminal_libs.apis import dead_links, problems, urls
from plugin_integrator_auditor import AUDITOR
from plugin_integrator_auditor import apis as cards


def test_the_cards_are_sound_and_link_the_makers_own_pages():
    assert problems(AUDITOR.apis) == [] and AUDITOR.apis == cards.APIS == (cards.SQLITE, cards.PYTHON_LIBRARY)
    for api in cards.APIS:
        assert (api.kind, api.verified, api.costs) == ("sdk", "2026-11-18", "") and api.docs
        assert {c.area for c in api.calls} <= {a.name for a in api.areas}
        assert len(api.areas) > len(api.covered) >= 4 and len(api.calls) > len(api.used) >= 4  # the rest is shown too
    assert all(u.startswith(("https://www.sqlite.org/", "https://docs.python.org/3/")) for u in urls(AUDITOR.apis))
    assert cards.SQLITE.docs == cards.EXPRESSIONS and {x.kind for x in cards.SQLITE.links} == {"docs", "reference", "guide"}


def test_the_cards_name_what_the_auditors_themselves_run():
    audit, files = inspect.getsource(auditing), inspect.getsource(spool)
    used = " ".join(c.name for api in cards.APIS for c in api.used)
    assert "CREATE TEMP TABLE IF NOT EXISTS pull_rows" in audit and "CREATE TEMP TABLE pull_rows" in used
    assert "INSERT OR REPLACE INTO temp.pull_rows" in audit and "INSERT OR REPLACE INTO temp.pull_rows" in used
    assert " IS t." in audit and " IS NOT t." in audit and "a IS b / a IS NOT b" in used
    assert "WITHOUT ROWID" in audit and "FROM temp.pull_rows" in audit and "INSERT INTO bars" in audit
    assert "hashlib.sha256(" in files and "hashlib.sha256()" in used
    assert "gzip.GzipFile(" in files and "mtime=0" in files and "compresslevel=LEVEL" in files and spool.LEVEL == 1
    assert "json.dumps(" in files and "json.loads(" in files and "default=_native" in files
    assert "json.dumps(obj, separators=, default=)" in used and "json.loads(text)" in used


def test_a_page_is_not_made_to_say_what_it_does_not():
    # CREATE TABLE's page says where a TEMP table is made, and no more: the card claims no more of it
    area = next(a for a in cards.SQLITE.areas if a.name == "Temporary tables")
    assert area.about == "A table made with TEMP is made in the temp database." and area.docs == cards.CREATE_TABLE
    floats = next(a for a in cards.PYTHON_LIBRARY.areas if a.name == "How a float is written")
    assert "on most systems" in floats.about and floats.docs == cards.FLOATS


@pytest.mark.skipif(os.environ.get("LIMINAL_VENDOR_PAGES") != "1", reason="reaches the makers' pages: LIMINAL_VENDOR_PAGES=1")
def test_the_cards_pages_answer():
    assert dead_links(AUDITOR.apis) == []
