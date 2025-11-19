# mypy: disable-error-code="call-overload, misc, type-arg"
# The type-arg here causes problems with passing the actual type to the alias
# Subsection. This however helps to type hinting, so it has to stay that way.
"""Crop settings and crop files for SWAP model.

Similar to the .dra or .swp files, the .crp file is a configuration file for the SWAP model.
The classes in this module represent distinct sections of the .crp file. The main class is the
`CropFile` class which holds the settings for the crop simulation.

SWAP has three modes for crop simulations which users define in the CROPROTATION table in the .swp file:

    * 1 - simple crop settings - use CropDevelopmentSettingsFixed
    * 2 - detailed, WOFOST general settings - use CropDevelopmentSettingsWOFOST
    * 3 - dynamic grass growth model - use CropDevelopmentSettingsGrass

For each choice, the .crp file will look different. Therefore, multiple classes
 are defined in this module to deal with those different settings.

Classes:
    Crop: Class for the crop section in the .swp file.
    CropFile: Class for the .crp file.
    Preparation: Class for the preparation settings.
    CropDevelopmentSettingsFixed: Class for the fixed crop development settings.
    CropDevelopmentSettingsWOFOST: Class for the crop development settings in WOFOST.
    CropDevelopmentSettingsGrass: Class for the grass crop development settings.
    OxygenStress: Class for the oxygen stress settings.
    DroughtStress: Class for the drought stress settings.
    SaltStress: Class for the salt stress settings.
    CompensateRWUStress: Class for the compensate root water uptake stress settings.
    Interception: Class for the interception settings.
    CO2Correction: Class for the CO2 correction settings.
    GrasslandManagement: Class for the grassland settings.
"""

from typing import (
    Any,
    Literal as _Literal,
)

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.irrigation import ScheduledIrrigation as _ScheduledIrrigation
from pyswap.components.tables import (
    AMAXTB,
    CFTB,
    CHTB,
    CROPROTATION,
    DMGRZTB,
    DMMOWDELAY,
    DMMOWTB,
    DTSMTB,
    FLTB,
    FOTB,
    FRTB,
    FSTB,
    GCTB,
    KYTB,
    LOSSGRZTB,
    LOSSMOWTB,
    LSDATB,
    LSDBTB,
    MRFTB,
    RDCTB,
    RDRRTB,
    RDRSTB,
    RDTB,
    RFSETB,
    RLWTB,
    SLATB,
    TMNFTB,
    TMPFTB,
    VERNTB,
    WRTB,
)
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import (
    Arrays as _Arrays,
    Decimal2f as _Decimal2f,
    IntList as _IntList,
    Subsection as _Subsection,
    Table as _Table,
)
from pyswap.core.valueranges import (
    UNITRANGE as _UNITRANGE,
    YEARRANGE as _YEARRANGE,
)
from pyswap.db.cropdb import CropVariety as _CropVariety
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    WOFOSTUpdateMixin as _WOFOSTUpdateMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "Crop",
    "CropFile",
    "_CropDevelopmentSettings",
    "CropDevelopmentSettingsFixed",
    "CropDevelopmentSettingsWOFOST",
    "CropDevelopmentSettingsGrass",
    "Interception",
    "OxygenStress",
    "DroughtStress",
    "SaltStress",
    "CompensateRWUStress",
    "Preparation",
    "GrasslandManagement",
    "CO2Correction",
    "AMAXTB",
    "CFTB",
    "CHTB",
    "CROPROTATION",
    "DMGRZTB",
    "DMMOWDELAY",
    "DMMOWTB",
    "DTSMTB",
    "FOTB",
    "FLTB",
    "FRTB",
    "FSTB",
    "GCTB",
    "KYTB",
    "LOSSMOWTB",
    "LOSSGRZTB",
    "LSDATB",
    "LSDBTB",
    "MRFTB",
    "RDCTB",
    "RDRRTB",
    "RDRSTB",
    "RDTB",
    "RFSETB",
    "RLWTB",
    "SLATB",
    "TMNFTB",
    "TMPFTB",
    "VERNTB",
    "WRTB",
]


class _CropDevelopmentSettings(
    _PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin, _WOFOSTUpdateMixin
):
    """Crop development settings.

    Private class. Documentation of variables is given in children classes.

    !!! note:

        CropDevelopmentSettings is a base class for the different crop
        development settings (type 1, 2 and 3). Crop parameters can be read from
        WOFOST database. Because some names of the same parameters are different
        between the wofost and swap templates, the alias parameter is used to
        rename the parameters in serialization to SWAP compatible .crp file.
        Currently it applies to TSUM1 and TSUM2.
    """

    # add in model config that additional attributes are allowed
    # model_config = _ConfigDict(
    #     extra="allow"
    # )

    wofost_variety: Any | None = _Field(default=None, exclude=True)

    swcf: _Literal[1, 2] | None = None
    cftb: _Table | None = None
    chtb: _Table | None = None
    albedo: _Decimal2f | None = _Field(default=None, **_UNITRANGE)
    rsc: _Decimal2f | None = _Field(default=None, ge=0.0, le=1.0e6)
    rsw: _Decimal2f | None = _Field(default=None, ge=0.0, le=1.0e6)
    tsum1: _Decimal2f | None = _Field(alias="tsumea", default=None, ge=0.0, le=1.0e4)
    tsum2: _Decimal2f | None = _Field(alias="tsumam", default=None, ge=0.0, le=1.0e4)
    tbase: _Decimal2f | None = _Field(default=None, ge=-10.0, le=30.0)
    kdif: _Decimal2f | None = _Field(default=None, ge=0.0, le=2.0)
    kdir: _Decimal2f | None = _Field(default=None, ge=0.0, le=2.0)
    swrd: _Literal[1, 2, 3] | None = None
    rdtb: _Arrays | None = None
    rdi: _Decimal2f | None = _Field(default=None, ge=0.0, le=1000.0)
    rri: _Decimal2f | None = _Field(default=None, ge=0.0, le=100.0)
    rdc: _Decimal2f | None = _Field(default=None, ge=0.0, le=1000.0)
    swdmi2rd: _Literal[0, 1] | None = None
    rlwtb: _Arrays | None = None
    wrtmax: _Decimal2f | None = _Field(default=None, ge=0.0, le=1.0e5)
    swrdc: _Literal[0, 1] | None = None
    rdctb: _Arrays | None = None


