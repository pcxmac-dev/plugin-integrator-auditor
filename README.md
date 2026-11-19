# plugin-integrator-auditor

The auditor for [Liminal](https://github.com/pcxmac-dev/liminal-charts): the plugin that holds how what the
integrator fetches is audited.

## What it is

A Liminal plugin of the integrator's (plugin API 2.4, `liminal_libs.auditing`): the auditors' plugin, one an app. It
holds seven options and nothing else. It has no key, no database of its own, fetches nothing and sends nothing.

The auditors themselves are the library's, and they run whether or not this package is installed (then on their
defaults, so auditing is never off because a package is missing). What the plugin adds is that the options can be
chosen on its page in the Plugins view, and that the page shows what the auditors are doing: the fetch cache by
state and size, the last sweep, the findings, and two buttons, Audit now and Sweep now.

## What the auditors do

- **The fetch cache.** What a feed sends is written to disk before any of it reaches a database: each answer as it
  was received, and the exact rows each write hands over. The write is made from the rows file read back.
- **The copy audit.** When a pull closes, each of its rows files is compared with the feed's stored bars, every key
  and every value. A pull that passes has its files removed. A bar the cache holds and the database does not is put in
  from the cache. A bar stored with other values is a finding: nothing stored is overwritten, and the feed is asked
  for it again.
- **The sweep.** Every watched series of every feed in turn, a time budget a run. A session day with no bar inside a
  span the feed is said to hold is a hole only with evidence that bars should be there (the feed's own daily bar of
  that day, another feed of the same market, its ticks, a pull that was cut off). A hole is asked of the feed again;
  one the feed has nothing for is remembered as absent and not asked a third time.

What a passing copy audit proves is that the load from the cache into the database was exact. It does not prove the
feed's data right: the second-feed audit and the sweep look at that.

## Its options

| Option | Variable | Choices (default first) |
|---|---|---|
| Audit when a symbol is updated | `AUDITOR_ON_UPDATE` | on, off |
| Sweep every | `AUDITOR_SWEEP_EVERY` | 24h, 6h, 7d, off |
| Minutes per sweep run | `AUDITOR_SWEEP_MINUTES` | 10, 5, 30, 60 |
| On a mismatch | `AUDITOR_ON_MISMATCH` | repair, flag |
| Keep verified payloads (days) | `AUDITOR_KEEP_DAYS` | 0, 1, 7, 30 |
| Cache cap (GB) | `AUDITOR_CACHE_GB` | 20, 5, 50, 100 |
| Re-pulls per sweep | `AUDITOR_REPULLS` | 5, 0, 20 |

Each is a variable of yours, read through the app's login as every plugin's settings are: never a file of this
software's. A value that is none of an option's choices stops the app and names the choices.

At its cap the cache makes fetching wait for the auditors. Unverified data is never deleted.

## Installing

The app finds it through the entry point group `liminal.providers` and lists it as `package:
plugin-integrator-auditor`, with this package's version; a checkout in the workspace's `plugins/` folder is loaded
from there. It needs `liminal-libs` 1.64.0 or newer.

```
python -m pip install -e ".[dev]"
python -m pytest -q
```

The tests open nothing and send nothing; one of them reads the makers' documentation pages, and only with
`LIMINAL_VENDOR_PAGES=1`.
