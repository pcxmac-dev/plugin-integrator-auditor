"""The auditor for Liminal: the plugin that holds how what is fetched is audited (the auditors' plugin, plugin API 2.4:
liminal_libs.auditing).

The user, 2026-11-15: "For the integrator, there needs to be a plugin called auditor and it will manage the
configuration of auditing data"; and 2026-11-18: "an auditor plugin, for auditing sources and maintaining the
integrity of the feeds; for the integrator".

It holds seven options and nothing else. The auditors themselves are the library's and run whether or not this
package is installed (then on their defaults): what it adds is that the options can be chosen, on its page in the
Plugins view, and that the page shows what the auditors are doing.

What the options are held to:

  - **Audit when a symbol is updated** (on, off): each pull of the fetch cache is audited as it closes, and a
    symbol's whole cache after its fetch. Off: pulls wait in the cache for the sweep.
  - **Sweep every** (24 h, 6 h, 7 days, off) and **Minutes per sweep run** (10, 5, 30, 60): the sweep goes over every
    watched series of every feed in turn, for so long a run, from where its last run stopped.
  - **On a mismatch** (repair from the cache, flag only): a bar the cache holds and the database does not is put in
    from the cache, or only said. A bar stored with other values is never overwritten either way: it is a finding,
    and the feed is asked for it again.
  - **Keep verified payloads** (0, 1, 7, 30 days): how long a pull's files stay once its audit passed.
  - **Cache cap** (20, 5, 50, 100 GB): unverified cache at the cap makes fetching wait for the auditors. Unverified
    data is never deleted.
  - **Re-pulls per sweep** (5, 0, 20): how many spans a feed's run asks it for again, of what the auditors found
    missing with evidence that it should be there.

Each is a variable of the user's, read through the app's login as every plugin's settings are (AUDITOR_ON_UPDATE,
AUDITOR_SWEEP_EVERY, AUDITOR_SWEEP_MINUTES, AUDITOR_ON_MISMATCH, AUDITOR_KEEP_DAYS, AUDITOR_CACHE_GB,
AUDITOR_REPULLS): never a file of this software's. A value that is none of an option's choices stops the app with
the choices named, as any setting's does."""
from __future__ import annotations

from typing import Mapping

from liminal_libs.auditing import ABOUT, CHOICES, AuditorPlugin, Policy

from .apis import APIS

__version__ = "0.1.0"


class Auditor(AuditorPlugin):
    """The auditor's options, as the contract has them (AuditorPlugin: `options`, `plan_choices`), and the Policy
    they make."""

    name = "auditor"
    title = "Auditor"
    about = ("How what is fetched is audited: each pull held against what was stored before its cache files go, and "
             "every symbol gone over in turn for days that should hold bars and do not")
    order = 900
    api = "2.4"
    version = __version__
    apis = APIS
    INTERNAL_NOTES = (
        "It answers one hook, settings: the Policy the auditors are held to, made of its seven options. It changes "
        "nothing and starts nothing.",
        "The auditors are the library's (liminal_libs.auditing) and run without this plugin too, on the defaults.",
    )

    def settings(self, variables: Mapping[str, str]) -> Policy:
        """The auditors' Policy as the user's variables have it: each option one of its choices, its default when
        it is not set."""
        return self.policy(variables)

    @staticmethod
    def labels() -> dict[str, str]:
        """Each option's words on a page, by its variable."""
        return dict(ABOUT)

    @staticmethod
    def choices() -> dict[str, tuple[str, ...]]:
        """Each option's choices, its default first."""
        return dict(CHOICES)


AUDITOR = Auditor()