class CropDevelopmentSettingsWOFOST(_CropDevelopmentSettings):
    """Additional settings as defined for the WOFOST model.

    Attributes:
        wofost_variety (CropVariety): Crop variety settings.
        swcf (Literal[1, 2]): Use crop factor or crop height for simulation of evapotranspiration

            * 1 - Crop factor, when using ETref from meteo input file (`swetr=1`)
                or Penman-Monteith.
                    **Activates**: [`cftb`]
            * 2 - Crop height, when using Penman-Monteith with actual crop height,
                albedo and canopy resistance.
                    **Activates**: [`chtb`, `albedo`, `rsc`, `rsw`]

        cftb (Optional[CFTB]): Table with crop factors as a function of development stage.
        chtb (Optional[CHTB]): Table with crop height as a function of development stage.
        albedo (Optional[float]): Crop reflection coefficient [0..1.0, -].
        rsc (Optional[float]): Minimum canopy resistance [0..1e6, s/m].
        rsw (Optional[float]): Canopy resistance of intercepted water [0..1e6, s/m].
        idsl (Literal[0, 1, 2]): Switch for crop development.

            * 0 - Depends on temperature.
                    **Activates**: [`tsumea`, `tsumam`, `dtsmtb`]
            * 1 - Depends on temperature and daylength.
                    **Activates**: [`tsumea`, `tsumam`, `dtsmtb`, `dlo`, `dlc`]
            * 2 - Depends on temperature, daylength and vernalisation factor.
                    **Activates**: [`tsumea`, `tsumam`, `dtsmtb`, `dlo`, `dlc`,
                        `vernsat`, `vernbase`, `verndvs`, `verntb`]

        tsumea (Optional[float]): Temperature sum from emergence to anthesis [0..1e4, °C].
        tsumam (Optional[float]): Temperature sum from anthesis to maturity [1..1e4, °C].
        dtsmtb (Optional[DTSMTB]): Table with increase in temperature sum as function of daily average temperature.
        dlo (Optional[float]): Optimum day length for crop development [0..24, hr].
        dlc (Optional[float]): Minimum day length [0..24, hr].
        vernsat (Optional[float]): Saturated vernalisation requirement [0..100, days].
        vernbase (Optional[float]): Base vernalisation requirement [0..100, days].
        verndvs (Optional[float]): Critical development stage after which the effect of vernalisation is halted [0.0..0.3, -].
        verntb (Optional[VERNTB]): Table with rate of vernalisation as function of average air temperature.
        tdwi (float): Initial total crop dry weight [0..10000, kg/ha].
        laiem (float): Leaf area index at emergence [0..10, m2/m2].
        rgrlai (float): Maximum relative increase in LAI [0..1, m2/m2/d].
        spa (float): Specific pod area [0..1, ha/kg].
        ssa (float): Specific stem area [0..1, ha/kg].
        span (float): Life span under leaves under optimum conditions [0..366, d].
        slatb (SLATB): Table with specific leaf area as function of crop development stage.
        kdif (float): Extinction coefficient for diffuse visible light [0..2, -].
        kdir (float): Extinction coefficient for direct visible light [0..2, -].
        eff (float): Light use efficiency for real leaf [0..10, kg m2 s / (J ha hr)].
        amaxtb (AMAXTB): Table with maximum CO2 assimilation rate as function of development stage.
        tmpftb (TMPFTB): Table with the reduction factor of the maximum CO2
            assimilation as function of average day temperature.
        tmnftb (TMNFTB): Table with the reduction factor of the maximum CO2
            assimilation as function of minimum day temperature.
        cvl (float): Efficiency of conversion into leaves [0..1, kg/kg].
        cvo (float): Efficiency of conversion into storage organs [0..1, kg/kg].
        cvr (float): Efficiency of conversion into roots [0..1, kg/kg].
        cvs (float): Efficiency of conversion into stems [0..1, kg/kg].
        q10 (float): Increase in respiration rate with temperature [0..5, /10 degrees C].
        rml (float): Maintenance respiration rate of leaves [0..1, kgCH2O/kg/d].
        rmo (float): Maintenance respiration rate of storage organs [0..1, kgCH2O/kg/d].
        rmr (float): Maintenance respiration rate of roots [0..1, kgCH2O/kg/d].
        rms (float): Maintenance respiration rate of stems [0..1, kgCH2O/kg/d].
        rfsetb (RFSETB): Table with reduction factor of senescence as function of development stage.
        frtb (FRTB): Table with fraction of total dry matter increase partitioned
            to the roots as function of development stage.
        fltb (FLTB): Table with fraction of total above ground dry matter increase
            partitioned to the leaves as function of development stage.
        fstb (FSTB): Table with fraction of total above ground dry matter increase
            partitioned to the stems as function of development stage.
        fotb (FOTB): Table with fraction of total above ground dry matter increase
            partitioned to the storage organs as function of development stage.
        perdl (float): Maximum relative death rate of leaves due to water stress [0..3, /d].
        rdrrtb (RDRRTB): Table with relative death rates of roots as function of development stage.
        rdrstb (RDRSTB): Table with relative death rates of stems as function of development stage.
        swrdc (Literal[0, 1]): Switch for calculation of relative root density

            * 0: Root density is not modified
            * 1: Root density is modified based on root water extraction (default)

        rdctb (RDCTB): Table with root density as function of relative rooting depth.
        swrd (Literal[1, 2, 3]): Switch development of root growth.

            * 1 - Root growth depends on development stage.
                    **Activates**: [`rdtb`]
            * 2 - Root growth depends on maximum daily increase.
                    **Activates**: [`rdi`, `rri`, `rdc`, `swdmi2rd`]
            * 3 - Root growth depends on available root biomass.
                    **Activates**: [`rlwtb`, `wrtmax`]

        rdtb (Optional[RDTB]): Table with rooting depth as a function of development stage.
        rdi (Optional[float]): Initial rooting depth [0..1000, cm].
        rri (Optional[float]): Maximum daily increase in rooting depth [0..100, cm].
        rdc (Optional[float]): Maximum rooting depth of particular crop [0..1000, cm].
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth.

            * 0 - Rooting depth increase is related to availability assimilates for roots.
            * 1 - Rooting depth increase is related to relative dry matter increase.

        rlwtb (Optional[RLWTB]): Table with rooting depth as function of root weight.
        wrtmax (Optional[float]): Maximum root weight [0..1e5, kg DM/ha].
    """

    idsl: _Literal[0, 1, 2] | None = None
    dtsmtb: _Arrays | None = None
    dlo: float | None = _Field(default=None, ge=0.0, le=24.0)
    dlc: float | None = _Field(default=None, ge=0.0, le=24.0)
    vernsat: float | None = _Field(default=None, ge=0.0, le=100.0)
    vernbase: float | None = _Field(default=None, ge=0.0, le=100.0)
    verndvs: float | None = _Field(default=None, ge=0.0, le=0.3)
    verntb: _Arrays | None = None
    tdwi: float | None = _Field(default=None, ge=0.0, le=10_000)
    laiem: float | None = _Field(default=None, ge=0.0, le=10)
    rgrlai: float | None = _Field(default=None, **_UNITRANGE)
    spa: float | None = _Field(**_UNITRANGE, default=None)
    ssa: float | None = _Field(default=None, **_UNITRANGE)
    span: float | None = _Field(default=None, **_YEARRANGE)
    slatb: _Arrays | None = None
    eff: float | None = _Field(default=None, ge=0.0, le=10.0)
    amaxtb: _Arrays | None = None
    tmpftb: _Arrays | None = None
    tmnftb: _Arrays | None = None
    cvo: float | None = _Field(default=None, **_UNITRANGE)
    cvl: float | None = _Field(default=None, **_UNITRANGE)
    cvr: float | None = _Field(default=None, **_UNITRANGE)
    cvs: float | None = _Field(default=None, **_UNITRANGE)
    q10: float | None = _Field(default=None, ge=0.0, le=5.0)
    rml: float | None = _Field(default=None, **_UNITRANGE)
    rmo: float | None | None = _Field(**_UNITRANGE, default=None)
    rmr: float | None = _Field(default=None, **_UNITRANGE)
    rms: float | None = _Field(default=None, **_UNITRANGE)
    rfsetb: _Arrays | None = None
    frtb: _Arrays | None = None
    fltb: _Arrays | None = None
    fstb: _Arrays | None = None
    fotb: _Arrays | None = None
    perdl: float | None = _Field(default=None, ge=0.0, le=3.0)
    rdrrtb: _Arrays | None = None
    rdrstb: _Arrays | None = None


