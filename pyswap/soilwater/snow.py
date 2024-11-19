from typing import Literal, Self

from pydantic import model_validator

from ..core import PySWAPBaseModel, SerializableMixin


class SnowAndFrost(PySWAPBaseModel, SerializableMixin):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of
            snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch, in case of frost reduce
            soil water flow
        snowinco (Optional[float]): Initial snow water equivalent
        teprrain (Optional[float]): Temperature above which all
            precipitation is rain
        teprsnow (Optional[float]): Temperature below which all
            precipitation is snow
        snowcoef (Optional[float]): Snowmelt calibration factor
        tfroststa (Optional[float]): Soil temperature (oC) where reduction
            of water fluxes starts
        tfrostend (Optional[float]): Soil temperature (oC) where reduction
            of water fluxes ends

    """

    swsnow: Literal[0, 1]
    swfrost: Literal[0, 1]
    snowinco: float | None = None
    teprrain: float | None = None
    teprsnow: float | None = None
    snowcoef: float | None = None
    tfrostst: float | None = None
    tfrostend: float | None = None

    @model_validator(mode="after")
    def _validate_snow_and_frost(self, v) -> Self:
        if self.swsnow == 1:
            assert self.snowinco is not None, "snowinco is required when swsnow is True"
            assert self.teprrain is not None, "teprrain is required when swsnow is True"
            assert self.teprsnow is not None, "teprsnow is required when swsnow is True"
            assert self.snowcoef is not None, "snowcoef is required when swsnow is True"

        if self.swfrost == 1:
            assert self.tfrostst is not None, (
                "tfrostst is required when swfrost is True"
            )
            assert self.tfrostend is not None, (
                "tfrostend is required when swfrost is True"
            )

        return self
