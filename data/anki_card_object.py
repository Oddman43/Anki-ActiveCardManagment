from dataclasses import dataclass


@dataclass
class Anki_Card:
    nid: int
    cid: int
    tags: list
    front: str
    back: str
    reviews: list[dict]
    new_front: str = ""
    new_back: str = ""
    percentage: float = 0.0
    to_mod: bool = False
    new_moded: bool = False

    def __post_init__(self) -> None:
        self.compute_percentaje()
        self.flag_to_mod()

    def flag_to_mod(self) -> None:
        self.to_mod = "GOBIR" not in self.tags and self.percentage > 0.9

    def compute_percentaje(self):
        if len(self.reviews) < 2:
            self.percentage = 0.0
            return
        reviews_to_process: list[dict] = (
            self.reviews[-10:] if len(self.reviews) > 10 else self.reviews
        )
        subs_dict_0 = {1: 0.5, 2: 0.2, 3: 1.0, 4: 1.2, 0: 0}
        subs_dict = {1: 0, 2: 0.2, 3: 1.0, 4: 1.2, 0: 0}
        rescheduled = any(dic["ease"] == 0 for dic in reviews_to_process)
        if len(reviews_to_process) < 10:
            numerator = subs_dict_0[reviews_to_process[0]["ease"]]
            numerator += sum(subs_dict[dic["ease"]] for dic in reviews_to_process[1:])
        else:
            numerator = sum(
                subs_dict[dic["ease"]] for dic in reviews_to_process[-10:]
            )
        denominator = (
            len(reviews_to_process) - 1 if rescheduled else len(reviews_to_process)
        )
        self.percentage = numerator / denominator
        return

    def format_dict(self) -> dict:
        return {
            "note": {
                "id": self.nid,
                "fields": (
                    {"Enunciado": self.new_front, "RC": self.new_back}
                    if self.to_mod
                    else {"Enunciado": self.front, "RC": self.back}
                ),
                "tags": self.tags,
            }
        }

    def save_original(self) -> dict:
        return {
            "note_id": self.nid,
            "tags": list(set(self.tags) - {"OFICIALES::MODED"}),
            "front": self.front,
            "back": self.back,
        }

    def save_csv(self) -> list:
        return [self.nid, round(self.percentage, 2)]