class CropDevelopmentSettingsFixed(_CropDevelopmentSettings):
    """Fixed crop development settings (Additionaly to CropDevelopmentSettings).

    Attributes:
        idev (Literal[1, 2]): Duration of crop growing period

            * 1 - Duration is fixed.
                    **Activates**: [`lcc`]
            * 2 - Duration is variable.
                    **Activates**: [`tsumea`, `tsumam`, `tbase`]

        lcc (Optional[int]): Duration of the crop growing period [1..366, day]
        tsumea (Optional[float]): Temperature sum from emergence to anthesis [0..1e4 degrees C].
        tsumam (Optional[float]): Temperature sum from anthesis to maturity [1..1e4 degrees C].
        tbase (Optional[float]): Start value of temperature sum [-10..30 degrees C].
        kdif (float): Extinction coefficient for diffuse visible light [0..2 -].
        kdir (float): Extinction coefficient for direct visible light [0..2 -].
        swgc (Literal[1, 2]): Choose between Leaf Area Index or Soil Cover Fraction

            * 1 - Leaf Area Index.
                    **Activates**: [`gctb`]
            * 2 - Soil Cover Fraction.
                    **Activates**: [`gctb`]

        gctb (Optional[GCTB]): Soil Cover Fraction or Leaf Area Index as a function of development stage
        swcf (Literal[1, 2]): Use crop factor or crop height for simulation of evapotranspiration

            * 1 - Crop factor, when using ETref from meteo input file (`swetr=1`)
                or Penman-Monteith.
                    **Activates**: [`cftb`]
            * 2 - Crop height, when using Penman-Monteith with actual crop height,
                albedo and canopy resistance.
                    **Activates**: [`chtb`, `albedo`, `rsc`, `rsw`]

        cftb (Optional[CFTB]): Table with crop factors as a function of development stage.
        chtb (Optional[CHTB]): Table with crop height as a function of development stage.
        albedo (Optional[float): Crop reflection coefficient [0..1.0, -].
        rsc (Optional[float]): Minimum canopy resistance [0..1e6, s/m].
        rsw (Optional[float]): Canopy resistance of intercepted water [0..1e6, s/m].
        rdctb (RDCTB): Table with root density as function of relative rooting depth.
        swrdc (Literal[0, 1]): Switch for calculation of relative root density

            * 0: Root density is not modified
            * 1: Root density is modified based on root water extraction (default)

        swrd (Literal[1, 2, 3]): Switch development of root growth.

            * 1 - Root growth depends on development stage.
                    **Activates**: [`rdtb`]
            * 2 - Root growth depends on maximum daily increase.
                    **Activates**: [`rdi`, `rri`, `rdc`, `swdmi2rd`]
            * 3 - Root growth depends on available root biomass.
                    **Activates**: [`rlwtb`, `wrtmax`]

        rdtb (Optional[RDTB]): Table with rooting depth as a function of development stage.
        rdi (Optional[float]): Initial rooting depth [0..1000, cm].
        rri (Optional[float]): Maximum daily increase in rooting depth [0..100, cm].
        rdc (Optional[float]): Maximum rooting depth of particular crop [0..1000, cm].
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth.

            * 0 - Rooting depth increase is related to availability assimilates for roots.
            * 1 - Rooting depth increase is related to relative dry matter increase.

        rlwtb (Optional[RLWTB]): Table with rooting depth as function of root weight.
        wrtmax (Optional[float]): Maximum root weight [0..1e5, kg DM/ha].
        kytb (KYTB): Table with yield response factor as function of development stage.
    """

    idev: _Literal[1, 2] | None = None
    lcc: int | None = _Field(default=None, **_YEARRANGE)
    swgc: _Literal[1, 2] | None = None
    gctb: _Arrays | None = None
    kytb: _Arrays | None = None


