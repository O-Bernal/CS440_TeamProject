import importlib, zipfile, textwrap
from pathlib import Path

def test_full_conversion(tmp_path, monkeypatch):
    # ── Arrange ────────────────────────────────
    (tmp_path / "inputs").mkdir()
    (tmp_path / "outputs").mkdir()
    raw = textwrap.dedent("""\
        Demo Book
        =Weather
        sunny
        rainy
        windy
        foggy
    """)
    (tmp_path / "inputs" / "weather.txt").write_text(raw, encoding="utf8")

    monkeypatch.chdir(tmp_path)     # hydra_convert now sees our sandbox

    # ── Act ────────────────────────────────────
    import hydra_convert
    importlib.reload(hydra_convert) # force fresh run

    # ── Assert ────────────────────────────────
    out = list((tmp_path / "outputs").glob("*.hllib"))
    assert len(out) == 1, "No .hllib written"

    with zipfile.ZipFile(out[0]) as z:
        files = set(z.namelist())
        assert "meta.hlmeta" in files
        assert "Demo_Book_none_1.2_.xml" in files
