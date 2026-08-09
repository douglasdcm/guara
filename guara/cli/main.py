import argparse

from guara.cli.commands.replay import replay


def create_parser():
    parser = argparse.ArgumentParser(
        description="Guara CLI tool for managing and executing transactions."
    )

    # Create subparsers to handle commands like 'replay'
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Configure the 'replay' subcommand
    replay_parser = subparsers.add_parser(
        "replay", help="Replay transaction executions from a log file or identifier."
    )

    # Add typical arguments for a replay feature (adjust these flags to match your needs)
    replay_parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to the JSON transaction log file to replay.",
    )
    replay_parser.add_argument(
        "-i",
        "--id",
        type=str,
        help="Specific transaction identifier or execution hash to target.",
    )
    replay_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the replay execution without invoking actual drivers.",
    )
    replay_parser.add_argument(
        "-r",
        "--resume",
        # type=bool,
        action="store_true",
        help="Resume the replay execution from a specific transaction or execution ID.",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "replay":
        return replay(args)