class CropDevelopmentSettingsGrass(CropDevelopmentSettingsWOFOST):
    """Crop development settings specific to grass growth.

    Attributes:
        swcf (Literal[1, 2]): Use crop factor or crop height for simulation of evapotranspiration

            * 1 - Crop factor, when using ETref from meteo input file (`swetr=1`)
                or Penman-Monteith.
                    **Activates**: [`cftb`]
            * 2 - Crop height, when using Penman-Monteith with actual crop height,
                albedo and canopy resistance.
                    **Activates**: [`chtb`, `albedo`, `rsc`, `rsw`]

        cftb (Optional[CFTB]): Table with crop factors as a function of day number.
        chtb (Optional[CHTB]): Table with crop height as a function of day number.
        albedo (Optional[float]): Crop reflection coefficient [0..1.0, -].
        rsc (Optional[float]): Minimum canopy resistance [0..1e6, s/m].
        rsw (Optional[float]): Canopy resistance of intercepted water [0..1e6, s/m].
        tdwi (float): Initial total crop dry weight [0..10000, kg/ha].
        laiem (float): Leaf area index at emergence [0..10, m2/m2].
        rgrlai (float): Maximum relative increase in LAI [0..1, m2/m2/d].
        swtsum (Literal[0, 1, 2]): Select either sum air temperatures or soil temperature at particular depth

            * 0 - No delay of start grass growth
            * 1 - Start of grass growth based on sum air temperatures > 200 degree C
            * 2 - Start of grass growth based on soil temperature at particular depth.
                    **Activates**: [`tsumtemp`, `tsumdepth`, `tsumtime`]

        tsumtemp (Optional[float]): Specific stem area [0..1, ha/kg]
        tsumdepth (Optional[float]): Life span under leaves under optimum conditions [0..366, d]
        tsumtime (Optional[float]): Lower threshold temperature for ageing of leaves [-10..30. °C]
        ssa (float): Specific stem area [0..1, ha/kg].
        span (float): Life span under leaves under optimum conditions [0..366, d].
        slatb (SLATB): Table with specific leaf area as function of crop development stage.
        kdif (float): Extinction coefficient for diffuse visible light [0..2, -].
        kdir (float): Extinction coefficient for direct visible light [0..2, -].
        eff (float): Light use efficiency for real leaf [0..10, kg m2 s / (J ha hr)].
        amaxtb (AMAXTB): Table with maximum CO2 assimilation rate as function of development stage.
        tmpftb (TMPFTB): Table with the reduction factor of the maximum CO2
            assimilation as function of average day temperature.
        tmnftb (TMNFTB): Table with the reduction factor of the maximum CO2
            assimilation as function of minimum day temperature.
        cvl (float): Efficiency of conversion into leaves [0..1, kg/kg].
        cvr (float): Efficiency of conversion into roots [0..1, kg/kg].
        cvs (float): Efficiency of conversion into stems [0..1, kg/kg].
        q10 (float): Increase in respiration rate with temperature [0..5, /10 degrees C].
        rml (float): Maintenance respiration rate of leaves [0..1, kgCH2O/kg/d].
        rmr (float): Maintenance respiration rate of roots [0..1, kgCH2O/kg/d].
        rms (float): Maintenance respiration rate of stems [0..1, kgCH2O/kg/d].
        rfsetb (RFSETB): Table with reduction factor of senescence as function of development stage.
        frtb (FRTB): Table with fraction of total dry matter increase partitioned
            to the roots as function of development stage.
        fltb (FLTB): Table with fraction of total above ground dry matter increase
            partitioned to the leaves as function of development stage.
        fstb (FSTB): Table with fraction of total above ground dry matter increase
            partitioned to the stems as function of development stage.
        perdl (float): Maximum relative death rate of leaves due to water stress [0..3, /d].
        rdrrtb (RDRRTB): Table with relative death rates of roots as function of development stage.
        rdrstb (RDRSTB): Table with relative death rates of stems as function of development stage.
        rdctb (RDCTB): Table with root density as function of relative rooting depth.
        swrdc (Literal[0, 1]): Switch for calculation of relative root density

            * 0: Root density is not modified
            * 1: Root density is modified based on root water extraction (default)

        swrd (Literal[1, 2, 3]): Switch development of root growth.

            * 1 - Root growth depends on development stage.
                    **Activates**: [`rdtb`]
            * 2 - Root growth depends on maximum daily increase.
                    **Activates**: [`rdi`, `rri`, `rdc`, `swdmi2rd`]
            * 3 - Root growth depends on available root biomass.
                    **Activates**: [`rlwtb`, `wrtmax`]

        rdtb (Optional[RDTB]): Table with rooting depth as a function of development stage.
        rdi (Optional[float]): Initial rooting depth [0..1000, cm].
        rri (Optional[float]): Maximum daily increase in rooting depth [0..100, cm].
        rdc (Optional[float]): Maximum rooting depth of particular crop [0..1000, cm].
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth.

            * 0 - Rooting depth increase is related to availability assimilates for roots.
            * 1 - Rooting depth increase is related to relative dry matter increase.

        rlwtb (Optional[RLWTB]): Table with rooting depth as function of root weight.
        wrtmax (Optional[float]): Maximum root weight [0..1e5, kg DM/ha].
    """

    swtsum: _Literal[0, 1, 2] | None = None
    tsumtemp: float | None = None
    tsumdepth: float | None = None
    tsumtime: float | None = None


class OxygenStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Oxygen stress settings for .crp file.

    Attributes:
        swoxygen (Literal[0, 1, 2]): Switch for oxygen stress:

            * 0 - No oxygen stress.
            * 1 - Oxygen stress according to Feddes et al. (1978).
                    **Activates**: [`hlim1`, `hlim2u`, `hlim2l`]
            * 2 - Oxygen stress according to Bartholomeus et al. (2008)
                    **Activates**: [`swoxygentype`]

        hlim1 (Optional[float]): No water extraction at higher pressure heads [-100..100, cm]
        hlim2u (Optional[float]): H below which optimum water extraction starts for top layer [-1000..100, cm]
        hlim2l (Optional[float]): H below which optimum water extraction starts for sub layer [-1000..100, cm]
        swoxygentype (Optional[Literal[1, 2]]): Switch for using physical processes or
            reproduction functions to calculate oxygen stress:

            * 1 - Physical processes.
                    **Activates**: [`q10_microbial`, `specific_resp_humus`, `srl`, `swrootradius`]
            * 2 - reproduction functions

        q10_microbial (Optional[float]): Relative increase in microbial respiration at
            temperature increase of 10 °C [1.0..4.0, -]
        specific_resp_humus (Optional[float]): Respiration rate of humus at 25 °C [0.0..1.0, kg O2 °C / (kg d)]
        srl (Optional[float]): Specific root length [0..1e10, m/kg]
        swrootradius (Optional[Literal[1, 2]]): Switch for calculation of root radius:

            * 1 - Calculate root radius.
                    **Activates**: [`dry_mat_cont_roots`, `air_filled_root_por`, `spec_weight_root_tissue`, `var_a`]
            * 2 - Root radius given in an input file.
                    **Activates**: [`root_radiuso2`]

        dry_mat_cont_roots (Optional[float]): Dry matter content of roots [0..1, -]
        air_filled_root_por (Optional[float]): Air filled root porosity [0..1, -]
        spec_weight_root_tissue (Optional[float]): Specific weight of non-airfilled root tissue [0.0..1e5, kg/m3]
        var_a (Optional[float]): Variance of root radius [0.0..1.0, -]
        root_radiuso2 (Optional[float]): Root radius [1e-6..0.1, cm]
        swwrtnonox (Literal[0, 1]): Switch for checking aerobic conditions in
            root zone to stop root(zone) development:

            * 1 - Don't check for aerobic conditions.
            * 2 - Check for aerobic conditions.
                    **Activates**: [`aeratecrit`]

        aeratecrit (Optional[float]): Threshold to stop root extension in case of oxygenstress; 0.0 maximum oxygen stress
        q10_root (Optional[float]): Relative increase in root respiration at temperature increase of 10 °C [DEPRECATED]
        f_senes (Optional[float]): Reduction factor for senescence, used for maintenance respiration [DEPRECATED]
        c_mroot (Optional[float]): Maintenance coefficient of root [DEPRECATED]
        mrftb (Optional[MRFTB]): Ratio root total respiration / maintenance respiration as a function of development stage [DEPRECATED]
        wrtb (Optional[WRTB]): List dry weight of roots at soil surface as a function of development stage [DEPRECATED]

    """

    # TODO: Find a way to validate the parameters that are required when the
    # croptype=1 and swoxygen=2 (currently I cannot access the croptype parameter)
    # >> move it to the Model class validation at the end, when all the params are available

    swoxygen: _Literal[0, 1, 2] | None = None
    swwrtnonox: _Literal[0, 1] | None = None
    swoxygentype: _Literal[1, 2] | None = None
    aeratecrit: float | None = _Field(default=None, ge=0.0001, le=1.0)
    hlim1: float | None = _Field(default=None, ge=-100.0, le=100.0)
    hlim2u: float | None = _Field(default=None, ge=-1000.0, le=100.0)
    hlim2l: float | None = _Field(default=None, ge=-1000.0, le=100.0)
    q10_microbial: float | None = _Field(default=None, ge=1.0, le=4.0)
    specific_resp_humus: float | None = _Field(default=None, **_UNITRANGE)
    srl: float | None = _Field(default=None, ge=0.0, le=1.0e10)
    swrootradius: _Literal[1, 2] | None = None
    dry_mat_cont_roots: float | None = _Field(default=None, **_UNITRANGE)
    air_filled_root_por: float | None = _Field(default=None, **_UNITRANGE)
    spec_weight_root_tissue: float | None = _Field(default=None, ge=0.0, le=1.0e5)
    var_a: float | None = _Field(default=None, **_UNITRANGE)
    root_radiuso2: float | None = _Field(default=None, ge=1.0e-6, le=0.1)
    # Variables below are not specified in the documentation, remove?
    q10_root: float | None = _Field(default=None, ge=1.0, le=4.0)
    f_senes: float | None = _Field(default=None, **_UNITRANGE)
    c_mroot: float | None = _Field(default=None, **_UNITRANGE)
    mrftb: _Arrays | None = None
    wrtb: _Arrays | None = None


class DroughtStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Drought stress settings for .crp file.

    Attributes:
        swdrought (Literal[1, 2]): Switch for drought stress

            * 1 - Drought stress according to Feddes et al. (1978).
                    **Activates**: [`hlim3h`, `hlim3l`, `hlim4`, `adcrh`, `adcrl`]
            * 2 - rought stress according to De Jong van Lier et al. (2008)
                    **Activates**: [`wiltpoint`, `kstem`, `rxylem`, `rootradius`, `kroot`,
                        `rootcoefa`, `swhydrlift`, `rooteff`, `stephr`, `criterhr`, `taccur`]

        hlim3h (Optional[float]): Pressure head below which water uptake reduction starts at high Tpot [-1e4..100, cm]
        hlim3l (Optional[float]): Pressure head below which water uptake reduction starts at low Tpot [-1e4..100, cm]
        hlim4 (Optional[float]): No water extraction at lower soil water pressure heads [-2e4..100, cm]
        adcrh (Optional[float]): Level of high atmospheric demand, corresponding to `hlim3h` [0..5, cm/d]
        adcrl (Optional[float]): Level of low atmospheric demand, corresponding to `hlim3l` [0..5, cm/d]
        wiltpoint (Optional[float]): Minimum pressure head in leaves [-1e8..1e2, cm]
        kstem (Optional[float]): Hydraulic conductance between leaf and root xylem [1e-10..10, /d]
        rxylem (Optional[float]): Xylem radius [1e-4..1, cm]
        rootradius (Optional[float]): Root radius [1e-4..1, cm]
        kroot (Optional[float]): Radial hydraulic conductivity of root tissue [1e-10..1e10, cm/d]
        rootcoefa (Optional[float]): Defines relative distance between roots at which mean soil water content occurs [0..1, -]
        swhydrlift (Optional[Literal[0, 1]]): Switch for possibility hydraulic lift in root system:

            * 1 - Yes
            * 2 - No

        rooteff (Optional[float]): Root system efficiency factor [0..1, -]
        stephr (Optional[float]): Step between values of hroot and hxylem in iteration cycle [0..10, cm]
        criterhr (Optional[float]): Maximum difference of Hroot between iterations; convergence criterium [0..10, cm]
        taccur (Optional[float]): Maximum absolute difference between simulated and calculated potential transpiration rate [1e-5..1e-2, cm/d]
    """

    swdrought: _Literal[1, 2] | None = None
    hlim3h: float | None = _Field(default=None, ge=-1.0e4, le=100.0)
    hlim3l: float | None = _Field(default=None, ge=-1.0e4, le=100.0)
    hlim4: float | None = _Field(default=None, ge=-1.6e4, le=100.0)
    adcrh: float | None = _Field(default=None, ge=0.0, le=5.0)
    adcrl: float | None = _Field(default=None, ge=0.0, le=5.0)
    wiltpoint: float | None = _Field(default=None, ge=-1.0e8, le=-1.0e2)
    kstem: float | None = _Field(default=None, ge=1.0e-10, le=10.0)
    rxylem: float | None = _Field(default=None, ge=1.0e-4, le=1.0)
    rootradius: float | None = _Field(default=None, ge=1.0e-4, le=1.0)
    kroot: float | None = _Field(default=None, ge=1.0e-10, le=1.0e10)
    rootcoefa: float | None = _Field(default=None, **_UNITRANGE)
    swhydrlift: _Literal[0, 1] | None = None
    rooteff: float | None = _Field(default=None, **_UNITRANGE)
    stephr: float | None = _Field(default=None, ge=0.0, le=10.0)
    criterhr: float | None = _Field(default=None, ge=0.0, le=10.0)
    taccur: float | None = _Field(default=None, ge=1.0e-5, le=1.0e-2)


class SaltStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Salt stress settings for .crp file.

    Attributes:
        swsalinity (Literal[0, 1, 2]): Switch for salt stress

            * 0 - No salt stress
            * 1 - Maas and Hoffman reduction function.
                    **Activates**: [`saltmax`, `saltslope`]
            * 2 - Use osmotic head.
                    **Activates**: [`salthead`]

        saltmax (Optional[float]): Threshold salt concentration in soil water [0..100 mg/cm3]
        saltslope (Optional[float]): Decline of root water uptake above threshold [0..1, cm3/mg]
        salthead (Optional[float]): Conversion factor salt concentration (mg/cm3) into osmotic head (cm) [0..1000, cm/(mg/cm3)]
    """

    swsalinity: _Literal[0, 1, 2] | None = None
    saltmax: float | None = _Field(default=None, ge=0.0, le=100.0)
    saltslope: float | None = _Field(default=None, **_UNITRANGE)
    salthead: float | None = _Field(default=None, ge=0.0, le=1000.0)


class CompensateRWUStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Compensate root water uptake stress settings for .crp file.

    Attributes:
        swcompensate (Literal[0, 1, 2]): Switch for compensate root water uptake stress

            * 0 - No compensation
            * 1 - Compensation according to Jarvis (1989)
            * 2 - Compensation according to Walsum (2019)

        swstressor (Literal[1, 2, 3, 4, 5]): Switch for stressor

            * 1 - Compensation of all stressors
            * 2 - Compensation of drought stress
            * 3 - Compensation of oxygen stress
            * 4 - Compensation of salinity stress
            * 5 - Compensation of frost stress

        alphacrit (float): Critical stress index for compensation of root water uptake
        dcritrtz (float): Threshold of rootzone thickness after which compensation occurs
    """

    swcompensate: _Literal[0, 1, 2] | None = None
    swstressor: _Literal[1, 2, 3, 4, 5] | None = None
    alphacrit: float | None = _Field(default=None, ge=0.2, le=1.0)
    dcritrtz: float | None = _Field(default=None, ge=0.02, le=100.0)


