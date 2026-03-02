from pathlib import Path

from colorex.cli import build_parser, main


def test_cli_parser_render_command():
    parser = build_parser()
    args = parser.parse_args(["render", "input.csv", "--out", "output.html"])
    assert args.command == "render"
    assert args.input == "input.csv"
    assert args.out == "output.html"


def test_cli_render_html_success(tmp_path: Path):
    csv = tmp_path / "input.csv"
    csv.write_text("1,2\n3,4\n", encoding="utf-8")
    out = tmp_path / "output.html"

    code = main(["render", str(csv), "--out", str(out), "--normalize", "linear"])

    assert code == 0
    assert out.exists()


def test_cli_non_zero_on_failure(tmp_path: Path):
    out = tmp_path / "output.html"
    code = main(["render", "does-not-exist.csv", "--out", str(out)])
    assert code == 1