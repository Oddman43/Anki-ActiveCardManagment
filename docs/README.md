# Anki Active Card Manager

## Description

This script automates the process of updating tags for Anki cards based on their review history. It leverages the Anki Connect add-on to interact with Anki and apply percentage-based tags to cards within specified decks.

## Table of Contents

*   [Features](#features)
*   [Requirements](#requirements)
*   [Installation](#installation)
*   [Script Details](#script-details)
*   [Usage](#usage)
    *   [Customizing Parameters](#customizing-parameters)
        *   [Choosing Decks to Tag](#choosing-decks-to-tag)
        *   [Customizing Tag Parameters](#customizing-tag-parameters)
        *   [Customizing `get_card_info` Parameters](#customizing-get_card_info-parameters)
    *   [Basic Usage](#basic-usage)
*   [License](#license)
*   [Author](#author)

## Features

*   Retrieves card information from the specified decks.
*   Filters cards based on a minimum review count.
*   Supports filtering for cards reviewed today.
*   Generates percentage-based tags.

## Requirements

*   Anki
*   [Anki Connect](https://ankiweb.net/shared/info/2055492159) Add-On
*   Python 3.12.7 or superior
*   `pip`
*   `anki_card_object.py` (Implementation of the `Anki_Card` class)
*   `anki_connect.py` (Implementation of the `invoke` function for Anki Connect)

## Installation

1.  Clone the repository:

    ```bash
    git clone [https://github.com/Oddman43/Anki-ActiveCardManagment](https://github.com/Oddman43/Anki-ActiveCardManagment)
    cd Anki-ActiveCardManagment
    ```

2.  Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

## Script Details

### `get_card_info(deck_name, min_reviews=3, only_today=True)`

Retrieves information about Anki cards from a specified deck.

This function uses the Anki Connect add-on API to fetch details about cards in a given deck. It filters cards based on a minimum number of reviews.

*   `deck_name`: The name of the Anki deck. Spaces in the name should be URL-encoded.
*   `min_reviews`: The minimum number of reviews a card must have to be included in the results. Defaults to 3.
*   `only_today`: If True, the results are limited to cards that have been reviewed today. If False, all cards meeting the `min_reviews` criteria are included. Defaults to True.
*   Returns: A list of `Anki_Card` objects containing information about the retrieved cards.

### `generate_tags(tag_name="AnkiACM", floor=60, increments=10)`

Generates a list of Anki tag names with percentage ranges.

Uses correct syntax so Anki Connect and Anki can interpret the tags correctly.

The tags are generated based on a floor percentage, increments, and a tag name with default values.

*   `tag_name`: The base name for the tags. Defaults to "AnkiACM".
*   `floor`: The starting percentage for the ranges. Defaults to 60.
*   `increments`: The increment between percentage ranges. Defaults to 10.
*   Returns: A list of tag names with percentage ranges.

### `update_tags(tags_list, cards)`

Updates the tags of Anki cards based on their percentage.

This function iterates through a list of Anki cards and updates their tags based on predefined percentage ranges. It removes any existing tags that are in the `tags_list` and adds the appropriate tag from `tags_list` based on the card's `percentage` attribute.

Important: If you change the tag name, floor, or increments used to generate `tags_list`, you may need to manually delete the old tags from your Anki cards.

*   `tags_list`: A list of tag names corresponding to percentage ranges. This list should be ordered from lowest to highest percentage range.
*   `cards`: A list of `Anki_Card` objects, each with a `percentage` attribute.

### `commit_update_tags(cards)`

Updates the tags of Anki cards using Anki Connect.

This function iterates through a list of Anki card objects and uses the `updateNoteTags` Anki Connect API to update the tags of each card. It relies on the `format_update_tags` method of the `Anki_Card` object to prepare the data in the format required by the Anki Connect API.

*   `cards`: A list of `Anki_Card` objects, each with a `format_update_tags` method that returns a dictionary suitable for the `updateNoteTags` Anki Connect API.

### `Anki_Card` Object

The `Anki_Card` object represents a single Anki card and stores its relevant information.

It is a dataclass, simplifying its creation and attribute access. It has the following attributes and methods:

*   **`nid` (int):** The note ID associated with the card.
*   **`cid` (int):** The card ID.
*   **`tags` (list):** A list of strings representing the card's tags.
*   **`reviews` (list\[dict]):** A list of dictionaries, where each dictionary contains information about a review of the card. These dictionaries are expected to have at least an `"ease"` key (an integer representing the ease factor of the review).
*   **`percentage` (float, optional):** A floating-point number representing a percentage value associated with the card (e.g., a learning progress percentage). This value is calculated automatically upon initialization. Defaults to 0.0.

#### Methods

*   **`__post_init__()`:** This method is called automatically after the `Anki_Card` object is created. It calls the `compute_percentage()` method to calculate the initial `percentage` value.
*   **`compute_percentage()`:** Calculates the `percentage` attribute based on the card's review history. It considers the last 10 reviews (or all reviews if there are fewer than 10). The calculation considers the `"ease"` values from the review dictionaries and correctly computes the percentage if any review has an ease of 0 (meaning the card was rescheduled).
*   **`format_update_tags()`:** Returns a dictionary formatted for the Anki Connect `updateNoteTags` API. This dictionary contains the `note` (using the `nid`) and `tags` that should be updated.

## Usage

### Customizing Parameters

#### Choosing Decks to Tag

**Important:** Deck names with spaces or special characters should be URL-encoded (e.g., "My Deck" becomes "My%20Deck"). A specific subdeck can be selected as `main_deck::sub_deck`.

**Command-line arguments (recommended):** The preferred way to specify decks is using command-line arguments:

```bash
python anki_acm.py "Deck Name 1" "Deck Name 2" "My Deck with Spaces" "Main Deck::Subdeck"
```

**Modifying the script (less recommended):** Alternatively, you can modify the decks list within the main function of the script. This is generally less flexible than command-line arguments.
```Python
decks: list = [
    "Manual_Deck_Name_1",
    "Manual_Deck_Name_2",
    "My Deck with Spaces" # Example with spaces, but better to use command line
]
```
To add more decks, simply append a comma followed by the deck name (string) to the list. However, using command-line arguments is highly encouraged for better flexibility.
#### Customizing tag parameters
The script uses default tag parameters. To change the default behavior, modify the `tags_parameters` list in the `main` function:

```python
tags_parameters: list = [ 
	"AnkiACM", # Tag name 
	60, # Floor percentage (starting percentage) 
	10, # Increment percentage 
	]
```

- **Tag name:** The base name of the tags.
- **Floor percentage:** The starting percentage for the tag ranges.
- **Increment percentage:** The increment between percentage ranges.
#### Customizing `get_card_info` parameters
The `get_card_info` function has configurable parameters. Modify the `deck_info` variable inside the `for deck in decks` loop in the `main` function. This allows you to customize each deck individually.

```python
for deck in decks:
    deck_info: list = [
        deck, 
        3,          # Minimum reviews
        True        # Consider only cards reviewed today
    ]
    cards: list[Anki_Card] = get_card_info(*deck_info) # Unpack the list as arguments
    # ... rest of the loop
```

- **Minimum reviews:** The minimum number of reviews a card must have to be included.
- **Consider only cards reviewed today:** If `True`, only cards reviewed today are included. It is recommended to set this to `False` for the initial run to tag all eligible cards, and then `True` for subsequent runs to only tag cards reviewed that day. Leaving it always `False` will be slower.
### Basic usage
Once you have setted your prefered values, open anki and run the script
## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE](..\LICENSE) file for details.
## Author
[Albert Sevilleja Torrents](https://www.linkedin.com/in/albertsevillejatorrents/) 
* GitHub: [Oddman43](https://github.com/Oddman43) 