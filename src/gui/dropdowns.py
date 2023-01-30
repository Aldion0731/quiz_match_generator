import tkinter as tk
from abc import ABC, abstractmethod


class DropdownMenu(ABC):
    @abstractmethod
    def get_selected_value(self) -> int:
        pass


class RoundMenu(DropdownMenu):
    def __init__(self, frame: tk.Frame) -> None:
        self.frame = frame
        self.variable = tk.IntVar(self.frame)
        self.variable.set(1)
        self.menu = tk.OptionMenu(self.frame, self.variable, *list(range(1, 7)))  # type: ignore

    def configure(self, **kwargs: int | str) -> None:
        self.menu.config(kwargs)

    def get_selected_value(self) -> int:
        return self.variable.get()
