import pytest
from anki_card_object import Anki_Card


@pytest.fixture
def cards_variations() -> list[Anki_Card]:
    """Generates a list of Anki_Card objects to unit test with pytest"""
    return [
        Anki_Card(
            32,
            2,
            ["AnkiACM::60%-70%"],
            [
                {"ease": 1, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            65,
            4,
            ["AnkiACM::70%-80%"],
            [
                {"ease": 3, "lastIvl": 0},
                {"ease": 1, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            74,
            6,
            ["AnkiACM::80%-90%"],
            [
                {"ease": 1, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            84,
            8,
            ["AnkiACM::90%-100%"],
            [
                {"ease": 3, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            91,
            8,
            ["AnkiACM::100%"],
            [
                {"ease": 2, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            100,
            8,
            ["AnkiACM::100%"],
            [
                {"ease": 3, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            1_57,
            15,
            [
                "AnkiACM::100%",
            ],
            [
                {"ease": 1, "lastIvl": 100},
                {"ease": 1, "lastIvl": 100},
                {"ease": 1, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            1_64,
            1,
            [],
            [
                {"ease": 1, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
                {"ease": 2, "lastIvl": 100},
            ],
        ),
        Anki_Card(
            1_100,
            8,
            [],
            [
                {"ease": 3, "lastIvl": 0},
                {"ease": 3, "lastIvl": 100},
                {"ease": 3, "lastIvl": 100},
            ],
        ),
    ]
