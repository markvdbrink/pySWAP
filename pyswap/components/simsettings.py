# mypy: disable-error-code="call-overload, misc, override, type-arg"

import logging as _logging
from datetime import date as _date
from typing import (
    ClassVar as _ClassVar,
    Literal as _Literal,
)

from pydantic import (
    ConfigDict as _ConfigDict,
    Field as _Field,
    model_validator as _model_validator,
)

from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import (
    BASE_PATH as _BASE_PATH,
    EXTENSIONS as _EXTENSIONS,
    FNAME_OUT as _FNAME_OUT,
)
from pyswap.core.fields import (
    Arrays as _Arrays,
    DayMonth as _DayMonth,
    String as _String,
    StringList as _StringList,
    Subsection as _Subsection,
)
from pyswap.core.valueranges import (
    UNITRANGE as _UNITRANGE,
    YEARRANGE as _YEARRANGE,
)
from pyswap.utils.mixins import (
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = ["GeneralSettings", "RichardsSettings"]

logger = _logging.getLogger(__name__)


class _ExtensionMixin(_PySWAPBaseModel, _SerializableMixin):
    """Handle creation of the switches through direct assignment and list."""

    swwba: _Literal[1, 0] | None = _Field(default=None, validation_alias="wba")
    swend: _Literal[1, 0] | None = _Field(default=None, validation_alias="end")
    swvap: _Literal[1, 0] | None = _Field(default=None, validation_alias="vap")
    swbal: _Literal[1, 0] | None = _Field(default=None, validation_alias="bal")
    swblc: _Literal[1, 0] | None = _Field(default=None, validation_alias="blc")
    swsba: _Literal[1, 0] | None = _Field(default=None, validation_alias="sba")
    swate: _Literal[1, 0] | None = _Field(default=None, validation_alias="ate")
    swbma: _Literal[1, 0] | None = _Field(default=None, validation_alias="bma")
    swdrf: _Literal[1, 0] | None = _Field(default=None, validation_alias="drf")
    swswb: _Literal[1, 0] | None = _Field(default=None, validation_alias="swb")
    swini: _Literal[1, 0] | None = _Field(default=None, validation_alias="ini")
    swinc: _Literal[1, 0] | None = _Field(default=None, validation_alias="inc")
    swcrp: _Literal[1, 0] | None = _Field(default=None, validation_alias="crp")
    swstr: _Literal[1, 0] | None = _Field(default=None, validation_alias="str")
    swirg: _Literal[1, 0] | None = _Field(default=None, validation_alias="irg")
    swcsv: _Literal[1, 0] | None = _Field(default=None, validation_alias="csv")
    swcsv_tz: _Literal[1, 0] | None = _Field(default=None, validation_alias="csv_tz")


class GeneralSettings(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """General settings of the simulation.

    Attributes:
        pathwork (str): Path to the working directory. **Immutable attribute**.
        pathatm (str): Path to folder with weather files. **Immutable attribute**.
        pathcrop (str): Path to folder with crop files. **Immutable attribute**.
        pathdrain (str): Path to folder with drainage files. **Immutable attribute**.
        swscre (Literal[0, 1, 2]): Switch, display progression of simulation
            run to screen:

            * 0 - Don't display to screen (default)
            * 1 - Display water balance components
            * 2 - Display daynumber

        swerror (Literal[0, 1]): Switch for printing errors to screen:

            * 0 - Don't print error messages (default)
            * 1 - Print error messages

        tstart (str): Start date of simulation run [YYYY-MM-DD].
        tend (str): End date of simulation run [YYYY-MM-DD].
        nprintday (int): Number of output times during a day [1..1440, -]
        swmonth (Literal[0, 1]): Switch for when to write output:

            * 0 - Output each month
            * 1 - Output via `period`, `swres` or `swodat` (default)
                    **Activates**: [`period`, `swres`, `swodat`]

        period (Optional[int]): Fixed output interval [0..366, day]
        swres (Optional[Literal[0, 1]]): Switch whether to reset output interval counter
            each year:

            * 0 - No
            * 1 - Yes

        swodat (Optional[Literal[0, 1]]): Switch for extra output dates.

            * 0 - No extra output dates
            * 1 - Extra output dates.
                    **Activates**: [`outdatin`]

        outdatin (Optional[DateList]): List of specific dates [YYY-MM-DD].
        swyrvar (Literal[0, 1]): Output times for overall water and solute
            balances in *.BAL and *.BLC file: choose output at a fixed date
            each year or at different dates

            * 0 - Each year output at the same date (default).
                    **Activates**: [`datefix`]
            * 1 - Output at specific dates.
                    **Activates**: [`outdat`]

        datefix (Optional[DayMonth]): Fixed date for output [MM-DD].
        outdat (Optional[DateList]): Specify all output dates [YYYY-MM-DD]
        outfil (str): Generic file name of output files. **Immutable attribute**.
        swheader (Literal[0, 1]): Print header at the start of each
            balance period:

            * 0 - Don't print header (default)
            * 1 - Print header

        extensions (list): List of file extensions SWAP should return. It is recommended to use
            "csv" and/or "csv_tz", as it includes the information of the other files.
            Available options are:

            * "csv": Variables over time
                    **Activates**: [`inlist_csv`]
            * "csv_tz": Variables over time and depth
                    **Activates**: [`inlist_csv_tz`]
            * "wba": Cumulative water balance
            * "end": End-conditions
            * "vap": Soil profiles of moisture, solute and temperature
            * "bal": Yearly water balance
            * "blc": Detailed yearly water balance
            * "sba": Cumulative solute balance
            * "ate": Soil temperature profiles
            * "bma": Water fluxes (only for macropore flow)
            * "drf": Drainage fluxes (only for extended drainage)
            * "swb": Surface water reservoir (only for extended drainage)
            * "ini": Initial soil physical and heat parameters
            * "inc": Water balance increments
            * "crp": Simple or detailed crop growth model output
            * "str": Oxygen, drought, salinity and frost stress
            * "irg": Irrigation gifts

        inlist_csv (Optional[StringList]): List of variables for the csv output.
            Available options for the total water balance are:

            * "RAIN" - Rainfall for current time interval [cm]
            * "SNOW" - Snowfall for current time interval [cm]
            * "IRRIG" - Irrigation for current time interval [cm]
            * "INTERC" - Crop interception for current time interval [cm]
            * "RUNON" - Runon for current time interval [cm]
            * "RUNOFF" - Runoff for current time interval [cm]
            * "TACT" - Crop transpiration for current time interval [cm]
            * "EACT" - Soil evaporation for current time interval [cm]
            * "SUBLIM" - Sublimated snow [cm]
            * "DRAINAGE" - Total drainage for current time interval [cm]
            * "VOLACT" - Water storage (L) of soil column [cm]
            * "DSTOR" - Change in water storage of [cm]
            * "QBOTTOM" - Net flow across bottom boundary for current time interval [cm]

            Miscellaneous variables with respect to ponding and groundwater level are:

            * "RAIN_NET" - Net rainfall for current time interval [cm]
            * "IRRIG_NET" - Net irrigation for current time interval [cm]
            * "SSNOW" - Amount of snow [cm]
            * "POND" - Ponding height [cm]
            * "GWL" - Groundwater level [cm + sl]

            Variables with respect to the simulation of evapotranspiration are:

            * "TPOT" - Potential crop transpiration for current time interval [cm]
            * "TACT" - Crop transpiration for current time interval [cm]
            * "EPOT" - Potential Soil evaporation for current time interval [cm]
            * "EACT" - Soil evaporation for current time interval [cm]
            * "INTERC" - Crop interception for current time interval [cm]
            * "TREDDRY" - Reduction due to drought stress [cm]
            * "TREDWET" - Reduction due to oxygen stress (too wet) [cm]
            * "TREDSOL" - Reduction due to salinity stress [cm]
            * "TREDFRS" - Reduction due to frost stress [cm]

            General crop parameters are:

            * "TSUM" - Temperature sum from start to end of growing season of the crop [°C]
            * "DVS" - Crop development stage [-]
            * "HEIGHT" - Crop height [cm]
            * "CRPFAC" - Crop factor [-]
            * "LAIPOT" - Leaf area index for potential run [m² m⁻²]
            * "LAI" - Leaf area index [m² m⁻²]
            * "RDPOT" - Rooting depth for potential run [cm]
            * "RD" - Rooting depth [cm]

            Available WOFOST variables are:

            * "PGASSPOT" - Assimilation rate after nitrogen stress and max. yield, potential crop growth [kg ha⁻¹]
            * "PGASS" - Assimilation rate after nitrogen stress and max. yield, actual crop growth [kg ha⁻¹]
            * "CPWDM" - Dry weight of dead and living plant organs for potential growth [kg ha⁻¹]
            * "CWDM" - Dry weight of dead and living plant organs [kg ha⁻¹]
            * "CPWSO" - Dry weight of storage organ for potential growth [kg ha⁻¹]
            * "CWSO" - Dry weight of storage organ [kg ha⁻¹]
            * "PWLV" - Dry weight of plant leaves for potential growth [kg ha⁻¹]
            * "WLV" - Dry weight of plant leaves [kg ha⁻¹]
            * "PWST" - Dry weight of plant stem for potential growth [kg ha⁻¹]
            * "WST" - Dry weight of plant stem [kg ha⁻¹]
            * "PWRT" - Dry weight of plant root for potential growth [kg ha⁻¹]
            * "WRT" - Dry weight of plant root [kg ha⁻¹]
            * "DWSO" - Dry weight of plant storage organs of actual crop [kg ha⁻¹]
            * "DWLV" - Dry weight of plant leaves of actual crop [kg ha⁻¹]
            * "DWLVPOT" - Dry weight of plant leaves of potential crop [kg ha⁻¹]
            * "DWST" - Dry weight of plant stem of actual crop [kg ha⁻¹]
            * "DWSTPOT" - Dry weight of plant stem of potential crop [kg ha⁻¹]
            * "DWRT" - Dry weight of plant roots of actual crop [kg ha⁻¹]
            * "DWRTPOT" - Dry weight of plant roots of potential crop [kg ha⁻¹]
            * "PGRASSDM" - Dry weight of dead and living grass organs for potential run [kg ha⁻¹]

            Variables for the grass module of WOFOST are:

            * "GRASSDM" - Dry weight of dead and living grass organs [kg ha⁻¹]
            * "PMOWDM" - Dry weight of harvested grass for potential run [kg ha⁻¹]
            * "MOWDM" - Dry weight of harvested grass [kg ha⁻¹]
            * "PGRAZDM" - Cumulative dry weight of grass consumed with grazing for potential run [kg ha⁻¹]
            * "GRAZDM" - Cumulative dry weight of grass consumed with grazing [kg ha⁻¹]
            * "PLOSSDM" - Total loss of potential harvest due to insufficient pressure head [kg ha⁻¹]
            * "LOSSDM" - Total loss of actual harvest due to insufficient pressure head [kg ha⁻¹]

            Variables that involve solute transport are:

            * "SQPREC" - Cumulative amount of solutes in precipitation [g cm⁻²]
            * "SQIRRIG" - Cumulative amount of solutes in irrigation water [g cm⁻²]
            * "SQBOT" - Cumulative amount of solutes passed through the soil column bottom [g cm⁻²]
            * "SQDRA" - Total amount of solutes transported to drainage canals [g cm⁻²]
            * "DECTOT" - Cumulative amount of solute decomposition [g cm⁻²]
            * "ROTTOT" - Cumulative amount of solutes extracted by plant roots [g cm⁻²]
            * "SAMPRO" - Total amount of solutes in soil column [g cm⁻²]
            * "SOLBAL" - Cumulative solute balance (M/L²) for current balance period [g cm⁻²]

        inlist_csv_tz (Optional[StringList]): List of variables over depth for
            the csv tz output. Available options are:

            * "H" - Pressure head [cm]
            * "WC" - Volumetric water content [cm³ cm⁻³]
            * "TEMP" - Soil temperature [°C]
            * "K" - Hydraulic conductivity [cm d⁻¹]
            * "CONC" - Solute concentration [g cm⁻³]
            * "CONCADS" - Adsorbed solute content [g cm⁻³]
            * "O2TOP" - Oxygen concentration at top of compartment [kg m⁻³]
            * "HEACAP" - Soil heat capacity [J m⁻³ K⁻¹]
            * "HEACON" - Soil heat conductivity [W m⁻¹ K⁻¹]
            * "RWU" - Root water uptake [cm d⁻¹]
            * "PRWU" - Potential root water uptake [cm d⁻¹]
            * "RDENS" - Relative root distribution [-]
            * "LRV" - Root length density distribution [cm cm]

        swafo (Literal[0, 1, 2]): Switch, output file with formatted hydrological data:

            * 0 - No output (default)
            * 1 - Output to a file named .AFO.
                    **Activates**: [`critdevmasbal`, `swdiscrvert`]
            * 2 - Output to a file named .BFO.
                    **Activates**: [`critdevmasbal`, `swdiscrvert`]

        swaun (Literal[0, 1, 2]): Switch, output file with unformatted hydrological data:

            * 0 - No output (default)
            * 1 - Output to a file named .AUN.
                    **Activates**: [`critdevmasbal`, `swdiscrvert`]
            * 2 - Output to a file named .BUN.
                    **Activates**: [`critdevmasbal`, `swdiscrvert`]

        critdevmasbal (Optional[float]): Critical deviation in
            water balance during `period` [0.0..1.0, cm].
        swdiscrvert (Optional[Literal[0, 1]]): Switch to convert vertical discretization:

            * 0 - No conversion (default)
            * 1 - Convert vertical discretization.
                    **Activates**: [`numnodnew`, `dznew`]

        numnodnew (Optional[int]): New number of nodes [1..macp, -].
        dznew (Optional[FloatList]): New thickness of compartments [1e-6..5e2, cm].
    """

    model_config = _ConfigDict(
        validate_assignment=True, use_enum_values=True, extra="ignore"
    )
    _all_extensions: _ClassVar[list[str]] = _EXTENSIONS
    extensions: list[str] = _Field(default_factory=list, exclude=True)
    exts: _Subsection[_ExtensionMixin] | None = None
    pathwork: _String = _Field(default=_BASE_PATH, frozen=True)
    pathatm: _String = _Field(default=_BASE_PATH, frozen=True)
    pathcrop: _String = _Field(default=_BASE_PATH, frozen=True)
    pathdrain: _String = _Field(default=_BASE_PATH, frozen=True)
    swscre: _Literal[0, 1, 3] = 0
    swerror: _Literal[0, 1] = 0
    tstart: _date | None = None
    tend: _date | None = None
    nprintday: int = _Field(default=1, ge=1, le=1440)
    swmonth: _Literal[0, 1] | None = None
    swyrvar: _Literal[0, 1] | None = None
    period: int | None = _Field(default=None, **_YEARRANGE)
    swres: _Literal[0, 1] | None = None
    swodat: _Literal[0, 1] | None = None
    outdatin: _Arrays | None = None
    datefix: _DayMonth | None = None
    outdat: _Arrays | None = None
    outfil: _String = _Field(default=_FNAME_OUT, frozen=True)
    swheader: _Literal[0, 1] = 0
    inlist_csv: _StringList | None = None
    inlist_csv_tz: _StringList | None = None
    swafo: _Literal[0, 1, 2] = 0
    swaun: _Literal[0, 1, 2] = 0
    critdevmasbal: float | None = _Field(default=None, **_UNITRANGE)
    swdiscrvert: _Literal[0, 1] = 0
    numnodnew: int | None = None
    dznew: _Arrays | None = None

    @_model_validator(mode="after")
    def validate_extensions(self):
        invalid_extensions = [
            ext for ext in self.extensions if ext not in self._all_extensions
        ]
        if invalid_extensions:
            msg = f"Invalid extensions: {', '.join(invalid_extensions)}"
            raise ValueError(msg)

        # Create the _ExtensionMixin object without triggering validation
        object.__setattr__(
            self,
            "exts",
            _ExtensionMixin(**{
                ext: 1 if ext in self.extensions else 0 for ext in self._all_extensions
            }),
        )
        return self


class RichardsSettings(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Settings for the Richards' equation.

    Attributes:
        swkmean (Literal[1, 2, 3, 4, 5, 6]): Switch for averaging method of hydraulic conductivity:

            * 1 - Unweighted arithmic mean (recommended)
            * 2 - Weighted arithmic mean
            * 3 - Unweighted geometric mean
            * 4 - Weighted geometric mean
            * 5 - Unweighted harmonic mean
            * 6 - Weighted harmonic mean

        swkimpl (Literal[0, 1]): Switch for updating hydraulic conductivity during iteration:

            * 0 - Don't update
            * 1 - Update

        dtmin (float): Minimum timestep [1.0e-7..0.1, d]
        dtmax (float): Maximum timestep [dtmin..1, d]
        gwlconv (float): Maximum difference of groundwater level between time steps [1.0e-5..1.0e3, cm]
        critdevh1cp (float): Maximum relative difference in pressure heads per compartment [1.0e-10..1.0e3, cm]
        critdevh2cp (float): Maximum absolute difference in pressure heads per compartment [1.0e-10..1.0e3, cm]
        critdevponddt (float): Maximum water balance error of ponding layer [1.0e-6..0.1, cm]
        maxit (int): Maximum number of iteration cycles [5..100, -]
        maxbacktr (int): Maximum number of back track cycles within an iteration cycle [1..10, -]
    """

    swkmean: _Literal[1, 2, 3, 4, 5, 6] | None = None
    swkimpl: _Literal[0, 1] | None = None
    dtmin: float | None = _Field(default=0.000001, ge=1e-7, le=0.1)
    dtmax: float | None = _Field(default=0.04, ge=0.000001, le=1.0)
    gwlconv: float | None = _Field(default=100.0, ge=1e-5, le=1000.0)
    critdevh1cp: float | None = _Field(default=0.01, ge=1e-10, le=1e3)
    critdevh2cp: float | None = _Field(default=0.1, ge=1e-10, le=1e3)
    critdevponddt: float | None = _Field(default=0.0001, ge=1e-6, le=0.1)
    maxit: int | None = _Field(default=30, ge=5, le=100)
    maxbacktr: int | None = _Field(default=3, ge=1, le=10)
