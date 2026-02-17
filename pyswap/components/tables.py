# pyright: reportInvalidTypeForm=false

from typing import Literal

import pandera as pa
from pandera.typing import Series

from pyswap.core.basemodel import BaseTableModel
from pyswap.core.valueranges import DVSRANGE, UNITRANGE, YEARRANGE

__all__ = [
    "AMAXTB",
    "CFTB",
    "CHTB",
    "CO2AMAXTB",
    "CO2EFFTB",
    "CO2TRATB",
    "CROPROTATION",
    "CSEEPARR",
    "DATET",
    "DATEHARVEST",
    "DATOWLTB1",
    "DATOWLTB2",
    "DATOWLTB3",
    "DATOWLTB4",
    "DATOWLTB5",
    "DAILYMETEODATA",
    "DC1TB",
    "DC2TB",
    "DETAILEDRAINFALL",
    "DMGRZTB",
    "DMMOWDELAY",
    "DMMOWTB",
    "DRAINAGELEVELTOPPARAMS",
    "DRNTB",
    "DTSMTB",
    "FOTB",
    "FLTB",
    "FRTB",
    "FSTB",
    "GCTB",
    "GWLEVEL",
    "HAQUIF",
    "HBOT5",
    "INIPRESSUREHEAD",
    "INITSOILTEMP",
    "INISSOIL",
    "INTERTB",
    "IRRIGEVENTS",
    "KYTB",
    "LSDATB",
    "LSDBTB",
    "LOSSGRZTB",
    "LOSSMOWTB",
    "MANSECWATLVL",
    "MRFTB",
    "MISC",
    "MXPONDTB",
    "OUTDAT",
    "OUTDATIN",
    "PRIWATLVL",
    "QBOT2",
    "QBOT4",
    "QDRNTB",
    "QTAB",
    "QWEIR",
    "QWEIRTB",
    "RAINFLUX",
    "RDTB",
    "RDCTB",
    "RDRRTB",
    "RDRSTB",
    "RLWTB",
    "RFSETB",
    "SECWATLVL",
    "SHORTINTERVALMETEODATA",
    "SLATB",
    "SOILHYDRFUNC",
    "SOILPROFILE",
    "SOILTEXTURES",
    "TC1TB",
    "TC2TB",
    "TC3TB",
    "TC4TB",
    "TC7TB",
    "TC8TB",
    "TMPFTB",
    "TMNFTB",
    "VERNTB",
    "WRTB",
]


# %% ++++++++++++++++++++++++++++ CROP TABLES ++++++++++++++++++++++++++++

crop_tables = [
    "DATEHARVEST",
    "RDTB",
    "RDCTB",
    "GCTB",
    "CFTB",
    "INTERTB",
    "KYTB",
    "MRFTB",
    "WRTB",
    "CROPROTATION",
    "DTSMTB",
    "VERNTB",
    "SLATB",
    "AMAXTB",
    "TMPFTB",
    "TMNFTB",
    "RFSETB",
    "FRTB",
    "FLTB",
    "FSTB",
    "FOTB",
    "RDRRTB",
    "RDRSTB",
    "DMGRZTB",
    "LSDATB",
    "LSDBTB",
    "RLWTB",
    "DMMOWTB",
    "DMMOWDELAY",
    "LOSSGRZTB",
    "LOSSMOWTB",
    "IRRIGEVENTS",
    "TC1TB",
    "TC2TB",
    "TC3TB",
    "TC4TB",
    "TC7TB",
    "TC8TB",
    "DC1TB",
    "DC2TB",
    "CO2EFFTB",
    "CO2TRATB",
    "CO2AMAXTB",
]


class DATEHARVEST(BaseTableModel):
    """Table with harvest dates.

    Attributes:
        DATEHARVEST (Series[pa.DateTime]): Date of harvest [yyyy-mm-dd].
    """

    DATEHARVEST: Series[pa.DateTime]


class RDTB(BaseTableModel):
    """Table with crop rooting depth as a function of development stage or day number.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day of the year [0..366, -].
        RD (Series[float]): Rooting depth of the crop [0..1000, cm].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    RD: Series[float] = pa.Field(ge=0.0, le=100.0)


class RDCTB(BaseTableModel):
    """Table with root density as function of relative rooting depth.

    Attributes:
        RRD (Series[float]): Relative rooting depth of the crop [0..1 -].
        RDENS (Series[float]): Root density of the crop [0..100, cm/cm^3].

    """

    RRD: Series[float] = pa.Field(ge=0.0, le=100.0)
    RDENS: Series[float] = pa.Field(**UNITRANGE)


class GCTB(BaseTableModel):
    """Table with Leaf Area Index or Soil Cover Fraction as function of development stage.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        LAI (Series[float]): Leaf Area Index of the crop [0..12, (m^2 leaf)/(m^2 soil)]
        SCF (Series[float]): Soil Cover Fraction [0..1, (m^2 cover)/(m^2 soil)]
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    LAI: Series[float] = pa.Field(ge=0.0, le=12.0)
    SCF: Series[float] = pa.Field(ge=0.0, le=1.0)


