from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET_FILES = [
    "main.py",
    "claude_tool_mcp/server.py",
    "deeprecurse/query.py",
    "rlm/main.py",
    "rlm/modal_runtime.py",
    "rlm/rlm/repl.py",
]
DEPRECATED_MODELS = ("gpt-5-mini", "gpt-5-nano")
EXPECTED_REPLACEMENTS = {
    "main.py": "gpt-5.1-codex-mini",
    "claude_tool_mcp/server.py": "gpt-5.1-codex-mini",
    "deeprecurse/query.py": "gpt-5.1-codex-mini",
    "rlm/modal_runtime.py": "gpt-5.1-codex-mini",
    "rlm/main.py": "gpt-5-codex-mini",
    "rlm/rlm/repl.py": "gpt-5-codex-mini",
}


def _read_file(rel_path: str) -> str:
    file_path = REPO_ROOT / rel_path
    assert file_path.exists(), f"Missing file: {file_path}"
    return file_path.read_text(encoding="utf-8")


def test_no_deprecated_model_defaults_present() -> None:
    for rel_path in TARGET_FILES:
        content = _read_file(rel_path)
        for deprecated in DEPRECATED_MODELS:
            assert deprecated not in content, (
                f"Deprecated model '{deprecated}' still present in {rel_path}"
            )


def test_expected_replacements_present() -> None:
    for rel_path, expected in EXPECTED_REPLACEMENTS.items():
        content = _read_file(rel_path)
        assert expected in content, (
            f"Expected model '{expected}' not found in {rel_path}"
        )


def test_readme_has_no_deprecated_model_names() -> None:
    content = _read_file("README.md")
    assert "gpt-5-nano" not in content
    assert "gpt-5-mini" not in content
