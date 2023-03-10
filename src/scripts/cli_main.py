from ..utilities.configurations import load_config
from .main import run


def run_exe() -> None:
    config = load_config()
    cli_round = input("Enter the match round: ")
    match_round = get_match_round(cli_round)
    run(config, int(match_round))


def get_match_round(cli_round: str) -> int:
    try:
        match_round = int(cli_round)
        if match_round not in range(1, 7):
            raise InvalidRound("Not a valid round")
        return match_round
    except InvalidRound:
        print("Defaulting to round 1 since a valid round was not provided")
        return 1


class InvalidRound(Exception):
    pass


if __name__ == "__main__":
    run_exe()
