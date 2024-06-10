"""
Meteorological settings for SWAP simulations.

This object is used to store the meteorological settings of the simulation. it
also requires the MeteoData object to be passed as an attribute. Upon creation of
the final model, the .met file is automatically created.

Classes:
    PenmanMonteith: Holds the Penman-Monteith settings of the simulation.
    Meteorology: Holds the settings of the meteo section of the .swp file.
"""

from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from ..core.utils.files import save_file
from ..core.utils.valueranges import UNITRANGE
from .metfile import MeteoData
from pydantic import Field, model_validator
from typing import Optional, Literal


class Meteorology(PySWAPBaseModel):
    """Meteorological settings of the simulation.

    Attributes:
        metfil (str): name of the .met file. Default 'meteo.met'.
        lat (float): latitude of the meteo station [degrees].
        swetr (int): Switch type of weather data for potential evapotranspiration:
            0 - Use basic weather data and apply Penman-Monteith equation.
            1 - Use reference evapotranspiration data in combination with crop factors.
        swdivide (int): Switch for distribution of E and T. Defaults to 0:
            0 - Based on crop and soil factors.
            1 - Based on direct application of Penman-Monteith.
        swmetdetail (int): Switch for time interval of evapotranspiration and rainfall weather data:
            0 - Daily data.
            1 - Subdaily data.
        swrain (int): Switch for use of actual rainfall intensity, defaults to 0:
            0 - Use daily rainfall amounts.
            1 - Use daily rainfall amounts + mean intensity.
            2 - Use daily rainfall amounts + duration.
            3 - Use detailed rainfall records (dt < 1 day), as supplied in separate file.
        swetsine (int): Switch, distribute daily Tp and Ep according to sinus wave, default to 0:
            0 - No distribution.
            1 - Distribute Tp and Ep according to sinus wave.
        meteodata (MeteoData): MeteoData model.
        penman_monteith (PenmanMonteith): PenmanMonteith model.
        table_rainflux (Table): rainfall intensity RAINFLUX as function of time TIME.
        rainfil (str): file name of file with detailed rainfall data.
        nmetdetail (int): Number of weather data records each day.

    Methods:
        write_met: Writes the .met file.
    """

    metfil: str
    lat: float = Field(ge=-90, le=90)
    swetr: Literal[0, 1]
    swdivide: Literal[0, 1]
    # TODO: SWRAIN should be optional, but Fortran code evaluates its presence anyway
    swrain: Optional[Literal[0, 1, 2, 3]] = 0
    # TODO: SWETSINE should be optional, but Fortran code evaluates its presence anyway
    swetsine: Literal[0, 1] = 0
    meteodata: Optional[MeteoData] = Field(
        default=None, repr=False, exclude=True)
    alt: float = Field(ge=-400.0, le=3000.0)
    altw: float = Field(default=None, ge=0.0, le=99.0)
    angstroma: float = Field(default=None, **UNITRANGE)
    angstromb: float = Field(default=None, **UNITRANGE)
    swmetdetail: Optional[Literal[0, 1]] = None
    table_rainflux: Optional[Table] = None
    rainfil: Optional[str] = None
    nmetdetail: Optional[int] = Field(default=None, ge=1, le=96)

    @model_validator(mode='after')
    def _validate_meteo_section(self):

        if self.swetr == 1:  # if PM method is NOT used
            assert self.swetsine is not None, "SWETSINE is required when SWETR is 1"
            assert self.swrain is not None, "SWRAIN is required when SWETR is 1"
            if self.swrain == 1:
                assert self.table_rainflux is not None, "RAINFLUX is required when SWRAIN is 1"
            elif self.swrain == 3:
                assert self.rainfil, "RAINFIL is required when SWRAIN is 3"

        else:
            assert self.alt is not None, "alt settings are required when SWETR is 0"
            assert self.altw is not None, "altw settings are required when SWETR is 0"
            assert self.angstroma is not None, "angstroma settings are required when SWETR is 0"
            assert self.angstromb is not None, "angstromb settings are required when SWETR is 0"
            assert self.swmetdetail is not None, "SWMETDETAIL is required when SWETR is 0"
            if self.swmetdetail == 1:
                assert self.nmetdetail is not None, "NMETDETAIL is required when SWMETDETAIL is 1"

    def write_met(self, path: str):
        """Writes the .met file.

        Note: in this function the extension is not passed because
        swp file requires the metfile parameter to be passed already with 
        the extension.

        Args:
            path (str): Path to the file.
        """
        save_file(
            string=self.meteodata.model_dump(mode='json')['content'],
            fname=self.metfil,
            path=path
        )

        print(f'{self.metfil} saved.')
