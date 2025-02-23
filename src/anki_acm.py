from anki_card_object import Anki_Card
from anki_connect import invoke


def get_card_info(deck_name: str, min_reviews: int = 3, ) -> list:
    """Retrieves information about Anki cards from a specified deck.

    This function uses the Anki Connect add-on API to fetch details about cards
    in a given deck. It filters cards based on a minimum number of reviews.

    :param deck_name: The name of the Anki deck. Spaces in the name should be escaped (e.g., "My Deck" becomes "My%20Deck")
    :param min_reviews: The minimum number of reviews a card must have to be included in the results. Defaults to 3.    
    :return: A list of Anki_Card objects containing information about the retrived cards in the specified deck
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


def generate_tags(increments: int = 10, tag_name: str = "AnkiACM", floor: int = 60) -> list:
    """Generates a list containing the name of tags

    Uses correct syntax so Anki connect and Anki can interpret correctly the tag

    :param increments: Defaults 10
    :param tag_name: Defaults AnkiACM
    :param floor: Defaults 60
    :return: List of tag names
    """
    percentages: list = [x for x in range(floor, 101, increments)]
    tag_list: list = [f"{tag_name}::<{floor}%",]
    i: int = 1
    for i in range(len(percentages)):
        tag_list.append(f"{tag_name}::{percentages[i-1]}-{percentages[i]}%")
    tag_list.append(f"{tag_name}::100%")
    return tag_list


def update_tags(tags_list: list, cards: list[Anki_Card]) -> None:
    """Computes the correct tag and updates the object

    :param tags_list:
    :param cards:
    """
    for card in cards:
        updated_tags = list(set(card.tags) - set(tags_list))
        ranges: list = [0.6, 0.7, 0.8, 0.9, 1.0, float("inf")]
        for i, upper_bound in enumerate(ranges):
            if card.percentage < upper_bound:
                card.tags = updated_tags + [tags_list[i]]
                break


def commit_update_tags(cards: list[Anki_Card]) -> None:
    """Updates the Anki tags using Anki Connect

    :param cards: A list of Anki_Card objects
    """
    for card in cards:
        updated_tags: dict = card.format_update_tags()
        invoke("updateNoteTags",**updated_tags)


def main() -> None:
    tags: list[str] = generate_tags(increments= 10, tag_name= "AnkiACM", floor = 60)
    decks: list = ["Change to deck name",]
    for deck in decks:
        print(f"Getting card info for {deck}")
        cards: list[Anki_Card] = get_card_info(deck)
        print("Updating tags")
        update_tags(tags, cards)
        commit_update_tags(cards)


if __name__ == "__main__":
    main()