class CFTB(BaseTableModel):
    """Table with crop factor as function of development stage or day number.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        CF (Series[float]): Crop factor [0..2, -].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    CF: Series[float] | None


class CHTB(BaseTableModel):
    """Crop height as function of development stage or day number.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        CH (Series[float]): Crop height [0..1e4, cm].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    # Added CF for compatibility with example grass files in original SWAP
    # distribution that are used for testing this package. CF is only stated but not used there.
    CF: Series[float] | None
    CH: Series[float] | None


class INTERTB(BaseTableModel):
    """Table with interception parameters for closed forest canopies.

    Attributes:
        T (Series[int]): Day of the year [0..366, d].
        PFREE (Series[float]): Free throughfall coefficient [0..1, -].
        PSTEM (Series[float]): Stem flow coefficient [0..1, -].
        SCANOPY (Series[float]): Storage capacity of canopy [0..10, cm].
        AVPREC (Series[float]): Average rainfall intensity [0..100, cm/d].
        AVEVAP (Series[float]): Average evaporation intensity during rainfall from a wet canopy [0..10, cm/d].
    """

    T: Series[float] = pa.Field(ge=0, le=366)
    PFREE: Series[float] = pa.Field(ge=0.0, le=1.0)
    PSTEM: Series[float] = pa.Field(ge=0.0, le=1.0)
    SCANOPY: Series[float] = pa.Field(ge=0.0, le=10.0)
    AVPREC: Series[float] = pa.Field(ge=0.0, le=100.0)
    AVEVAP: Series[float] = pa.Field(ge=0.0, le=10.0)


class KYTB(BaseTableModel):
    """Table with yield response factor as function of development stage.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        KY (Series[float]): Yield response factor of the crop [0..5, -].
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    KY: Series[float] = pa.Field(ge=0.0, le=5.0)


class MRFTB(BaseTableModel):
    """Ratio total root respiration to maintenace respiration.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        MAX_RESP_FACTOR (Series[float]): Ratio root total respiration with maintenance respiration [1..5, -].
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    MAX_RESP_FACTOR: Series[float] = pa.Field(ge=1.0, le=5.0)


class WRTB(BaseTableModel):
    """Table with dry weight of roots at soil surface as function of development stage.

    Attributes:
        DVS (Series[float]): Development stage of the crop  [0..2, -].
        W_ROOT_SS (Series[float]): Dry weight of roots at soil surface [0..10, kg/m3].
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    W_ROOT_SS: Series[float] = pa.Field(ge=0.0, le=10.0)


class CROPROTATION(BaseTableModel):
    """Table with crop rotation settings.

    Attributes:
        CROPSTART (Series[pa.DateTime]): Start date of the crop [dd-mmm-yyyy] (e.g. 01-jan-2000).
        CROPEND (Series[pa.DateTime]): End date of the crop [dd-mmm-yyyy] (e.g. 01-jan-2000)..
        CROPFIL (Series[str]): Crop file name.
        CROPTYPE (Series[int]): Crop module type:

            * 1: Simple
            * 2: WOFOST general
            * 3: WOFOST grass
    """

    CROPSTART: Series[pa.DateTime]
    CROPEND: Series[pa.DateTime]
    CROPFIL: Series[str]
    CROPTYPE: Series[int] = pa.Field(ge=1, le=3)


# WOFOST-specific tables
class DTSMTB(BaseTableModel):
    """Table with increase in temperature sum as function of daily average temperature.

    Attributes:
        TAV (Series[float]): Daily average temperature [0..100, °C].
        DTSM (Series[float]): Increase in temperature sum [0..60, °C].
    """

    TAV: Series[float] = pa.Field(ge=0.0, le=100.0)
    DTSM: Series[float] = pa.Field(ge=0.0, le=60.0)


class VERNTB(BaseTableModel):
    """Table with rate of vernalisation as function of average air temperature.

    Attributes:
        TAV (Series[float]): Daily average temperature [?..?, °C].
        ROV (Series[float]): Rate of vernalisation [?..?, /d].
    """

    TAV: Series[float]
    ROV: Series[float]


class SLATB(BaseTableModel):
    """Table with specific leaf area as function of crop development stage or day number.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        SLA (Series[float]): Leaf area [0..1, ha/kg].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    SLA: Series[float] = pa.Field(ge=0.0, le=1.0)


class AMAXTB(BaseTableModel):
    """Table with maximum CO2 assimilation rate as function of development stage or day number.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        AMAX (Series[float]): Maximum CO2 assimilation rate [0..100, kg/ha/hr].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    AMAX: Series[float] = pa.Field(ge=0.0, le=100.0)


class TMPFTB(BaseTableModel):
    """Table with the reduction the maximum CO2 assimilation rate as function of average day temperature.

    Attributes:
        TAVD (Series[float]): Average day temperature [-10..50, °C].
        TMPF (Series[float]): Reduction factor of maximum CO2 assimilation rate [0..1, -].
    """

    TAVD: Series[float] = pa.Field(ge=-10.0, le=50.0)
    TMPF: Series[float] = pa.Field(ge=0.0, le=1.0)


class TMNFTB(BaseTableModel):
    """Table with the reduction the maximum CO2 assimilation rate as function of minimum day temperature.

    Attributes:
        TMNR (Series[float]): Minimum day temperature [-10..50, °C].
        TMNF (Series[float]): Reduction factor of maximum CO2 assimilation rate [0..1, -].
    """

    TMNR: Series[float] = pa.Field(ge=-10.0, le=50.0)
    TMNF: Series[float] = pa.Field(ge=0.0, le=1.0)


class RFSETB(BaseTableModel):
    """Table with reduction factor of senescence as function of development stage or day number.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        RFSE (Series[float]): Reduction factor of senescence [0..1, -].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    RFSE: Series[float] = pa.Field(ge=0.0, le=1.0)


