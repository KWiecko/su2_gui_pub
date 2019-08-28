from pyforms.controls import ControlCheckBox, ControlBase
from pyvalid import accepts, returns


class ParamOnOffSwitch(ControlCheckBox):

    @property
    @returns(ControlBase)
    def toogled_param(self) -> ControlBase:
        return self._toogled_param

    @toogled_param.setter
    @accepts(object, ControlBase)
    def toogled_param(self, new_val: ControlBase):
        self._toogled_param = new_val

    def __init__(self, toogled_param: ControlBase):
        """
        Init with params

        Parameters
        ----------
        toogled_param: ControlBase
            toogled param control
        """
        super(ParamOnOffSwitch, self).__init__()
        self.toogled_param = toogled_param
        self.value = True
        self.changed_event = self._on_off_toogle

    def _on_off_toogle(self):
        """
        On-Off switch behaviour def
        Returns
        -------

        """
        # print(self.value)
        if self.value is True:
            self.toogled_param.enabled = True
        else:
            self.toogled_param.enabled = False
        # print(self.toogled_param.value)
