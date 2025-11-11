import argparse
from .install import add_install_parser
from .identify import add_identify_parser
from .analyze import add_analyze_parser
from .verify import add_verify_parser
from .ci import add_ci_check_parser

def main():
    """
    The main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="A tool for rebase analysis and intent verification."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Add sub-commands here
    add_install_parser(subparsers)
    add_identify_parser(subparsers)
    add_analyze_parser(subparsers)
    add_verify_parser(subparsers)
    add_ci_check_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