class FRTB(BaseTableModel):
    """Table with fraction of total dry matter increase partitioned to the roots.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        FR (Series[float]): Fraction of total dry matter increase partitioned to the roots [0..1, kg/kg].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    FR: Series[float] = pa.Field(ge=0.0, le=1.0)


class FLTB(BaseTableModel):
    """Table with fraction of total above ground dry matter increase partitioned to the leaves

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        FL (Series[float]): Fraction of total above ground dry matter increase partitioned to the leaves [0..1, kg/kg].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    FL: Series[float] = pa.Field(ge=0.0, le=1.0)


class FSTB(BaseTableModel):
    """Table with fraction of total above ground dry matter increase partitioned to the stems.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        DNR (Series[float]): Day number [0..366, -].
        FS (Series[float]): Fraction of total above ground dry matter increase partitioned to the stems [0..1, kg/kg].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    FS: Series[float] = pa.Field(ge=0.0, le=1.0)


class FOTB(BaseTableModel):
    """Table with fraction of total above ground dry matter increase partitioned to the storage organs.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        FO (Series[float]): Fraction of total above ground dry matter increase partitioned to the storage organs [0..1, kg/kg].
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FO: Series[float] = pa.Field(ge=0.0, le=1.0)


class RDRRTB(BaseTableModel):
    """Table with relative death rates of roots as function of development stage.

    Attributes:
        DVS (Series[float]): Development stage of the crop [0..2, -].
        RDRR (Series[float]): Relative death rates of roots [0..?, kg/kg/d].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    RDRR: Series[float] = pa.Field(ge=0.0)


class RDRSTB(BaseTableModel):
    """Talbe with relative death rates of stems as function of development stage.

    Attributes:
        DVS (Series[float]): Development stage of the crop  [0..2, -].
        RDRS (Series[float]): Relative death rates of stems [0..?, kg/kg/d].
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    RDRS: Series[float] = pa.Field(ge=0.0)


class RLWTB(BaseTableModel):
    """rooting depth RL [0..5000 cm, R] as function of root weight RW [0..5000 kg DM/ha, R]

    Attributes:
        RW (Series[float]): rooting depth
        RL (Series[float]): root weight
    """

    RW: Series[float] = pa.Field(ge=0.0, le=5000.0)
    RL: Series[float] = pa.Field(ge=0.0, le=5000.0)


class CO2EFFTB(BaseTableModel):
    """Correction factor light use efficiency for change in CO2 concentration."""

    CO2PPM: Series[float]
    FACTOR: Series[float]


class CO2TRATB(BaseTableModel):
    """Correction factor maximum transpiration rate for change in CO2 concentration."""

    CO2PPM: Series[float]
    FACTOR: Series[float]


class CO2AMAXTB(BaseTableModel):
    """Correction factor assimilation rate for change in CO2 concentration."""

    CO2PPM: Series[float]
    FACTOR: Series[float]


# Tables of grassland management


class DMGRZTB(BaseTableModel):
    """Table with threshold of above ground dry matter to trigger grazing as function of daynumber.

    Attributes:
        DNR (Series[float]): Day number [1..366, d].
        DMGRZ (Series[float]): Threshold of above ground dry matter to trigger grazing [0..1e6, kg DM/ha].
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    DMGRZ: Series[float] = pa.Field(ge=0.0, le=1.0e6)


class LSDATB(BaseTableModel):
    """Table with actual livestock density of each grazing period.

    !!! note

        Total number of periods should be equal to number of periods in SEQGRAZMOW

    Attributes:
        SEQNR (Series[int]): Number of the sequence period with mowing/grazing [0..366, d]
        LSDA (Series[float]): Actual livestock (LS) density of the grazing period [0.0..1000.0, LS/ha]
    """

    SEQNR: Series[int] = pa.Field(**YEARRANGE)
    LSDA: Series[float] = pa.Field(ge=0.0, le=1000.0)


class LSDBTB(BaseTableModel):
    """Table with relation between livestock density, number of grazing days and dry matter uptake

    Attributes:
        LSDB (Series[float]): Basic Live Stock Density [0..1000, LS/ha]
        DAYSGRAZING (Series[float]): Maximum days of grazing [0..366, d]
        UPTGRAZING (Series[float]): Dry matter uptake by grazing [0..1000, kg/ha]
        LOSSGRAZING (Series[float]): Dry matter loss during grazing due to droppings and treading [0..1000, kg/ha]
    """

    LSDb: Series[float] | None = pa.Field(ge=0.0, le=1000.0)
    LSDB: Series[float] | None = pa.Field(ge=0.0, le=1000.0)
    DAYSGRAZING: Series[float] = pa.Field(**YEARRANGE)
    UPTGRAZING: Series[float] = pa.Field(ge=0.0, le=1000.0)
    LOSSGRAZING: Series[float] = pa.Field(ge=0.0, le=1000.0)

    def __post_init__(self):
        from warnings import warn

        warn(
            "The use of `LSDb` is deprecated and will be removed in a later version. Please use `LSDB`.",
            FutureWarning,
            stacklevel=4,
        )


class DMMOWTB(BaseTableModel):
    """Table with thresholds of above ground dry matter to trigger mowing as function of daynumber.

    !!! note

        Maximum 20 records

    Attributes:
        DNR (Series[float]): Day number [1..366, d].
        DMMOW (Series[float]): threshold of above ground dry matter [0..1e6, kg DM/ha]
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    DMMOW: Series[float] = pa.Field(ge=0.0, le=1.0e6)


