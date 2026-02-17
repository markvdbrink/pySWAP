# mypy: disable-error-code="call-overload, misc"

"""Lateral drainage settings

Settings for the lateral drainage of the .swp file, including the .dra file settings.

Classes:
    Flux: Fluxes between drainage levels in .dra file.
    DraFile: Drainage file (.dra) settings.
    Drainage: The lateral drainage settings of .swp file.
"""

from typing import Literal as _Literal

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.tables import (
    DATOWLTB1,
    DATOWLTB2,
    DATOWLTB3,
    DATOWLTB4,
    DATOWLTB5,
    DRAINAGELEVELTOPPARAMS,
    DRNTB,
    MANSECWATLVL,
    PRIWATLVL,
    QDRNTB,
    QWEIR,
    QWEIRTB,
    SECWATLVL,
)
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import FNAME_IN as _FNAME_IN
from pyswap.core.fields import (
    File as _File,
    FloatList as _FloatList,
    String as _String,
    Subsection as _Subsection,
    Table as _Table,
)
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "Flux",
    "DraFile",
    "Drainage",
    "DATOWLTB1",
    "DATOWLTB2",
    "DATOWLTB3",
    "DATOWLTB4",
    "DATOWLTB5",
    "DRAINAGELEVELTOPPARAMS",
    "DRNTB",
    "MANSECWATLVL",
    "PRIWATLVL",
    "QDRNTB",
    "QWEIR",
    "QWEIRTB",
    "SECWATLVL",
]


