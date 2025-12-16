# mypy: disable-error-code="call-overload, misc, override"
# Justification for exemptions:
# - call-overload and misc was raised wherever I unpacked values inside Field()
#   calls (e.g., **_UNITRANGE). This approach works correctly.
# - override was raised on model_string, because the methods do not share the
#   same signature. This was not a proirity to fix.
"""Boundary conditions settings.

Classes:

    BottomBoundary: Bottom boundary settings.
"""

from pathlib import Path as _Path
from typing import Literal as _Literal

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.tables import (
    CSEEPARR,
    DATET,
    GWLEVEL,
    HAQUIF,
    HBOT5,
    INISSOIL,
    MISC,
    QBOT2,
    QBOT4,
    QTAB,
)
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import (
    Decimal2f as _Decimal2f,
    String as _String,
    Table as _Table,
)
from pyswap.core.valueranges import (
    UNITRANGE as _UNITRANGE,
    YEARRANGE as _YEARRANGE,
)
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "BottomBoundary",
    "CSEEPARR",
    "DATET",
    "GWLEVEL",
    "HAQUIF",
    "HBOT5",
    "INISSOIL",
    "MISC",
    "QBOT2",
    "QBOT4",
    "QTAB",
]


class BottomBoundary(
    _PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin, _FileMixin
):
    """Bottom boundary settings.

    Technically in SWAP boundary conditions can be specified either inside the
    .swp file or in a separate .bbc file. The `swbbcfile` attribute determines
    whether the boundary conditions are written to a .bbc file.

    Attributes:
        swbbcfile (Literal[0, 1]): Switch whether to generate a .bbc file

            * 0: Specify boundary conditions in current file (preferred).
            * 1: Specify boundary conditions in a separate .bbc file. Might be
                deprecated in the future.
                    **Activates**: [`bbcfile`]

        bbcfil (Optional[String]): Name of file with bottom boundary data
            (without .BBC extension).
        swbotb (Literal[1, 2, 3, 4, 5, 6, 7, 8]): Switch for type of
            bottom boundary.

            * 1: Prescribe groundwater level
                    **Activates**: [`gwlevel`]
            * 2: Prescribe bottom flux
                    **Activates**: [`sw2`]
            * 3: Calculate bottom flux from hydraulic head of deep aquifer
                    **Activates**: [`swbotb3resvert`, `swbotb3impl`, `shape`
                        `hdrain`, `rimlay`, `sw3`, `sw4`]
            * 4: Calculate bottom flux as function of groundwater level
                    **Activates**: [`swqhbot`]
            * 5: Prescribe soil water pressure head of bottom compartment
                    **Activates**: [`hbot5`]
            * 6: Bottom flux equals zero.
            * 7: Free drainage of soil profile.
            * 8: Free outflow at soil-air interface.

        gwlevel (Optional[GWLEVEL]): Table with groundwater level data.
        sw2 (Optional[Literal[1, 2]]): Specify whether a sinus function or
            a table are used for the bottom flux.

            * 1: Sinus function
                    **Activates**: [`sinave`, `sinamp`, `sinmax`]
            * 2: Table
                    **Activates**: [`qbot`]

        sinave (Optional[float]): Average value of bottom flux (positive is
            upwards) [-10..10, cm/d]
        sinamp (Optional[float]): Amplitude of bottom flux sine function [-10..10, cm/d]
        sinmax (Optional[float]): Time of the year with maximum bottom flux [0..366, d]
        qbot (Optional[QBOT2]): Table with bottom flux data.

        swbotb3resvert (Optional[Literal[0, 1]]): Switch for vertical
            hydraulic resistance between bottom boundary and groundwater level.

            * 0: Include vertical hydraulic resistance.
            * 1: Suppress vertical hydraulic resistance.

        swbotb3impl (Optional[Literal[0, 1]]): Switch for numerical solution
            of bottom flux.

            * 0: Explicit solution (choose always when `shape` < 1.0).
            * 1: Implicit solution.

        shape (Optional[float]): Shape factor to derive average groundwater
            level [0..1, -].
        hdrain (Optional[float]): Mean drain base to correct for average
            groundwater level [-1e4..0, cm].
        rimlay (Optional[float]): Vertical resistance of aquitard [0..1e5, d].
        sw3 (Optional[Literal[1, 2]]): Specify whether a sinus function or
            a table are used for the hydraulic head in the deep aquifer.

            * 1: Sinus function
                    **Activates**: [`aqave`, `aqamp`, `aqtmax`, `aqper`]
            * 2: Table
                    **Activates**: [`haquif`]

        aqave (Optional[float]): Average hydraulic head in underlaying
            aquifer [-1e4..1e3, cm].
        aqamp (Optional[float]): Amplitude hydraulic head sinus wave [0..1e3, cm].
        aqtmax (Optional[float]): First time of the year with maximum
            hydraulic head [0..366, d].
        aqper (Optional[float]): Period of hydraulic head sinus wave [0..366, d].
        haquif (Optional[HAQUIF]): Table with average pressure head in
            underlaying aquifer as function of time.
        sw4 (Optional[Literal[0, 1]]): An extra groundwater flux can be
            specified which is added to above specified flux.

            * 0: No extra flux.
            * 1: Extra flux.
                    **Activates**: [`qbot4`]

        qbot4 (Optional[QBOT4]): Table with extra bottom flux data.

        swqhbot (Optional[Literal[1, 2]]): Specify whether an exponential
            relation or a table is used.

            * 1: Bottom flux is calculated with an exponential relation.
                    **Activates**: [`cofqha`, `cofqhb`, `cofqhc`]
            * 2: Bottom flux is derived from a table.
                    **Activates**: [`qtab`]

        cofqha (Optional[float]): Coefficient A for exponential relation for
            bottom flux [-100..100, cm/d].
        cofqhb (Optional[float]): Coefficient B for exponential relation for
            bottom flux [-1..1, 1/cm].
        cofqhc (Optional[float]): Water flux (positive upward) in addition to
            flux from exponential relation [-10..10, cm/d].
        qtab (Optional[QTAB]): Table with groundwater level-bottom
            flux relation.
        hbot5 (Optional[HBOT5]): Table with the bottom compartment
            pressure head.
    """

    _extension = _PrivateAttr(default="bbc")

    swbbcfile: _Literal[0, 1] | None = None
    bbcfil: _String | None = None
    swbotb: _Literal[1, 2, 3, 4, 5, 6, 7, 8] | None = None
    sw2: _Literal[1, 2] | None = None
    sw3: _Literal[1, 2] | None = None
    sw4: _Literal[0, 1] | None = None
    swbotb3resvert: _Literal[0, 1] | None = None
    swbotb3impl: _Literal[0, 1] | None = None
    swqhbot: _Literal[1, 2] | None = None
    sinave: _Decimal2f | None = _Field(ge=-10.0, le=10.0, default=None)
    sinamp: _Decimal2f | None = _Field(ge=-10.0, le=10.0, default=None)
    sinmax: _Decimal2f | None = _Field(**_YEARRANGE, default=None)
    shape: _Decimal2f | None = _Field(**_UNITRANGE, default=None)
    hdrain: _Decimal2f | None = _Field(ge=-10000.0, le=0.0, default=None)
    rimlay: _Decimal2f | None = _Field(ge=0, le=100000.0, default=None)
    aqave: _Decimal2f | None = _Field(ge=-10000, le=1000, default=None)
    aqamp: _Decimal2f | None = _Field(ge=0, le=1000.0, default=None)
    aqtmax: _Decimal2f | None = _Field(**_YEARRANGE, default=None)
    aqper: _Decimal2f | None = _Field(**_YEARRANGE, default=None)
    cofqha: _Decimal2f | None = _Field(ge=-100.0, le=100.0, default=None)
    cofqhb: _Decimal2f | None = _Field(ge=-1.0, le=1.0, default=None)
    cofqhc: _Decimal2f | None = _Field(ge=-10.0, le=10.0, default=None)
    gwlevel: _Table | None = None
    qbot: _Table | None = None
    haquif: _Table | None = None
    qbot4: _Table | None = None
    qtab: _Table | None = None
    hbot5: _Table | None = None

    def bbc(self) -> str:
        """Return the string representing the bbc file."""
        return self._model_string(exclude={"swbbcfile", "bbcfil"})

    def _model_string(self, **kwargs) -> str:
        """Internal method to handle model string generation.

        This was implemented to avoid pydantic from raising a maximum recursion
        depth error when calling the model_string method from the super class.
        """
        return super().model_string(**kwargs)

    def model_string(self, **kwargs) -> str:
        """Override model_string method to handle the swbbcfile attribute.

        This method is called in the final serialization step, when each section
        is converted into a string representation. So, depending on the
        swbbcfile attribute, this function will return:

            - a full section string representation, as for when all boundary
                conditions are included in the .swp file, or;
            - it will only include swbbcfile and bbcfil (the name of the file
                when the other parameters are defined). In that case, the other
                parameters are written to a separate .bbc file using the
                write_bbc method.
        """
        if self.swbbcfile == 1:
            return super().model_string(include={"swbbcfile", "bbcfil"}, **kwargs)
        else:
            return super().model_string()

    def write_bbc(self, path: _Path):
        """Write bottom boundary conditions to a .bbc file.

        This method is only available when the swbbcfile attribute is set to 1.
        Writes entire setion settings (except swbbcfile and bbcfil, defined in
        the .swp file) to a separate .bbc file.

        Parameters:
            path (Path): Path to the directory where the .bbc file will be
                saved.
        """
        if self.swbbcfile != 1:
            msg = "Bottom boundary conditions are not set to be written to a .bbc file."
            raise ValueError(msg)

        self.save_file(string=self.bbc(), fname=self.bbcfil, path=path)