class DMMOWDELAY(BaseTableModel):
    """Table with relation between dry matter harvest and days of delay in regrowth after mowing.

    Attributes:
        DMMOWDELAY (Series[float]): Dry matter harvest [0..1e6, kg/ha].
        DAYDELAY (Series[int]): Days of delay in regrowth [0..366, d].
    """

    DMMOWDELAY: Series[float] = pa.Field(ge=0.0, le=1.0e6)
    DAYDELAY: Series[int] = pa.Field(**YEARRANGE)


class LOSSGRZTB(BaseTableModel):
    """Table with relation between pressure head and fraction of dry matter losses during grazing.

    Attributes:
        HGRZ (Series[float]): Pressure head [-1000..0, cm]
        HLOSSGRZ (Series[float]): Fraction of dry matter loss [0..1, -]
    """

    HGRZ: Series[float] = pa.Field(ge=1000, le=0)
    HLOSSGRZ: Series[float] = pa.Field(**UNITRANGE)


class LOSSMOWTB(BaseTableModel):
    """Table with relation between pressure head and fraction of dry matter losses during mowing.

    Attributes:
        HMOW (Series[float]): Pressure head [-1000..0, cm]
        HLOSSMOW (Series[float]): Fraction of dry matter loss [0..1, -]
    """

    HMOW: Series[float] = pa.Field(ge=1000, le=0)
    HLOSSMOW: Series[float] = pa.Field(**UNITRANGE)


irrigation_tables = [
    "IRRIGEVENTS",
    "TC1TB",
    "TC2TB",
    "TC3TB",
    "TC4TB",
    "TC7TB",
    "TC8TB",
    "DC1TB",
    "DC2TB",
]


class IRRIGEVENTS(BaseTableModel):
    """information for each fixed irrigation event.

    Attributes:
        IRDATE (Series[datetime]):date of irrigation.
        IRDEPTH (Series[float]): amount of water [0..1000 mm, R].
        IRCONC (Series[float]): concentration of irrigation water [0..1000 mg/cm3, R].
        IRTYPE (Series[int]): type of irrigation

            * 0 - sprinkling
            * 1 - surface

    """

    IRDATE: Series[pa.DateTime]
    IRDEPTH: Series[float] | None = pa.Field(default=None, ge=0.0, le=1000.0)
    IRCONC: Series[float] = pa.Field(ge=0.0, le=1000.0)
    IRTYPE: Series[int] = pa.Field(ge=0, le=1)


class TC1TB(BaseTableModel):
    """tc1tb option table"""

    DVS_TC1: Series[float] = pa.Field(ge=0.0, le=2.0)
    TREL: Series[float] = pa.Field(ge=0.0, le=1.0)


class TC2TB(BaseTableModel):
    """tc2tb option table"""

    DVS_TC2: Series[float] = pa.Field(ge=0.0, le=2.0)
    RAW: Series[float] = pa.Field(ge=0.0, le=1.0)


class TC3TB(BaseTableModel):
    """tc3tb option table"""

    DVS_TC3: Series[float] = pa.Field(ge=0.0, le=2.0)
    TAW: Series[float] = pa.Field(ge=0.0, le=1.0)


class TC4TB(BaseTableModel):
    """tc4tb option table"""

    DVS_TC4: Series[float] = pa.Field(ge=0.0, le=2.0)
    DWA: Series[float] = pa.Field(ge=0.0, le=500.0)


class TC7TB(BaseTableModel):
    """tc7tb option table"""

    DVS_TC7: Series[float] = pa.Field(ge=0.0, le=2.0)
    HCRI: Series[float] = pa.Field(ge=-1000.0, le=-100.0)


class TC8TB(BaseTableModel):
    """tc8tb option table"""

    DVS_TC8: Series[float] = pa.Field(ge=0.0, le=2.0)
    TCRI: Series[float] = pa.Field(ge=0.0, le=1.0)


class DC1TB(BaseTableModel):
    DVS_DC1: Series[float]
    DI: Series[float]


class DC2TB(BaseTableModel):
    DVS_DC2: Series[float]
    FID: Series[float]


# %% ++++++++++++++++++++++++++++ METEO TABLES ++++++++++++++++++++++++++++

meteo_tables = [
    "DAILYMETEODATA",
    "SHORTINTERVALMETEODATA",
    "DETAILEDRAINFALL",
    "RAINFLUX",
]


