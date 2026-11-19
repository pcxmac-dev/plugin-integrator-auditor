# Changelog

## 0.1.0 (2026-11-18)

The first release: the auditors' plugin (plugin API 2.4, liminal-libs 1.64.0; the user, 2026-11-15: "For the
integrator, there needs to be a plugin called auditor and it will manage the configuration of auditing data", and
2026-11-18: "an auditor plugin, for auditing sources and maintaining the integrity of the feeds").

- Seven options, each with its choices and its default first: audit when a symbol is updated, the sweep's interval and
  its minutes a run, what is done on a mismatch, how long verified payloads are kept, the cache's cap, and the re-pulls
  a sweep.
- Its `settings` are the auditors' Policy. A value that is none of an option's choices stops the app with the choices
  named.
- It holds options and nothing else: no key, no database, no fetching, no scan. The auditors are the library's and
  run on their defaults without it.
- Its API cards: SQLite (the comparison runs inside it) and Python's standard library (the cache's files), every
  address one of sqlite.org's or docs.python.org's own pages, read on 2026-11-18.