class Interception(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Interception settings for .crp file.

    Attributes:
        swinter (Literal[0, 1, 2]): Switch for rainfall interception method

            * 0 - No interception.
            * 1 - Agricultural crops (Von Hoyningen-Hune and Braden).
                    **Activates**: [`cofab`]
            * 2 - Trees and forests (Gash).
                    **Activates**: [`intertb`]

        cofab (Optional[float]): Interception coefficient, corresponding to maximum interception amount
        intertb (Optional[INTERTB]): Table with free throughfall coefficient, stemflow coefficient
            canopy storage coefficient, average rainfall intensity and average evaporation
             intensity during rainfall from a wet canopy as function of time.
    """

    swinter: _Literal[0, 1, 2] | None = None
    cofab: float | None = _Field(default=None, **_UNITRANGE)
    intertb: _Table | None = None


class CO2Correction(
    _PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin, _WOFOSTUpdateMixin
):
    """CO2 correction settings for WOFOST-type .crp file.

    Attributes:
        swco2 (Literal[0, 1]): Switch for assimilation correction due to CO2 impact

            * 0 - No CO2 assimilation correction.
            * 1 - CO2 assimilation correction.
                    **Activates**: [`co2amaxtb`, `co2efftb`, `co2tratb`]

        co2amaxtb (Optional[CO2AMAXTB]): Table with correction of photosynthesis as a
            function of atmospheric CO2 concentration.
        co2efftb (Optional[CO2EFFTB]): Table with correction of radiation use efficiency as
            a function of atmospheric CO2 concentration
        co2tratb (Optional[CO2TRATB]): Table with correction of transpiration as a
            function of atmospheric CO2 concentration.
    """

    _validation: bool = _PrivateAttr(default=False)
    wofost_variety: _CropVariety | None = _Field(default=None, exclude=True)

    swco2: _Literal[0, 1] | None = None
    co2amaxtb: _Arrays | None = None
    co2efftb: _Arrays | None = None
    co2tratb: _Arrays | None = None


class Preparation(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Preparation, sowing and germination settings for .crp file.

    Attributes:
        swprep (Literal[0, 1]): Switch for preparation.

            * 1 - No preparation.
            * 2 - Preparation before start of crop growth.
                    **Activates**: [`zprep`, `hprep`, `maxprepdelay`]

        zprep (Optional[float]): Z-level for monitoring work-ability for the crop [-100..0, cm].
        hprep (Optional[float]): Maximum pressure head during preparation [-200..0, cm].
        maxprepdelay (Optional[int]): Maximum delay of preparation from start of growing season [1..366, d].
        swsow (Literal[0, 1]): Switch for sowing

            * 0 - No sowing
            * 1 - Sowing before start of crop growth.
                    **Activates**: [`zsow`, `hsow`, `ztempsow`, `tempsow`, `maxsowdelay`]

        zsow (Optional[float]): Z-level for monitoring work-ability for the crop [-100..0, cm].
        hsow (Optional[float]): Maximum pressure head during sowing [-200..0, cm].
        ztempsow (Optional[float]): Z-level for monitoring temperature for sowing [-100..0, cm].
        tempsow (Optional[float]): Soil temperature needed for sowing [0..30, °C].
        maxsowdelay (Optional[int]): Maximum delay of sowing from start of growing season [1..366, d].
        swgerm (Literal[0, 1, 2]): Switch for germination.

            * 0 - No germination.
            * 1 - Germination with temperature sum.
                    **Activates**: [`tsumemeopt`, `tbasem`, `teffmx`]
            * 2 - Germination with temperature sum and water potential.
                    **Activates**: [`tsumemeopt`, `tbasem`, `teffmx`, `hdrygerm`, `hwetgerm`, `zgerm`, `agerm`]

        tsumemeopt (Optional[float]): Temperature sum needed for crop emergence [0..1000, °C]
        tbasem (Optional[float]): Minimum temperature, used for germination trajectory [0..40, °C].
        teffmx (Optional[float]): Maximum temperature, used for germination trajectory [0..40, °C].
        hdrygerm (Optional[float]): Pressure head rootzone for dry germination trajectory [-1000..-0.01, cm].
        hwetgerm (Optional[float]): Pressure head rootzone for wet germination trajectory [-1000..-0.01, cm].
        zgerm (Optional[float]): Z-level for monitoring average pressure head for germination [-100..0, cm].
        agerm (Optional[float]): A-coefficient Eq. 24/25 Feddes & Van Wijk (1988) [0..1000, -].
        swharv (Literal[0, 1]): Switch for harvest.

            * 0 - Timing of harvest depends on end of growing period.
            * 1 - Timing of harvest depends on development stage.
                    **Activates**: [`dvsend`]

        dvsend (Optional[float]): Development stage at harvest [0..3 -].
    """

    swprep: _Literal[0, 1] | None = _Field(default=None)
    swsow: _Literal[0, 1] | None = None
    swgerm: _Literal[0, 1, 2] | None = None
    swharv: _Literal[0, 1] | None = None
    dvsend: float | None = _Field(default=None, ge=0.0, le=3.0)
    zprep: float | None = _Field(default=None, ge=-100.0, le=0.0)
    hprep: float | None = _Field(default=None, ge=-200.0, le=0.0)
    maxprepdelay: int | None = _Field(default=None, ge=1, le=366)
    zsow: float | None = _Field(default=None, ge=-100.0, le=0.0)
    hsow: float | None = _Field(default=None, ge=-200.0, le=0.0)
    ztempsow: float | None = _Field(default=None, ge=-100.0, le=0.0)
    tempsow: float | None = _Field(default=None, ge=0.0, le=30.0)
    maxsowdelay: int | None = _Field(default=None, ge=1, le=366)
    tsumemeopt: float | None = _Field(default=None, ge=0.0, le=1000.0)
    tbasem: float | None = _Field(default=None, ge=0.0, le=1000.0)
    teffmx: float | None = _Field(default=None, ge=0.0, le=1000.0)
    hdrygerm: float | None = _Field(default=None, ge=-1000.0, le=1000.0)
    hwetgerm: float | None = _Field(default=None, ge=-100.0, le=1000.0)
    zgerm: float | None = _Field(default=None, ge=-100.0, le=1000.0)
    agerm: float | None = _Field(default=None, ge=0.0, le=1000.0)


class GrasslandManagement(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Settings specific to the dynamic grass growth module.

    Attributes:
        seqgrazmow (IntList): sequence of periods with different practices within calender year. Available options:

            * 1 - Grazing.
                    **Activates**: [`swdmgrz`, `maxdaygrz`, `swlossgrz`, `tagprest`, `lsdatb`, `lsdbtb`]
            * 2 - Mowing.
                    **Activates**: [`swdmmow`, `maxdaymow`, `swlossmow`, `mowrest`, `dmmowdelay`]
            * 3 - Grazing with dewooling.
                    **Activates**: [`swdmgrz`, `maxdaygrz`, `swlossgrz`, `dewrest`, `lsdatb`, `lsdbtb`]

        swharvest (Literal[1, 2]): Switch for timing harvest, either for mowing or grazing

            * 1 - Use dry matter threshold.
                    **Activates**: [`swdmgrz`]
            * 2 - Use fixed dates.
                    **Activates**: [`dateharvest`]

        dateharvest (Optional[DateList]): Harvest dates (maximum 999)
        swdmgrz (Optional[Literal[1, 2]]): Switch for dry matter threshold to trigger harvest by grazing

            * 1 - Use fixed threshold.
                    **Activates**: [`dmgrazing`]
            * 2 - Use flexible threshold.
                    **Activates**: [`dmgrztb`]

        dmgrazing (Optional[float]): Minimum dry matter amount for cattle to enter the field [0..1d6, kg DM/ha]
        dmgrztb (Optional[DMGRZTB]): Table with threshold of above ground dry matter to
            trigger grazing as function of daynumber.
        maxdaygrz (Optional[int]): Maximum growing period after harvest [1..366, -]
        swlossgrz (Optional[Literal[0, 1]]): [UNCERTAIN WHAT THIS DOES] Switch for losses
            due to insufficient pressure head during grazing

            * 0 - No loss.
            * 1 - Losses due to treading.

        tagprest (Optional[float]): Minimum amount of above ground DM after grazing [0..1d6, kg DM/ha]
        dewrest (Optional[float]): Remaining yield above ground after dewooling event [0..1d6, kg DM/ha]
        lsdatb (Optional[LSDATB]): Table with actual livestock density of each grazing period.
        lsdbtb (Optional[LSDBTB]): Table with relation between livestock density, number of
            grazing days and dry matter uptake.
        swdmmow (Optional[int]): Switch for dry matter threshold to trigger harvest by mowing:

            * 1 - Use fixed threshold.
                    **Activates**: [`dmharvest`, `daylastharvest`, `dmlastharvest`]
            * 2 - Use flexible threshold.
                    **Activates**: [`dmmowtb`]

        dmharvest (Optional[float]): Threshold of above ground dry matter to trigger mowing [0..1d6, kg DM/ha]
        daylastharvest (Optional[int]): Last calendar day on which mowing may occur [1..366, -]
        dmlastharvest (Optional[float]): Minimum above ground dry matter for mowing on last date [0..1d6, kg DM/ha]
        dmmowtb (Optional[DMMOWTB]): Table with dry matter mowing threshold
        maxdaymow (Optional[int]): Maximum growing period after harvest [1..366, d]
        swlossmow (Optional[int]): [UNCERTAIN WHAT THIS DOES] Switch for losses due to
            insufficient pressure head during mowing:

            * 0 - No loss
            * 1 - Losses due to treading.

        mowrest (Optional[float]): Remaining yield above ground after mowing event [0..1d6 kg DM/ha, R]
        dmmowdelay (Optional[DMMOWDELAY]): Relation between dry matter harvest [0..1d6 kg/ha, R] and days of delay in regrowth [0..366 d, I] after mowing
        swpotrelmf (int): Switch for calculation of potential yield

            * 1 - Theoretical potential yield.
            * 2 - Attainable yield.
                    **Activates**: [`relmf`]

        relmf (Optional[float]): Relative management factor to reduce theoretical potential yield to attainable yield [0..1, -]
    """

    seqgrazmow: _IntList | None = None
    swharvest: _Literal[1, 2] | None = None
    dateharvest: _Arrays | None = None
    swdmgrz: _Literal[1, 2] | None = None
    dmgrazing: _Decimal2f | None = None
    dmgrztb: _Arrays | None = None
    maxdaygrz: int | None = None
    swlossgrz: _Literal[0, 1] | None = None
    tagprest: _Decimal2f | None = None
    dewrest: _Decimal2f | None = None
    lsdatb: _Table | None = None
    lsdbtb: _Table | None = None
    swdmmow: int | None = None
    dmharvest: _Decimal2f | None = None
    daylastharvest: int | None = None
    dmlastharvest: _Decimal2f | None = None
    dmmowtb: _Arrays | None = None
    maxdaymow: int | None = None
    swlossmow: int | None = None
    mowrest: _Decimal2f | None = None
    dmmowdelay: _Table | None = None
    swpotrelmf: int | None = None
    relmf: _Decimal2f | None = None


class CropFile(_PySWAPBaseModel, _FileMixin, _SerializableMixin):
    """Main class for the .crp file.

    This class collects all the settings for the crop file. Currently the types of the
    attributes are set to Any because the validation is not yet implemented.

    Attributes:
        name (str): Name of the crop.
        prep (Preparation): Preparation settings
        cropdev_settings (CropDevelopmentSettings): Crop development settings
        oxygenstress (OxygenStress): Oxygen stress settings
        droughtstress (DroughtStress): Drought stress settings
        saltstress (SaltStress): Salt stress settings
        compensaterwu (CompensateRWUStress): Compensate root water uptake stress settings
        interception (Interception): Interception settings
        scheduledirrigation (ScheduledIrrigation): Scheduled irrigation settings
        grassland_management (GrasslandManagement): Grassland management settings
    """

    _extension: bool = _PrivateAttr(default="crp")

    name: str = _Field(exclude=True)
    prep: _Subsection[Preparation] | None = None
    cropdev_settings: (
        _Subsection[
            CropDevelopmentSettingsFixed
            | CropDevelopmentSettingsWOFOST
            | CropDevelopmentSettingsGrass
        ]
        | None
    ) = None
    oxygenstress: _Subsection[OxygenStress] | None = None
    droughtstress: _Subsection[DroughtStress] | None = None
    saltstress: _Subsection[SaltStress] | None = SaltStress(swsalinity=0)
    compensaterwu: _Subsection[CompensateRWUStress] | None = CompensateRWUStress(
        swcompensate=0
    )
    interception: _Subsection[Interception] | None = None
    scheduledirrigation: _Subsection[_ScheduledIrrigation] | None = (
        _ScheduledIrrigation(schedule=0)
    )
    grasslandmanagement: _Subsection[GrasslandManagement] | None = None
    co2correction: _Subsection[CO2Correction] | None = None

    @property
    def crp(self) -> str:
        """Return the model string of the .crp file."""
        return self.model_string()


class Crop(_PySWAPBaseModel, _SerializableMixin, _FileMixin, _YAMLValidatorMixin):
    """Crop settings of the simulation.

    Attributes:
        swcrop (int): Switch for crop:

            * 0 - Bare soil.
            * 1 - Simulate crop.

        rds (float): Maximum rooting depth of the crop for this soil [1..5000, cm].
        croprotation (CROPROTATION): Table with crop rotation data.
        cropfiles (List[CropFile]): List of crop files.

    Methods:
        write_crop: Write the crop files.
    """

    swcrop: _Literal[0, 1, None] = None
    rds: float | None = _Field(default=None, ge=1, le=5000)
    croprotation: _Table | None = None
    cropfiles: dict[str, CropFile] = _Field(default_factory=dict, exclude=True)

    def write_crop(self, path: str):
        for name, cropfile in self.cropfiles.items():
            cropfile.save_file(string=cropfile.crp, fname=name, path=path)