class DAILYMETEODATA(BaseTableModel):
    """Table with daily meteorological data.

    Attributes:
        STATION (Series[str]): Station identifier (e.g. station code or name).
            Expected to be a short string, unique per station in a dataset.
        DD (Series[str]): Day of month. Stored as strings to preserve leading
            zeros when present (e.g. "01", "02", ... "31").
        MM (Series[str]): Month of year as a two-character string (e.g. "01".."12").
        YYYY (Series[str]): Year as a string (e.g. "2024").
        RAD (Series[float]): Incoming shortwave (solar) radiation for the day
            (kJ m^-2 day^-1).
        TMIN (Series[float]): Daily minimum air temperature (°C).
        TMAX (Series[float]): Daily maximum air temperature (°C).
        HUM (Series[float]): Daily mean vapor pressure (kPa).
        WIND (Series[float]): Daily mean wind speed (m s^-1).
        RAIN (Series[float]): Daily accumulated precipitation (mm day^-1).
        ETREF (Series[float]): Reference evapotranspiration for the day (mm day^-1).
        WET (Series[float]): Fraction (0-1) of the day it was raining,
            necessary when swrain=1
    """

    STATION: Series[str]
    DD: Series[str]
    MM: Series[str]
    YYYY: Series[str]
    RAD: Series[float]
    TMIN: Series[float]
    TMAX: Series[float]
    HUM: Series[float]
    WIND: Series[float]
    RAIN: Series[float]
    ETREF: Series[float]
    WET: Series[float]


class SHORTINTERVALMETEODATA(BaseTableModel):
    Date: Series[pa.DateTime]
    Record: Series[int] = pa.Field(ge=1, le=10)
    Rad: Series[float]
    Temp: Series[float]
    Hum: Series[float]
    Wind: Series[float]
    Rain: Series[float]


class DETAILEDRAINFALL(BaseTableModel):
    Station: Series[str]
    Day: Series[int]
    Month: Series[int]
    Year: Series[int]
    Time: Series[float]
    Amount: Series[float]


class RAINFLUX(BaseTableModel):
    """Mean rainfall intensity as function of Julian time.

    Maximum of 30 records allowed.

    Attributes:
        TIME (Series[float]): day of the year
        RAINFLUX (Series[float]): rainfall in mm d^-1.
    """

    TIME: Series[float] = pa.Field(**YEARRANGE)
    RAINFLUX: Series[float] = pa.Field(ge=0, le=1000.0)


# %% ++++++++++++++++++++++++++++ SOILWATER TABLES ++++++++++++++++++++++++++++

soilwater_tables = [
    "INIPRESSUREHEAD",
    "MXPONDTB",
    "SOILPROFILE",
    "SOILHYDRFUNC",
    "SOILTEXTURES",
    "INITSOILTEMP",
]


class INIPRESSUREHEAD(BaseTableModel):
    """Initial pressure head [cm, R] as a function of soil layer [1..N, I].

    Attributes:
        ZI: Series[int]: soil depth [-1.d5..0 cm, R].
        H: Series[float]: Initial soil water pressure head [-1.d10..1.d4 cm, R].
    """

    ZI: Series[float] = pa.Field(ge=-1.0e5, le=0.0)
    H: Series[float] = pa.Field(ge=-1.0e10, le=1.0e4)


class MXPONDTB(BaseTableModel):
    """minimum thickness for runoff PONDMXTB [0..1000 cm, R] as function of time

    Attributes:
        DATEPMX: Series[pa.DateTime]: Date of the ponding threshold for runoff.
        PONDMXTB: Series[float]: Minimum thickness for runoff.
    """

    DATEPMX: Series[pa.DateTime]
    PONDMXTB: Series[float]


class SOILPROFILE(BaseTableModel):
    """Vertical discretization of soil profile

    Attributes:
        ISUBLAY: Series[int]: number of sub layer, start with 1 at soil surface [1..MACP, I].
        ISOILLAY: Series[int]: number of soil physical layer, start with 1 at soil surface [1..MAHO, I].
        HSUBLAY: Series[float]: height of sub layer [0..1.d4 cm, R].
        HCOMP: Series[float]: height of compartments in the sub layer [0.0..1000.0 cm, R].
        NCOMP: Series[int]: number of compartments in the sub layer (Mind NCOMP = HSUBLAY/HCOMP) [1..MACP, I].
    """

    ISOILLAY: Series[int] = pa.Field(ge=1)
    ISUBLAY: Series[int] = pa.Field(ge=1)
    HSUBLAY: Series[float] = pa.Field(ge=0.0, le=1.0e4)
    HCOMP: Series[float] = pa.Field(ge=0.0, le=1.0e3)
    NCOMP: Series[int] = pa.Field(ge=1)


