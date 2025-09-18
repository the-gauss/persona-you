import argparse


def cmd_ingest(args: argparse.Namespace) -> None:
    print(f"[ingest] person={args.person!r} source={args.source!r} (placeholder)")


def cmd_mem(args: argparse.Namespace) -> None:
    print(f"[mem] person={args.person!r} (placeholder)")


def cmd_chat(args: argparse.Namespace) -> None:
    print(f"[chat] person={args.person!r} (placeholder)")


def cmd_wipe(args: argparse.Namespace) -> None:
    print(f"[wipe] person={args.person!r} (placeholder)")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="persona-you", description="PersonaYou CLI (scaffold)")
    sub = p.add_subparsers(dest="command", required=True)

    p_ing = sub.add_parser("ingest", help="Parse raw exports into processed dataset")
    p_ing.add_argument("--person", required=True)
    p_ing.add_argument("--source", required=True)
    p_ing.set_defaults(func=cmd_ingest)

    p_mem = sub.add_parser("mem", help="Extract/update persona memories and index")
    p_mem.add_argument("--person", required=True)
    p_mem.set_defaults(func=cmd_mem)

    p_chat = sub.add_parser("chat", help="Chat locally with the persona")
    p_chat.add_argument("--person", required=True)
    p_chat.set_defaults(func=cmd_chat)

    p_wipe = sub.add_parser("wipe", help="Remove persona data/adapters")
    p_wipe.add_argument("--person", required=True)
    p_wipe.set_defaults(func=cmd_wipe)

    return p


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

