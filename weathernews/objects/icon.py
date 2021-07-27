from weathernews.data import icon_details
from weathernews.error import IconNotFoundError


class Icon:
    def __init__(self, filename: str) -> None:
        if filename not in icon_details.keys():
            raise IconNotFoundError(f"Filename \'{filename}\' not found.")

        self.short = icon_details[filename]["short"]
        self.long = icon_details[filename]["long"]