class SOILHYDRFUNC(BaseTableModel):
    """Soil hydraulic functions table.

        !!! warning
            ALFAW required only when the hysteresis option is set to 1 or 2. This column is set as optional column and (for now) is not checked.

    Attributes:
        ORES (Series[float]): Residual water content [0..1 cm3/cm3, R]
        OSAT (Series[float]): Saturated water content [0..1 cm3/cm3, R]
        ALFA (Series[float]): Parameter alfa of main drying curve [0.0001..100 /cm, R]
        NPAR (Series[float]): Parameter n [1.001..9 -, R]
        LEXP (Series[float]): Exponent in hydraulic conductivity function [-25..25 -, R]
        KSATFIT (Series[float]): Fitting parameter Ksat of hydraulic conductivity function [1.d-5..1d5 cm/d, R]
        H_ENPR (Series[float]): Air entry pressure head [-40.0..0.0 cm, R]
        KSATEXM (Series[float]): Measured hydraulic conductivity at saturated conditions [1.d-5..1d5 cm/d, R]
        BDENS (Series[float]): Dry soil bulk density [100..1d4 mg/cm3, R]
        ALFAW (Optional[Series[float]]): Alfa parameter of main wetting curve in case of hysteresis [0.0001..100 /cm, R]
    """

    ORES: Series[float] = pa.Field(ge=0.0, le=1.0)
    OSAT: Series[float] = pa.Field(ge=0.0, le=1.0)
    ALFA: Series[float] = pa.Field(ge=0.0001, le=100.0)
    NPAR: Series[float] = pa.Field(ge=1.001, le=9.0)
    LEXP: Series[float] = pa.Field(ge=-25.0, le=25.0)
    KSATFIT: Series[float] = pa.Field(ge=1.0e-5, le=1.0e5)
    H_ENPR: Series[float] = pa.Field(ge=-40.0, le=0.0)
    KSATEXM: Series[float] = pa.Field(ge=1.0e-5, le=1.0e5)
    BDENS: Series[float] = pa.Field(ge=100.0, le=1.0e4)
    ALFAW: Series[float] | None = pa.Field(ge=0.0001, le=100.0)


# %% ++++++++++++++++++++++++++++ HEAT FLOW TABLES ++++++++++++++++++++++++++++


class SOILTEXTURES(BaseTableModel):
    """Table for soil textures.

    Attributes:
        PSAND (float): Depth of soil layer [cm, R]
        PSILT (float): Sand content [g/g mineral parts, R]
        PCLAY (float): Clay content [g/g mineral parts, R]
        ORGMAT (float): Organic matter content [g/g dry soil, R]
    """

    PSAND: float
    PSILT: float
    PCLAY: float
    ORGMAT: float


class INITSOILTEMP(BaseTableModel):
    """Table for initial soil temperature.

    Attributes:
        ZH (float): Depth of soil layer [cm, R]
        TSOIL (float): Initial temperature [oC, R]
    """

    ZH: float = pa.Field(ge=-100000, le=0)
    TSOIL: float = pa.Field(ge=-50, le=50)


# %% ++++++++++++++++++++++++++++ BOUNDARY TABLES ++++++++++++++++++++++++++++

boundary_tables = [
    "GWLEVEL",
    "QBOT2",
    "HAQUIF",
    "QBOT4",
    "QTAB",
    "HBOT5",
    "DATET",
    "CSEEPARR",
    "INISSOIL",
    "MISC",
]


class GWLEVEL(BaseTableModel):
    """Table for groundwater levels over time.

    Attributes:
        DATE1 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        GWLEVEL (Series[float]): Groundwater level [-1e4..1e3, cm].
    """

    DATE1: Series[pa.DateTime]
    GWLEVEL: Series[float]


class QBOT2(BaseTableModel):
    """Table for bottom boundary flow over time.

    Attributes:
        DATE2 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        QBOT2 (Series[float]): Bottom boundary flow [-100..100, cm/d]. Upward flow is positive.
    """

    DATE2: Series[pa.DateTime]
    QBOT2: Series[float]


class HAQUIF(BaseTableModel):
    """Table for average hydraulic head in underling aquifer over time.

    Attributes:
        DATE3 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        HAQUIF (Series[float]): Average hydraulic head in underlying aquifer [-1e4..1e3, cm].
    """

    DATE3: Series[pa.DateTime]
    HAQUIF: Series[float]


class QBOT4(BaseTableModel):
    """Table for bottom boundary flow over time.

    Attributes:
        DATE4 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        QBOT4 (Series[float]): Bottom boundary flow [-100..100, cm/d]. Upward flow is positive.
    """

    DATE4: Series[pa.DateTime]
    QBOT4: Series[float]


class QTAB(BaseTableModel):
    """Table bottom boundary flux as function of groundwater level.

    Attributes:
        HTAB (Series[float]): Groundwater level, negative below soil surface [-1e4..0, cm]
        QTAB (Series[float]): Bottom boundary flux [-100..100, cm/d]. Upward flow is positive.
    """

    HTAB: Series[float]
    QTAB: Series[float]


class HBOT5(BaseTableModel):
    """Table for bottom compartment pressure head over time.

    Attributes:
        DATE6 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        HBOT5 (Series[float]): Bottom compartment pressure head [-1e10..1000, cm].
    """

    DATE5: Series[pa.DateTime]
    HBOT5: Series[float]


transport_tables = [
    "TBOT",
    "CSEEPARR",
]


class DATET(BaseTableModel):
    """Table for time.

    !!! Note:
        Deprecated from version 0.3.9. Use TBOT instead.

    Attributes:
        DATE7 (Series[pa.DateTime]): Date of the time.
        TIME (Series[float]): Time.
    """

    DATET: Series[pa.DateTime]
    TBOT: Series[float]

    def __post_init__(self):
        from warnings import warn

        warn(
            "The use of `DATET` is deprecated and will be removed in a later version. Please use `TBOT`.",
            FutureWarning,
            stacklevel=4,
        )


class TBOT(BaseTableModel):
    """Table for temperature bottom compartment over time.

    Attributes:
        DATE7 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        TBOT (Series[float]): Temperature bottom compartment [-50..50, °C].
    """

    DATET: Series[pa.DateTime]
    TBOT: Series[float]


