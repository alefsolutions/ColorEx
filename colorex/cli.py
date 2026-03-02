"""Command line interface for ColorEx."""

from __future__ import annotations

import argparse
import sys

from .exceptions import ColorExError
from .heatmap import Heatmap
from .theme import Theme, available_themes, get_builtin_theme


def _parse_theme(value: str):
    # Custom theme: #112233,#ddeeff[,#f0f0f0]
    if "," in value:
        parts = [x.strip() for x in value.split(",")]
        if len(parts) not in (2, 3):
            raise argparse.ArgumentTypeError(
                "Custom theme must be 'primary,secondary[,neutral]'"
            )
        if len(parts) == 2:
            return Theme(primary=parts[0], secondary=parts[1])
        return Theme(primary=parts[0], secondary=parts[1], neutral=parts[2])
    try:
        return get_builtin_theme(value)
    except ValueError as exc:
        valid = ", ".join(available_themes())
        raise argparse.ArgumentTypeError(f"{exc}. Valid built-ins: {valid}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="colorex", description="Render heatmaps from CSV")
    sub = parser.add_subparsers(dest="command", required=True)

    render = sub.add_parser("render", help="Render a CSV into HTML or PNG")
    render.add_argument("input", help="Input CSV path")
    render.add_argument("--out", required=True, help="Output file (.html or .png)")
    render.add_argument("--theme", default="blue-red", type=_parse_theme, help="Theme name or custom 'primary,secondary[,neutral]'")
    render.add_argument("--normalize", default="linear", choices=["linear", "log", "quantile"], help="Normalization mode")
    render.add_argument("--show-values", action="store_true", help="Show numeric values in HTML tiles")
    render.add_argument("--title", default=None)
    render.add_argument("--subtitle", default=None)
    render.add_argument("--strict-missing", action="store_true", help="Fail when missing values are present")
    render.add_argument("--no-legend", action="store_true", help="Disable HTML legend")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "render":
        parser.error("Unknown command")

    try:
        hm = Heatmap(
            args.input,
            theme=args.theme,
            normalize=args.normalize,
            show_values=args.show_values,
            title=args.title,
            subtitle=args.subtitle,
            strict_missing=args.strict_missing,
        )
        output = args.out.lower()
        if output.endswith(".html"):
            hm.to_html(args.out, legend=not args.no_legend)
        elif output.endswith(".png"):
            hm.to_image(args.out)
        else:
            parser.error("--out must end with .html or .png")
        return 0
    except (ColorExError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())