class Flux(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Fluxes between drainage levels in .dra file.

    !!! Note:

        This is a single class containing the variables of each of the five
        drainage layers. Add a suffix with the number of the level you want to
        specify behind the variable (e.g. `drares1`, `swallo2`, etc.).

    Attributes:
        drares (float): Drainage resistance [10..1e5, d].
        infres (float): Infiltration resistance [10..1e5, d].
        swallo (Literal[1, 2]): Switch to allow drainage from this level.

            * 1: Drainage and infiltration are both allowed.
            * 2: Only infiltration is allowed.
            * 3: Only drainage is allowed.

        l (Optional[float]): Drain spacing (only if swdivd in DraFile equals 1) [1..1e5, m].
        zbotdr (Optional[float]): Level of the bottom of the drain (only if
            swdivd in DraFile equals 1) [-1e4..0, cm].
        swdtyp (Optional[Literal[1, 2]]): Type of drainage medium.

            * 1: Drain tube.
            * 2: Open channel.

        datowltb (Optional[DATOWL]): Table with channel water level as function
            of date. Add suffix to the table according to the level number (e.g. `DATOWL1`).
    """

    # level 1
    drares1: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres1: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo1: _Literal[1, 2, 3] | None = None
    l1: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr1: float = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp1: _Literal[1, 2] | None = None
    datowltb1: _Table | None = None
    # level 2
    drares2: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres2: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo2: _Literal[1, 2, 3] | None = None
    l2: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr2: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp2: _Literal[1, 2] | None = None
    datowltb2: _Table | None = None
    # level 3
    drares3: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres3: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo3: _Literal[1, 2, 3] | None = None
    l3: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr3: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp3: _Literal[1, 2] | None = None
    datowltb3: _Table | None = None
    # level 4
    drares4: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres4: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo4: _Literal[1, 2, 3] | None = None
    l4: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr4: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp4: _Literal[1, 2] | None = None
    datowltb4: _Table | None = None
    # level 5
    drares5: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres5: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo5: _Literal[1, 2, 3] | None = None
    l5: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr5: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp5: _Literal[1, 2] | None = None
    datowltb5: _Table | None = None


class DraFile(_PySWAPBaseModel, _FileMixin, _SerializableMixin):
    """Content of the drainage file (.dra).

    !!! Note:

        This class currently combines the basic drainage and surface water management
        routines and thus contains all the parameters of both methods. Please look
        at the documentation of the `Drainage` object which parameters need specification
        for each method.

    Attributes:
        swdivd (Literal[1, 2]): Calculate vertical distribution of
            drainage flux in groundwater:

            * 0: Don't calculate
            * 1: Calculate.
                    **Activates**: [`cofani`]

        cofani (Optional[FloatList]): Anisotropy factor for each soil layer
            (horizontal/vertical saturated hydraulic conductivity)
        dramet (Literal[1, 2, 3]): Method of lateral drainage calculation.
            Activated by `swdra=1` in the `Drainage` object.

            * 1: Use table of drainage flux - groundwater level relation.
                    **Activates**: [`lm1`, `qdrntb`]
            * 2: Use drainage formula of Hooghoudt or Ernst.
                    **Activates**: [`lm2`, `shape`, `wetper`, `zbotdr`, `entres`, `ipos`, `basegw`, `khtop`]
            * 3: Use drainage/infiltration resistance, multi-level if needed.
                    **Activates**: [`nrlevs`, `swintfl`, `swtopnrsrf`, `fluxes`]


        lm1 (Optional[float]): Drain spacing [1..1000, m]
        qdrntb (Optional[QDRNTB]): Table with relation between drainage flux and groundwater level.
        lm2 (Optional[float]): Drain spacing [1..1000, m].
        shape (Optional[float]): Shape factor to account for actual location between
            drain and water divide [0..1, -].
        wetper (Optional[float]): Wet perimeter of the drain [0..1000, cm].
        zbotdr (Optional[float]): Level below surface (negative) of drain bottom [-1000..0, cm].
        entres (Optional[float]): Drain entry resistance [0..1000, d].
        ipos (Optional[Literal[1, 2, 3, 4, 5]]): Position of drain

            * 1: On top of an impervious layer in a homogeneous profile
            * 2: Above an impervious layer in a homogeneous profile
            * 3: At the interface of a fine upper and a coarse lower soil layer
                    **Activates**: [`khbot`, `zintf`]
            * 4: In the lower, more coarse soil layer
                    **Activates**: [`khbot`, `zintf`, `kvtop`, `kvbot`]
            * 5: In the upper, more fine soil layer
                    **Activates**: [`khbot`, `zintf`, `kvtop`, `kvbot`, `geofac`]

        basegw (Optional[float]): Level of impervious layer below soil surface
            (negative) [-1e4..0, cm].
        khtop (Optional[float]): Horizontal hydraulic conductivity of the top
            layer [0..1000, cm/d].
        khbot (Optional[float]): Horizontal hydraulic conductivity of the bottom
            layer [0..1000, cm/d]
        zintf (Optional[float]): Interface level of the coarse and
            fine soil layer [-1e4..0, cm].
        kvtop (Optional[float]): Vertical hydraulic conductivity of
            the top layer [0..1000, cm/d].
        kvbot (Optional[float]): Vertical hydraulic conductivity of
            the bottom layer [0..1000, cm/d].
        geofac (Optional[float]): Geometric factor of Ernst [0..100, -].
        nrlevs (Optional[int]): Number of drainage levels [1..5, -].
        swtopnrsrf (Optional[Literal[0, 1]]): Switch to adjust the bottom of
            model discharge layer. Only in case of lateral interflow (swdivdra=1)
            or rapid discharge (swnrsrf=1 or swnrsrf=2).

            * 0: No
            * 1: Yes, the bottom of the highest order drainage system
                represents the maximum depth of the interflow.

        swintfl (Optional[Literal[0, 1]]): Option for interflow in highest
            drainage level (shallow system with short residence time)

            * 0: No
            * 1: Yes
                    **Activates**: [`cofintflb`, `expintflb`]

        cofintflb (Optional[float]): Coefficient for interflow relation [1e-2..10, d].
        expintflb (Optional[float]): Exponent for interflow relation [0.1..1, -].
        fluxes (Optional[Flux]): Flux object containing parameters for each drainage level.

        altcu (float): Altitude of the control unit relative to reference level [-3e5..3e5, cm].
        nrsrf (int): Number of subsurface drainage levels [1..5, -].
        drntb (DRNTB): Table with physical characteristics of each subsurface drainage level.
        swnrsrf (Literal[0, 1, 2]): Switch to introduce rapid subsurface drainage

            * 0: No rapid drainage
            * 1: Rapid drainage in the highest drainage system
                (implies adjustment of RDRAIN of highest drainage system)
                    **Activates**: [`rsurfdeep`, `rsurfshallow`]
            * 2: Rapid drainage as interflow according to a power relation
                (implies adjustment of RDRAIN of highest drainage system)
                    **Activates**: [`cofintfl`, `expintfl`]

        rsurfdeep (Optional[float]): Maximum resistance of rapid subsurface drainage [1e-3..1e3, d].
        rsurfshallow (Optional[float]): Minimum resistance of rapid subsurface drainage [1e-3..1e3, d].
        cofintfl (Optional[float]): Coefficient for interflow relation [0.01..10, 1/d].
        expintfl (Optional[float]): Exponent for interflow relation [0.1..1, -].
        swsrf (Literal[1, 2, 3]): Switch for interaction with surface water system

            * 1: No interaction with surface water system.
            * 2: Surface water system is simulated without separate primary system.
                    **Activates**: [`swsec`]
            * 3: Surface water system is simulated with separate primary system.
                    **Activates**: [`swsec`, `priwatlvl`]

        swsec (Optional[Literal[1, 2]]): Option for surface water level of secondary system

            * 1: Surface water level is input.
                     **Activates**: [`secwatlvl`]
            * 2: Surface water level is simulated
                     **Activates**: [`wlact`, `osswlm`, `nmper`, `mansecwatlvl`, `swqhr`]


        secwatlvl (Optional[SECWATLVL]): Table with water level in secondary course as function of date.
        wlact (Optional[float]): Initial surface water level [altcu-1000..altcu, cm].
        osswlm (Optional[float]): Criterium for warning about oscillation [0..10, cm].
        nmper (Optional[int]): Number of management periods [1..10, -].
        mansecwatlvl (Optional[MANSECWATLVL]): Table with parameters for each management period.
        swqhr (Optional[Literal[1, 2]]): Switch for type of discharge relationship.

            * 1: Exponential relationship
                    **Activates**: [`sofcu`, `qweir`]
            * 2: Table
                    **Activates**: [`qweirtb`]

        sofcu (Optional[float]): Size of the control unit [0.1..1e5, ha].
        qweir (Optional[QWEIR]): Table with parameters exponential weir discharge for all management periods.
        qweirtb (Optional[QWEIRTB]): Table with parameters of weir discharge for all management periods.
        priwatlvl (Optional[PRIWATLVL]): Table with water level in primary water course.
        swdislay (Literal[0, 1, 2]): Switch to adjust upper boundary of each model discharge layer.

            * 0: No adjustment.
            * 1: Adjustment based on depth of top of model discharge.
                    **Activates**: [`drainageleveltopparams`]
            * 2: Adjustment based on factor of top of model discharge.
                    **Activates**: [`drainageleveltopparams`]

        drainageleveltopparams(Optional[DRAINAGELEVELTOPPARAMS]): Table to adjust
            the top of each drainage level.
    """

    _extension = _PrivateAttr("dra")
    # General
    dramet: _Literal[1, 2, 3] | None = None
    swdivd: _Literal[1, 2] | None = None
    cofani: _FloatList | None = None
    swdislay: _Literal[0, 1, 2, 3] | None = None
    drainageleveltopparams: _Table | None = None
    # Drainage method 1: flux table
    lm1: float | None = _Field(default=None, ge=1.0, le=1000.0)
    qdrntb: _Table | None = None
    # Drainage method 2: formula
    lm2: float | None = _Field(default=None, ge=1.0, le=1000.0)
    shape: float | None = _Field(default=None, **_UNITRANGE)
    wetper: float | None = _Field(default=None, ge=0.0, le=1000.0)
    zbotdr: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    entres: float | None = _Field(default=None, ge=0.0, le=1000.0)
    ipos: _Literal[1, 2, 3, 4, 5] | None = None
    basegw: float | None = _Field(default=None, ge=-1.0e4, le=0.0)
    khtop: float | None = _Field(default=None, ge=0.0, le=1000.0)
    khbot: float | None = _Field(default=None, ge=0.0, le=1000.0)
    zintf: float | None = _Field(default=None, ge=-1.0e4, le=0.0)
    kvtop: float | None = _Field(default=None, ge=0.0, le=1000.0)
    kvbot: float | None = _Field(default=None, ge=0.0, le=1000.0)
    geofac: float | None = _Field(default=None, ge=0.0, le=100.0)
    # Drainage method 3: infiltration resistance
    nrlevs: int | None = _Field(default=None, ge=1, le=5)
    swintfl: _Literal[0, 1] | None = None
    cofintflb: float | None = _Field(default=None, ge=0.01, le=10.0)
    expintflb: float | None = _Field(default=None, ge=0.1, le=1.0)
    swtopnrsrf: _Literal[0, 1] | None = None
    fluxes: _Subsection | None = None
    # Extended section: surface water management
    altcu: float | None = _Field(default=None, ge=-300000.0, le=300000.0)
    drntb: _Table | None = None
    nrsrf: int | None = _Field(default=None, ge=1, le=5)
    swnrsrf: _Literal[0, 1, 2] | None = None
    rsurfdeep: float | None = _Field(default=None, ge=0.001, le=1000.0)
    rsurfshallow: float | None = _Field(default=None, ge=0.001, le=1000.0)
    cofintfl: float | None = _Field(default=None, ge=0.01, le=10.0)
    expintfl: float | None = _Field(default=None, ge=0.01, le=10.0)
    swsrf: _Literal[1, 2, 3] | None = None
    swsec: _Literal[1, 2] | None = None
    secwatlvl: _Table | None = None
    wlact: float | None = _Field(default=None, ge=-300000.0, le=300000.0)
    osswlm: float | None = _Field(default=None, ge=0.0, le=10.0)
    nmper: int | None = _Field(default=None, ge=1, le=3660)
    mansecwatlvl: _Table | None = None
    swqhr: _Literal[1, 2] | None = None
    sofcu: float | None = _Field(default=None, ge=0.1, le=100000.0)
    qweir: _Table | None = None
    qweirtb: _Table | None = None
    priwatlvl: _Table | None = None

    @property
    def dra(self):
        return self.model_string()


class Drainage(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """The lateral drainage settings inside .swp file.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.

            * 0: No drainage.
            * 1: Simulate with a basic drainage routine. Specify `swdivd` and
                `dramet` and associated parameters in the `drafile`.
                    **Activates**: [`drafile`]
            * 2: Simulate with surface water management. Specify `altcu`,
                `nrsrf`, `drntb`, `swnrsrf` and `swdislay`.
                    **Activates**: [`drafile`]

        drfil (str): Name of the file. This attribute is frozen, there is no
            need to change it.
        drafile (Optional[DraFile]): Content of the drainage file.
    """

    swdra: _Literal[0, 1, 2] | None = None
    drfil: _String | None = _Field(default=_FNAME_IN, frozen=True)
    drafile: _File | None = _Field(default=None, exclude=True)

    def write_dra(self, path: str) -> None:
        self.drafile.save_file(string=self.drafile.dra, fname=self.drfil, path=path)
        return None