class CSEEPARR(BaseTableModel):
    """Table for seepage.

    Attributes:
        DATE8 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        CSEEPARR (Series[float]): Seepage.
    """

    DATEC: Series[pa.DateTime]
    CSEEPARR: Series[float]


class INISSOIL(BaseTableModel):
    """Table for capillary rise.

    Attributes:
        DATE9 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        CML (Series[float]): Capillary rise.
    """

    ZC: Series[float]
    CML: Series[float]


class MISC(BaseTableModel):
    """Table for miscellaneous.

    Attributes:
        DATE10 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        MISC (Series[float]): Miscellaneous.
    """

    LDIS: Series[float]
    KF: Series[float]
    DECPOT: Series[float]
    FDEPTH: Series[float]


# %% ++++++++++++++++++++++++++++ DRAINAGE TABLES ++++++++++++++++++++++++++++

drainage_tables = [
    "DRNTB",
    "DRAINAGELEVELTOPPARAMS",
    "DATOWLTB1",
    "DATOWLTB2",
    "DATOWLTB3",
    "DATOWLTB4",
    "DATOWLTB5",
    "SECWATLVL",
    "MANSECWATLVL",
    "QWEIR",
    "QWEIRTB",
    "PRIWATLVL",
    "QDRNTB",
]


class DRNTB(BaseTableModel):
    """Drainage characteristics table.

    Attributes:
        LEV (Series[int]): Drainage level [1..5, -].
        SWDTYP (Series[int]): Type of drainage medium [1 = drain tube, 2 = open channel].
        L (Series[float]): Drain spacing [1..1e5, m].
        ZBOTDRE (Series[float]): Level of drainage medium bottom [-10000..0, cm].
        GWLINF (Series[float]): Groundwater level influence [-10000..200, cm].
        RDRAIN (Series[float]): Drainage resistance [10..1e5, d].
        RINFI (Series[float]): Infiltration resistance [0..1e5, d].
        RENTRY (Series[float]): Entry resistance [0..1000, d].
        REXIT (Series[float]): Exit resistance [0..1000, d].
        WIDTHR (Series[float]): Width of the drainage medium [0..1000, cm].
        TALUDR (Series[float]): Talud of the drainage medium [0..1000, cm].
    """

    LEV: Series[int] = pa.Field(ge=1, le=5)
    SWDTYP: Series[Literal[0, 1]]
    L: Series[float] = pa.Field(ge=1.0, le=100000.0)
    ZBOTDRE: Series[float]
    GWLINF: Series[float] = pa.Field(ge=-1000.0, le=0.0)
    RDRAIN: Series[float] = pa.Field(ge=1.0, le=100000.0)
    RINFI: Series[float] = pa.Field(ge=1.0, le=100000.0)
    RENTRY: Series[float] = pa.Field(ge=0.0, le=100.0)
    REXIT: Series[float] = pa.Field(ge=0.0, le=100.0)
    WIDTHR: Series[float] = pa.Field(ge=0.0, le=10000.0)
    TALUDR: Series[float] = pa.Field(ge=0.01, le=5.0)


class DRAINAGELEVELTOPPARAMS(BaseTableModel):
    """Drainage level with switches to adjust the top of each model discharge layer.

    Attributes:
        LEVEL (Series[Literal[1, 2, 3, 4, 5]]) : Drainage level.
        SWTOPDISLAY (Series[Literal[0, 1]]): Switch for each drainage level to
            distribute drainage flux vertically with a given position of the top
            of the model discharge layers [Y=1, N=0].
        ZTOPDISLAY (Series[float]): Array with depth of top of model discharge
            layer for each drain level [-10000.0..0.0, cm].
        FTOPDISLAY (Series[float]): Array with factor of top of model discharge
            layer for each drain level [0.0..1.0, -].
    """

    LEVEL: Series[Literal[1, 2, 3, 4, 5]]
    SWTOPDISLAY: Series[Literal[0, 1]]
    ZTOPDISLAY: Series[float] = pa.Field(ge=-10000.0, le=0.0)
    FTOPDISLAY: Series[float] = pa.Field(ge=0.0, le=1.0)


class DATOWLTB1(BaseTableModel):
    """Table to specify water level in open channel of drainage level 1.

    Attributes:
        DATOWL1 (Series[pa.DateTime]): Date [dd-mmm-yyyy], e.g. 12-jan-2000
        LEVEL1 (Series[float]): Surface water level, negative below soil surface
            [?..?, cm].
    """

    DATOWL1: Series[pa.DateTime]
    LEVEL1: Series[float]


class DATOWLTB2(BaseTableModel):
    """Table to specify water level in open channel of drainage level 2.

    Attributes:
        DATOWL2 (Series[pa.DateTime]): Date [dd-mmm-yyyy], e.g. 12-jan-2000
        LEVEL2 (Series[float]): Surface water level, negative below soil surface
            [?..?, cm].
    """

    DATOWL2: Series[pa.DateTime]
    LEVEL2: Series[float]


class DATOWLTB3(BaseTableModel):
    """Table to specify water level in open channel of drainage level 3.

    Attributes:
        DATOWL3 (Series[pa.DateTime]): Date [dd-mmm-yyyy], e.g. 12-jan-2000
        LEVEL3 (Series[float]): Surface water level, negative below soil surface
            [?..?, cm].
    """

    DATOWL3: Series[pa.DateTime]
    LEVEL3: Series[float]


