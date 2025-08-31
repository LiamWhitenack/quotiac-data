import random
from abc import ABC, abstractmethod
from typing import Any, Self

from codiac_sandbox.hint_types import GiveALetterHint, HintBase
from codiac_sandbox.utils.make_letter_map import get_new_letter_map

# from PySide6.QtCore import QDate


class CryptographBase(ABC):
    def __init__(
        self,
        string_to_encrypt: str,
        puzzle_type: str = "Undefined",
        hints: list[HintBase] | None = None,
        used: bool = False,
        **kwargs: str,
    ) -> None:
        if hints is None:
            hints = []
        self.string_to_encrypt = string_to_encrypt
        self.puzzle_type = puzzle_type
        self.encryption_map = get_new_letter_map(string_to_encrypt)
        letters = list(
            s for s in string_to_encrypt.lower() if s in "qwertyuiopasdfghjklzxcvbnm"
        )
        random.shuffle(letters)
        self.hints = hints + [GiveALetterHint(letter) for letter in letters]
        self.used = used
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(
        self, to_read_from_frontend: bool = False
    ) -> dict[str, list[Any] | str | dict[str, str]]:
        res: dict[str, Any]
        data = self.__dict__.copy()
        hints: list[dict[str, Any]] = []
        hint: HintBase
        seen_letters: set[str] = set()
        for hint in data["hints"]:
            if isinstance(hint, GiveALetterHint):
                if hint.letter not in seen_letters:
                    seen_letters.add(hint.letter)
                    hints.append(hint.to_json())
        data["hints"] = hints

        if to_read_from_frontend:
            res = {}
            for key in ["used"]:
                del data[key]
            for key in ["puzzle_type", "string_to_encrypt", "hints", "encryption_map"]:
                res[key] = data.pop(key)

            res["other_info"] = {
                k.replace("_", " ").title(): str(v)
                for k, v in data.items()
                if v is not None
            }
            res["string_to_encrypt"] = res["string_to_encrypt"].lower()
            res = {k: str(v) for k, v in res.items() if v is not None}
        else:
            res = data
            res = (
                dict(
                    type=self.__class__.__name__,
                    puzzle_type=self.puzzle_type,
                    string_to_encrypt=self.string_to_encrypt,
                    length=len(self.string_to_encrypt),
                )
                | res
            )
            res |= dict(
                hints=None,
                encryption_map=None,
            )

        return res

    @classmethod
    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create an instance from JSON data. Must be implemented by subclasses."""
        pass


class ListPuzzle(CryptographBase):
    def __init__(self, setup: str, elements: list[str], used: bool = False) -> None:
        super().__init__(" ".join(elements), "list", used=used)
        self.setup = setup

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            setup=data["setup"],
            elements=data["string_to_encrypt"].split(),
            used=data["used"],
        )


class TrivialFact(CryptographBase):
    def __init__(
        self,
        fact: str,
        used: bool = False,
    ):
        super().__init__(fact, f"Trivial Fact", used=used)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            fact=data["string_to_encrypt"],
            used=data["used"],
        )


class CharacterQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        source_type: str,
        character_name: str,
        source: str,
        date: str,
        used: bool = False,
    ):
        super().__init__(quote, f"{source_type} Quote", used=used)
        self.character_name = character_name
        self.source = source
        self.date = date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            source_type=data["puzzle_type"].split(" ")[0],
            character_name=data["character_name"],
            source=data["source"],
            date=data["date"],
            used=data["used"],
        )


class FamousDocumentQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        source: str,
        author: str,
        date: str,
        used: bool = False,
    ):
        super().__init__(quote, "Famous Document", used=used)
        self.source = source
        self.author = author
        self.date = date

    @classmethod
    def from_json(
        cls,
        data: dict[str, Any],
        used: bool = False,
    ) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            source=data["source"],
            author=data["author"],
            date=data["date"],
            used=data["used"],
        )


class DirectQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        author: str,
        date: str | None = None,
        used: bool = False,
    ) -> None:
        super().__init__(quote, "Direct Quote", used=used)
        self.author = author
        self.date = date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            author=data["author"],
            date=data.get("date"),
            used=data["used"],
        )


class GeneralPhrase(CryptographBase):
    def __init__(
        self,
        phrase: str,
        used: bool = False,
    ):
        super().__init__(phrase, "General Quote", used=used)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(phrase=data["string_to_encrypt"], used=data["used"])


class SongLyrics(CryptographBase):
    def __init__(
        self,
        lyrics: str,
        artist: str,
        title: str,
        date: str,
        used: bool = False,
    ) -> None:
        super().__init__(lyrics, "Song lyrics", used=used)
        self.artist = artist
        self.title = title
        self.date = date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            lyrics=data["string_to_encrypt"],
            artist=data["artist"],
            title=data["title"],
            date=data["date"],
            used=data["used"],
        )


class Riddle(CryptographBase):
    def __init__(
        self,
        question_answer: str,
        used: bool = False,
    ) -> None:
        super().__init__(question_answer, "Riddle", used=used)
        self.question_answer = question_answer

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question_answer=data["question_answer"],
            used=data["used"],
        )


class Pun(CryptographBase):
    def __init__(
        self,
        question_answer: str,
        used: bool = False,
    ) -> None:
        super().__init__(question_answer, "Pun", used=used)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question_answer=data["question_answer"],
            used=data["used"],
        )


class RiddleSolvedInReverse(CryptographBase):
    def __init__(
        self,
        question: str,
        answer: str,
        used: bool = False,
    ) -> None:
        super().__init__(question, "Reverse Riddle", used=used)
        self.answer = answer

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question=data["string_to_encrypt"], answer=data["answer"], used=data["used"]
        )


PuzzleClass = (
    ListPuzzle
    | CharacterQuote
    | FamousDocumentQuote
    | DirectQuote
    | GeneralPhrase
    | SongLyrics
    | Riddle
    | Pun
    | RiddleSolvedInReverse
)
