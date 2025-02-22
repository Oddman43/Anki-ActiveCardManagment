from dataclasses import dataclass


@dataclass
class Anki_Card:
    nid: int
    cid: int
    tags: list
    reviews: list[dict]
    percentage: float = 0.0

    def __post_init__(self) -> None:
        self.compute_percentaje()

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

    def format_update_tags(self) -> dict:
        return {
                "note": self.nid,
                "tags": self.tags,
            }
