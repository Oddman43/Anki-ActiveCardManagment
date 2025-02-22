from anki_card_object import Anki_Card
from anki_connect import invoke


def get_card_info(deck_name: str, min_reviews: int = 3, ) -> list:
    """"Retrieves information about Anki cards from a specified deck.

    This function uses the Anki Connect add-on API to fetch details about cards
    in a given deck. It filters cards based on a minimum number of reviews.

    :param deck_name: The name of the Anki deck. Spaces in the name should be escaped (e.g., "My Deck" becomes "My%20Deck")
    :param min_reviews: The minimum number of reviews a card must have to be included in the results. Defaults to 3.    
    :return: A list of Anki_Card objects containing information about the retrived cards
    """
    info_review: dict = {
        k: v
        for k, v in invoke(
            "getReviewsOfCards", cards=(invoke("findCards", query=f"deck:{deck_name}"))
        ).items()
        if len(v) >= min_reviews
    }
    cards_info: list[dict] = invoke(
        "cardsInfo", cards=[int(cid) for cid, _ in info_review.items()]
    )
    cards = []
    for dic in cards_info:
        card = Anki_Card(
            dic["note"],
            dic["cardId"],
            invoke("getNoteTags", note=dic["note"]),
            info_review[str(dic["cardId"])]
        )
        cards.append(card)
    return cards


def update_tags(tags_list: list, cards: list[Anki_Card]) -> None:
    for card in cards:
        updated_tags = list(set(card.tags) - set(tags_list))
        ranges: list = [0.6, 0.7, 0.8, 0.9, 1.0, float("inf")]
        for i, upper_bound in enumerate(ranges):
            if card.percentage < upper_bound:
                card.tags = updated_tags + [tags_list[i]]
                break



def main() -> None:
    tags: list[str] = [
        "AnkiACM::<60%",
        "AnkiACM::60%-70%",
        "AnkiACM::70%-80%",
        "AnkiACM::80%-90%",
        "AnkiACM::90%-99%",
        "AnkiACM::100%",
    ]
    decks: list = ["",]
    for deck in decks:
        print(f"Getting card info for {deck}")
        cards: list[Anki_Card] = get_card_info(deck)
        print("Updating tags")
        update_tags(tags, cards)


if __name__ == "__main__":
    main()