import pytest
from .anki_card_object import Anki_Card
from ..src.anki_acm import update_tags


def test_percentage(cards_variations: list[Anki_Card]) -> None:
    percentages = [0.42, 0.64, 0.74, 0.84, 0.92, 1.0, 1.0, 0.74, 1.0]
    for i, card in enumerate(cards_variations):
        assert card.percentage == pytest.approx(percentages[i], rel=1e-2)



def test_update_tag(cards_variations: list[Anki_Card]) -> None:
    tags: list[str] = [
        "OFICIALES::<60%",
        "OFICIALES::60%-70%",
        "OFICIALES::70%-80%",
        "OFICIALES::80%-90%",
        "OFICIALES::90%-99%",
        "OFICIALES::100%",
    ]
    expected_tags: list = [
        "OFICIALES::<60%",
        "OFICIALES::60%-70%",
        "OFICIALES::70%-80%",
        "OFICIALES::80%-90%",
        "OFICIALES::90%-99%",
        "OFICIALES::100%",
        "OFICIALES::100%",
        "OFICIALES::70%-80%",
        "OFICIALES::100%",
    ]
    update_tags(tags, cards_variations)
    for i, card in enumerate(cards_variations):
        assert expected_tags[i] in card.tags


def test_format_dict(cards_variations: Anki_Card) -> None:
    card_1: Anki_Card = cards_variations[0]
    card_2: Anki_Card = cards_variations[6]
    dict_format_1: dict = {
        "note": {
            "id": 42,
            "fields": {
                "Enunciado": "16. Pregunta 16<br><br><br>    1=> Opcion 1<br><br>    2=> Opcion 2<br><br>    3=> Opcion 3<br><br>    4=> Opcion 4",
                "RC": "1",
            },
            "tags": ["BIR::2021", "BIR::Fisiologia_Histologia", "OFICIALES::60%-70%"],
        }
    }
    dict_format_2: dict = {
        "note": {
            "id": 1001,
            "fields": {"Enunciado": "", "RC": ""},
            "tags": [
                "BIR::2021",
                "BIR::Fisiologia_Histologia",
                "OFICIALES::100%",
                "OFICIALES::MODED",
            ],
        }
    }
    assert card_1.format_dict() == dict_format_1
    assert card_2.format_dict() == dict_format_2

