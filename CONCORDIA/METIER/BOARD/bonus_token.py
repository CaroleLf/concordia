from ..good import Good


class BonusToken:
    bonus_sesters: int
    target_good: Good
    is_returned: bool = False

    def __init__(self, bonus_sesters: int, target_good: Good) -> None:
        self.bonus_sesters = bonus_sesters
        self.target_good = target_good

    def returned(self) -> None:
        """
        Allow to change the returned status of the bonus token
        """

        self.is_returned = not self.is_returned
