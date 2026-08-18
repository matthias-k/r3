"""Shared pytest fixtures for the R3 test suite."""

import pytest


@pytest.fixture(autouse=True)
def _isolated_git_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    """Give every test a self-contained git identity, independent of the machine.

    Several tests create throwaway git repos and commit into them (via
    ``executor.execute``), which needs an author/committer identity -- supplied here
    via the ``GIT_AUTHOR_*``/``GIT_COMMITTER_*`` env vars, which already take
    precedence over any config-file identity. Nulling ``GIT_CONFIG_GLOBAL`` and
    ``GIT_CONFIG_SYSTEM`` does a separate, necessary job: it neutralizes machine-local
    settings unrelated to identity -- most notably ``commit.gpgsign`` (which makes
    ``git commit`` fail with a signing error regardless of the identity supplied), but
    also e.g. ``core.editor`` -- so a LOCAL run reproduces the bare-CI state and a
    green local run genuinely proves the CI fix.

    ``executor.execute(...)`` spawns subprocesses that inherit ``os.environ``, so
    ``monkeypatch.setenv`` is sufficient; no per-call plumbing is needed. This fixture
    is function-scoped because it uses the function-scoped ``monkeypatch`` fixture
    (which auto-reverts), so the env changes never leak between tests.
    """
    monkeypatch.setenv("GIT_AUTHOR_NAME", "R3 Test")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "R3 Test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "r3-test@example.com")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "r3-test@example.com")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", "/dev/null")
