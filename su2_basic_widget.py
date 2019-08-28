from pyforms.basewidget import BaseWidget


class SU2BasicWidget(BaseWidget):
    def __init__(
            self, label='', initial_max_width=None, initial_max_height=None,
            initial_min_width=None, initial_min_height=None):
        super(SU2BasicWidget, self).__init__(label)
        self._max_width = initial_max_width
        self._max_height = initial_max_height

        self._min_width = initial_min_width
        self._min_height = initial_min_height

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, new_val):
        self._max_height = new_val

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, new_val):
        self._max_width = new_val

    @property
    def min_height(self):
        return self._min_height

    @min_height.setter
    def min_height(self, new_val):
        self._min_height = new_val

    @property
    def min_width(self):
        return self._min_width

    @min_width.setter
    def min_width(self, new_val):
        self._min_width = new_val
