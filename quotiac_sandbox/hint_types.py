class HintBase:
    def to_json(self) -> dict[str, str]:
        return self.__dict__ | dict(type=self.__class__.__name__)


class GiveALetterHint(HintBase):
    def __init__(self, letter: str) -> None:
        self.letter = letter
