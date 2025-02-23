import pytest
from anki_card_object import Anki_Card
from anki_acm import update_tags, generate_tags
from test_cards_fixture import cards_variations


def test_percentage(cards_variations: list[Anki_Card]) -> None:
    """Tests that the `__post_init__` method `compute_percentaje` works as intended

    :param cards_variations: Pyests fixture of a list containing Anki_Card objects
    """
    percentages = [0.32, 0.64, 0.74, 0.84, 0.92, 1.0, 0.58, 0.64, 1.0]
    for i, card in enumerate(cards_variations):
        assert card.percentage == pytest.approx(percentages[i], rel=1e-2)


def test_update_tag(cards_variations: list[Anki_Card]) -> None:
    """Tests that the tags are updated or added correctly

    :param cards_variations: Pyests fixture of a list containing Anki_Card objects
    """
    expected_tags: list = [
        "AnkiACM::<60%",
        "AnkiACM::60%-70%",
        "AnkiACM::70%-80%",
        "AnkiACM::80%-90%",
        "AnkiACM::90%-100%",
        "AnkiACM::100%",
        "AnkiACM::<60%",
        "AnkiACM::60%-70%",
        "AnkiACM::100%",
    ]
    update_tags(generate_tags(), cards_variations)
    for i, card in enumerate(cards_variations):
        assert expected_tags[i] in card.tags


def test_generate_tags() -> None:
    """Tests generate_tags function with a wide range of inputs"""
    tags_expected: list = [
        [
            "AnkiACM::<60%",
            "AnkiACM::60%-70%",
            "AnkiACM::70%-80%",
            "AnkiACM::80%-90%",
            "AnkiACM::90%-100%",
            "AnkiACM::100%",
        ],
        [
            "AnkiACM::<20%",
            "AnkiACM::20%-40%",
            "AnkiACM::40%-60%",
            "AnkiACM::60%-80%",
            "AnkiACM::80%-100%",
            "AnkiACM::100%",
        ],
        [
            "AnkiACM::<20%",
            "AnkiACM::20%-30%",
            "AnkiACM::30%-40%",
            "AnkiACM::40%-50%",
            "AnkiACM::50%-60%",
            "AnkiACM::60%-70%",
            "AnkiACM::70%-80%",
            "AnkiACM::80%-90%",
            "AnkiACM::90%-100%",
            "AnkiACM::100%",
        ],
        [
            "AnkiACM::<75%",
            "AnkiACM::75%-80%",
            "AnkiACM::80%-85%",
            "AnkiACM::85%-90%",
            "AnkiACM::90%-95%",
            "AnkiACM::95%-100%",
            "AnkiACM::100%",
        ],
        [
            "test::<95%",
            "test::95%-96%",
            "test::96%-97%",
            "test::97%-98%",
            "test::98%-99%",
            "test::100%",
        ],
    ]
    tags_params: list = [
        [],
        ["AnkiACM", 20, 20],
        ["AnkiACM", 20, 10],
        ["AnkiACM", 75, 5],
        ["test", 95, 1],
    ]
    for i in range(len(tags_params)):
        assert tags_expected[i] == generate_tags(*tags_params[i])


def test_format_update_tags(cards_variations: Anki_Card) -> None:
    """Tests `format_update_tags` method"""
    update_tags(generate_tags(), [cards_variations[0], cards_variations[7]])
    card_1: Anki_Card = cards_variations[0]
    card_2: Anki_Card = cards_variations[7]
    out_format_1: dict = {
        "note": 32,
        "tags": [
            "AnkiACM::<60%",
        ],
    }
    out_format_2: dict = {
        "note": 164,
        "tags": [
            "AnkiACM::60%-70%",
        ],
    }
    assert card_1.format_update_tags() == out_format_1
    assert card_2.format_update_tags() == out_format_2
