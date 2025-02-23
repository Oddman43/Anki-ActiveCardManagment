from anki_card_object import Anki_Card
from anki_connect import invoke


def get_card_info(
    deck_name: str,
    min_reviews: int = 3,
) -> list:
    """Retrieves information about Anki cards from a specified deck.

    This function uses the Anki Connect add-on API to fetch details about cards in a given deck. It filters cards based on a minimum number of reviews.

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
            info_review[str(dic["cardId"])],
        )
        cards.append(card)
    return cards


def generate_tags(
    tag_name: str = "AnkiACM", floor: int = 60, increments: int = 10
) -> list:
    """Generates a list of Anki tag names with percentage ranges.

    Uses correct syntax so Anki Connect and Anki can interpret the tags correctly.

    The tags are generated based on a floor percentage, increments, and a tag name with default values

    :param tag_name: The base name for the tags. Defaults to "AnkiACM".
    :param floor: The starting percentage for the ranges. Defaults to 60.
    :param increments: The increment between percentage ranges. Defaults to 10.
    :return: A list of tag names with percentage ranges.
    """
    percentages: list = [x for x in range(floor, 99, increments)]
    tag_list: list = [
        f"{tag_name}::<{floor}%",
    ]
    i: int = 0
    for i in range(len(percentages)):
        tag_list.append(f"{tag_name}::{percentages[i]}%-{percentages[i]+increments}%")
    tag_list.append(f"{tag_name}::100%")
    return tag_list


def update_tags(tags_list: list, cards: list[Anki_Card]) -> None:
    """Updates the tags of Anki cards based on their percentage.

    This function iterates through a list of Anki cards and updates their tags based
    on predefined percentage ranges.  It removes any existing tags that are in the
    `tags_list` and adds the appropriate tag from `tags_list` based on the card's
    `percentage` attribute.

    Important: If you change the tag name, floor, or increments used to generate
    `tags_list`, you may need to manually delete the old tags from your Anki cards.

    :param tags_list: A list of tag names corresponding to percentage ranges. This list should be ordered from lowest to highest percentage range.
    :param cards: A list of Anki card objects, each with a `percentage` attribute.
    """
    for card in cards:
        updated_tags = list(set(card.tags) - set(tags_list))
        ranges: list = [0.6, 0.7, 0.8, 0.9, 1.0, float("inf")]
        for i, upper_bound in enumerate(ranges):
            if card.percentage < upper_bound:
                card.tags = updated_tags + [tags_list[i]]
                break


def commit_update_tags(cards: list[Anki_Card]) -> None:
    """Updates the tags of Anki cards using Anki Connect.

    This function iterates through a list of Anki card objects and uses the
    `updateNoteTags` Anki Connect API to update the tags of each card.  It relies
    on the `format_update_tags` method of the `Anki_Card` object to prepare the
    data in the format required by the Anki Connect API.

    :param cards: A list of Anki card objects, each with a `format_update_tags` method that returns a dictionary suitable for the `updateNoteTags` Anki Connect API.
    """
    for card in cards:
        updated_tags: dict = card.format_update_tags()
        invoke("updateNoteTags", **updated_tags)


def main() -> None:
    # You can modify here the parameters of tags_list
    tags_parameters: list = [
        "AnkiACM",  # Tag name
        60,  # Floor
        10,  # Increments
    ]
    tags: list[str] = generate_tags(*tags_parameters)
    decks: list = [
        "Add deck name",
    ]
    for deck in decks:
        print(f"Getting card info for {deck}")
        cards: list[Anki_Card] = get_card_info(deck)
        print("Updating tags")
        update_tags(tags, cards)
        commit_update_tags(cards)


if __name__ == "__main__":
    main()
