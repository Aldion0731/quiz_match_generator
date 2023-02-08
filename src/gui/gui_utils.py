import tkinter as tk
from dataclasses import dataclass

from ..scripts.main import run as run_generator
from ..utilities.configurations import Config, load_config


@dataclass
class Frames:
    header: tk.Frame
    user_input_round: tk.Frame
    generate_match: tk.Frame


def create_frames(window: tk.Tk) -> Frames:
    return Frames(
        header=tk.Frame(window),
        user_input_round=tk.Frame(window),
        generate_match=tk.Frame(window),
    )


def create_window(config: Config) -> tk.Tk:
    window = tk.Tk()
    window.iconbitmap(config.school_info.icon)
    window.columnconfigure([0, 1, 2], weight=1, minsize=75)  # type: ignore
    window.rowconfigure([0, 1, 2], weight=1, minsize=75)  # type: ignore
    window.title(
        f"{config.school_info.name.value} - Quiz Match Generator (Aldion Lee \xa9 2023)"
    )
    return window


def generate_match(match_round: int, window: tk.Tk) -> None:
    config = load_config()
    run_generator(config, match_round)
    window.destroy()
