"""Command-line interface for todo-expire."""
import argparse
import json
import sys

from scanner import scan


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="todo-expire", description="Find expired TODO/FIXME/HACK/XXX comments."
    )
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--ext", help="comma-separated extensions, e.g. py,js,ts")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--all", action="store_true", help="show all TODOs, not only expired")
    p.add_argument("--no-fail", action="store_true", help="always exit 0")
    args = p.parse_args(argv)

    exts = None
    if args.ext:
        exts = set()
        for x in args.ext.split(","):
            x = x.strip()
            if not x:
                continue
            if not x.startswith("."):
                x = "." + x
            exts.add(x.lower())

    items = scan(args.path, exts)
    if args.all:
        shown = items
    else:
        shown = [i for i in items if i.expired]

    if args.format == "json":
        print(json.dumps([i.__dict__ for i in shown], indent=2))
    else:
        if not shown:
            print("No TODOs found." if args.all else "No expired TODOs found.")
        for i in shown:
            tag = "EXPIRED" if i.expired else "ok"
            exp = i.expiry if i.expiry else "no-expiry"
            print(f"{i.path}:{i.line}: [{i.kind}] ({exp}) {i.text}  [{tag}]")

    if (not args.no_fail) and (not args.all) and shown:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
