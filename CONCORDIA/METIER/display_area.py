from CONCORDIA.METIER.good import Good


class DisplayArea:
    display_area_any_good_required: bool
    display_area_n_goods: int
    display_area_position: int
    display_area_good: Good

    def __init__(self, p_display_area_any_good_required: bool, p_display_area_n_goods: int,
                 p_display_area_position: int, p_display_area_good: Good):
        self.display_area_any_good_required = p_display_area_any_good_required
        self.display_area_n_goods = p_display_area_n_goods
        self.display_area_position = int(p_display_area_position)
        self.display_area_good = p_display_area_good
