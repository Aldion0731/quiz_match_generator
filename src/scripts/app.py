import tkinter as tk

from PIL import Image, ImageTk

from ..gui.dropdowns import RoundMenu
from ..gui.gui_utils import create_frames, create_window, generate_match
from ..utilities.addresses import Verifier
from ..utilities.configurations import load_config


def run() -> None:
    config = load_config()
    window = create_window(config)
    frames = create_frames(window)

    label_header = tk.Label(
        frames.header,
        text="Quiz Match Generator",
        font=("Helvetica 40 bold"),
        fg="green",
        pady=50,
    )
    label_header.grid(row=0, column=0)

    img = ImageTk.PhotoImage(Image.open(config.school_info.logo).resize((250, 250)))
    label_header_img = tk.Label(frames.header, image=img)
    label_header_img.grid(row=1, column=0)

    label_user_input_round = tk.Label(
        frames.user_input_round,
        text="Select the match round:",
        font=("Helvetica 18 bold"),
    )
    label_user_input_round.grid(row=1, column=0)

    round_menu = RoundMenu(frames.user_input_round)
    round_menu.configure(width=20, height=2, bg="#FFCA4B", font="Helvetica 18 bold")
    round_menu.menu.grid(row=2, column=0)

    button_generate = tk.Button(
        frames.generate_match,
        text="Generate Match",
        bg="#FFCA4B",
        height=2,
        width=50,
        borderwidth=3,
        relief="raised",
        font=("Helvetica 18 bold"),
        command=lambda: generate_match(round_menu.get_selected_value(), window),
    )
    button_generate.grid(row=0, column=0)

    frames.header.grid(row=0, column=1)
    frames.user_input_round.grid(row=1, column=1)
    verifier = Verifier()
    if not verifier.registered:
        message = tk.Message(
            window,
            text="Register with developer: Aldion Lee (lxdavid.lee@gmail.com)",
            font=("Helvetica 18 bold"),
            fg="red",
            width=1000,
        )
        message.grid(row=2, column=1)
    else:
        frames.generate_match.grid(row=2, column=1)

    window.mainloop()


if __name__ == "__main__":
    run()
