"""The auditor's plugin: its settings are the auditors' Policy, each option one of the library's choices; a value
that is none of them stops the app with the choices named; and it does nothing else (no key, no database, no
fetching, no scan). Nothing is opened and nothing is sent."""
from __future__ import annotations

import inspect

import pytest

import plugin_integrator_auditor as module
from liminal_libs import auditing
from liminal_libs.config import ConfigError
from plugin_integrator_auditor import AUDITOR, Auditor


def test_its_settings_are_the_policy_the_options_make():
    assert AUDITOR.settings({}) == auditing.Policy()  # nothing set: the defaults
    made = AUDITOR.settings({"AUDITOR_ON_UPDATE": "off", "AUDITOR_SWEEP_EVERY": "6h", "AUDITOR_SWEEP_MINUTES": "30",
                             "AUDITOR_ON_MISMATCH": "flag", "AUDITOR_KEEP_DAYS": "7", "AUDITOR_CACHE_GB": "50",
                             "AUDITOR_REPULLS": "20", "MASSIVE_API_KEY": "not its business"})
    assert made == auditing.Policy(on_update=False, sweep_hours=6.0, sweep_minutes=30, repair=False, keep_days=7,
                                   cap_gb=50, repulls=20)
    assert AUDITOR.settings_of({"AUDITOR_SWEEP_EVERY": "off"}).sweep_hours is None


def test_a_value_that_is_none_of_the_choices_stops_the_app_with_the_choices_named():
    for name, choices in auditing.CHOICES.items():
        with pytest.raises(ConfigError, match=f"{name}='sometimes': one of {', '.join(choices)}"):
            AUDITOR.settings({name: "sometimes"})


def test_every_option_has_its_words_and_its_choices_with_the_default_first():
    assert AUDITOR.labels() == auditing.ABOUT and set(AUDITOR.labels()) == set(AUDITOR.options)
    assert AUDITOR.choices() == auditing.CHOICES
    assert [choices[0] for choices in AUDITOR.choices().values()] == ["on", "24h", "10", "repair", "0", "20", "5"]
    assert all(name.startswith("AUDITOR_") for name in AUDITOR.options)
    doc = inspect.getdoc(module)
    for name in AUDITOR.options:  # the package's own words name every variable
        assert name in doc, name


def test_it_holds_options_and_does_nothing_else():
    assert (AUDITOR.name, AUDITOR.title, AUDITOR.version, AUDITOR.api) == ("auditor", "Auditor", "0.1.0", "2.4")
    assert isinstance(AUDITOR, Auditor) and AUDITOR.about and len(AUDITOR.about) < 240
    own = {name for name, value in vars(Auditor).items() if callable(value) or isinstance(value, staticmethod)}
    assert own == {"settings", "labels", "choices"}  # one hook, and its words for a page
    assert AUDITOR.api_facts() == {} and all(len(line) <= 400 for line in AUDITOR.INTERNAL_NOTES)
    src = inspect.getsource(module)
    for reach in ("import requests", "import socket", "import subprocess", "open(", "sqlite3"):
        assert reach not in src, reach  # it opens nothing and sends nothing: the auditors are the library's
