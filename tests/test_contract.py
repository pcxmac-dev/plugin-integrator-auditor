"""The plugin here conforms to the class contract (plugin API 2.4): liminal_libs.sources.conformance, read from the
plugin alone (nothing opened, nothing sent)."""
from __future__ import annotations

import plugin_integrator_auditor as module
from liminal_libs import auditing
from liminal_libs.auditing import AuditorPlugin
from liminal_libs.sources.conformance import assert_module_conforms
from liminal_libs.sources.registry import _plugins_in
from liminal_libs.ui import STATIC


def test_the_plugin_here_conforms_to_the_class_contract():
    found = assert_module_conforms(module)
    assert [p.name for p in found] == ["auditor"] and all(p.api == "2.4" and not p.is_record for p in found)
    (p,) = found
    assert isinstance(p, AuditorPlugin) and (p.SYSTEM, p.KIND) == ("integrator", "auditor")
    assert p.options == tuple(auditing.CHOICES) and dict(p.plan_choices) == auditing.CHOICES
    assert p.keys == () and p.plan_vars == () and p.databases == () and p.fetcher is None  # it holds options, no more
    assert p.apis and p.interface()["apis"] == [a.name for a in p.apis]  # what it attaches to (2.2)
    assert set(p.interface()["hooks"]) == {"settings"} and p.has_settings and not p.has_scan
    assert f"    {p.ICON}: '" in (STATIC / "icons.js").read_text(encoding="utf-8")
    assert module.__version__ == "0.1.0" == p.version and [q.name for q in _plugins_in(module, "test")] == ["auditor"]
