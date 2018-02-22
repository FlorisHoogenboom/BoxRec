class Boxer(object):
    def __init__(
            self, id, name
    ):
        self.id = id
        self.name = name


class Fight(object):
    def __init__(
        self, event_id, fight_id,
        boxer_left_id, boxer_right_id,
        hist_rating_left, hist_rating_right,
        boxer_left=None, boxer_right=None,
        winner='left'
    ):
        self.event_id = event_id
        self.fight_id = fight_id
        self.boxer_left_id = boxer_left_id
        self.boxer_right_id = boxer_right_id
        self.boxer_right = boxer_right
        self.boxer_left = boxer_left
        self.hist_rating_left = hist_rating_left
        self.hist_rating_right = hist_rating_right
        self.winner = winner

    @property
    def boxer_left(self):
        if self._boxer_left is None:
            raise NameError('Boxer has not been set')
        return self._boxer_left

    @boxer_left.setter
    def boxer_left(self, val):
        self._boxer_left = val

    @property
    def boxer_right(self):
        if self._boxer_right is None:
            raise NameError('Boxer has not been set')
        return self._boxer_right

    @boxer_right.setter
    def boxer_right(self, val):
        self._boxer_right = val

    @property
    def winning_boxer(self):
        if self.winner == 'left':
            return self.boxer_left
        else:
            return self.boxer_right