class DATOWLTB4(BaseTableModel):
    """Table to specify water level in open channel of drainage level 4.

    Attributes:
        DATOWL4 (Series[pa.DateTime]): Date [dd-mmm-yyyy], e.g. 12-jan-2000
        LEVEL4 (Series[float]): Surface water level, negative below soil surface
            [?..?, cm].
    """

    DATOWL4: Series[pa.DateTime]
    LEVEL4: Series[float]


class DATOWLTB5(BaseTableModel):
    """Table to specify water level in open channel of drainage level 5.

    Attributes:
        DATOWL5 (Series[pa.DateTime]): Date [dd-mmm-yyyy], e.g. 12-jan-2000
        LEVEL5 (Series[float]): Surface water level, negative below soil surface
            [?..?, cm].
    """

    DATOWL5: Series[pa.DateTime]
    LEVEL5: Series[float]


class SECWATLVL(BaseTableModel):
    """Water level in secondary water course as function of date.

    Attributes:
        DATE2 (Series[DateTime]): Date of the water level [dd-mmm-yyyy] (e.g. 01-jan-2000).
        WLS (Series[float]): Water level in secondary water course [altcu-1000..altcu-0.01, cm]
    """

    DATE2: Series[pa.DateTime]
    WLS: Series[float]


class MANSECWATLVL(BaseTableModel):
    """Parameters for each management period.

    Attributes:
        IMPER_4B (Series[float]): Index of management period [1..nmper, -]
        IMPEND (Series[pa.DateTime]): Date that period ends [YYYY-MM-DD]
        SWMAN (Series[float]): Type of water management [1..2, -]

            * 1: fixed weir crest
            * 2: automatic weir

        WSCAP (Series[float]): Surface water supply capacity [0..100, cm/d]
        WLDIP (Series[float]): Allowed dip of surface water level before starting supply [0..100, cm]
        INTWL (Series[float]): Length of water-level adjustment period (SWMAN = 2 only) [1..31, d]
    """

    IMPER_4B: Series[float]
    IMPEND: Series[pa.DateTime]
    SWMAN: Series[float]
    WSCAP: Series[float]
    WLDIP: Series[float]
    INTWL: Series[float]


class QWEIR(BaseTableModel):
    """Table with parameters exponential weir discharge for all management periods.

    Attributes:
        IMPER_4C (Series[float]): Index of management period [1..nmper, -]
        HBWEIR (Series[float]): Weir crest [altcu-zbotdr..altcu+100, cm].
            Levels above soil surface are allowed, but simulated surface water
            levels should remain below 100 cm above soil surface.
            The crest must be higher than the deepest channel bottom of the
            secondary system (ZBOTDR(1 or 2).
            Represents the lowest possible weir position if swman = 2.
        ALPHAW (Series[float]): Alpha-coefficient of discharge formula [0.1..50.0, -]
        BETAW (Series[float]): Beta-coefficient of discharge formula [0.5..3.0, -]
    """

    IMPER_4C: Series[float]
    HBWEIR: Series[float]
    ALPHAW: Series[float]
    BETAW: Series[float]


class QWEIRTB(BaseTableModel):
    """Table with parameters of weir discharge for all management periods.

    Attributes:
        IMPER_4D (Series[float]): Index of management period [1..nmper, -]
        ITAB (Series[float]): Index per management period [1..10, -]
        HTAB (Series[float]): Surface water level [altcu-1000..altcu+100, cm].
            First value for each period = altcu + 100 cm).
        QTAB (Series[float]): Discharge [0..500, cm/d].
            Should go down to a value of zero at a level that is higher than
            the deepest channel bottom of secondary surface water system.
    """

    IMPER_4D: Series[float]
    IMPTAB: Series[float]
    HTAB: Series[float]
    QTAB: Series[float]


class PRIWATLVL(BaseTableModel):
    """Table with water level in the primary water course over time.

    Attributes:
        DATE1 (Series[pa.DateTime]): Date [dd-mmm-yyyy] (e.g. 01-jan-2000).
        WLP (Series[float]): Water level in the primary water course [altcu-1000..altcu-0.01, cm]
    """

    DATE1: Series[pa.DateTime]
    WLP: Series[float]


class QDRNTB(BaseTableModel):
    """Table relating the drainage flux to groundwater level.

    Attributes:
        QDRAIN (Series[float]): Drainage flux [-100..1000, cm/d]
        GWL (Series[float]): Groundwater level, negative below soil surface [-1000..10, cm]
    """

    QDRAIN: Series[float]
    GWL: Series[float]


# %% ++++++++++++++++++++++++++++ GENERAL SETTINGS TABLES ++++++++++++++++++++++++++++

general_settings_tables = ["OUTDATIN", "OUTDAT"]


class OUTDATIN(BaseTableModel):
    """OUTDATIN table

    Attributes:
        OUTDAT: Series[str]: Name of the output file.
    """

    OUTDATIN: Series[pa.DateTime]


class OUTDAT(BaseTableModel):
    """OUTDAT table

    Attributes:
        OUTDAT: Series[str]: Name of the output file.
    """

    OUTDAT: Series[pa.DateTime]
