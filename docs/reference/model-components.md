# Model components

Each SWAP model is composed of components like lego blocks. This module defines
all the components that can be used to build a SWAP model.

<!-- prettier-ignore-start -->

## General settings

::: pyswap.components.metadata
    options:
        members:
            - Metadata
::: pyswap.components.simsettings
    options:
        members:
            - GeneralSettings
            - RichardsSettings

## Meteorological settings

::: pyswap.components.meteorology
    options:
        members:
            - Meteorology
            - MetFile
            - metfile_from_csv
            - metfile_from_knmi
            - DAILYMETEODATA
            - SHORTINTERVALMETEODATA
            - DETAILEDRAINFALL
            - RAINFLUX

## Crop settings

::: pyswap.components.crop
    options:
        members:
            - Crop
            - CropFile
            - CropDevelopmentSettingsFixed
            - CropDevelopmentSettingsWOFOST
            - CropDevelopmentSettingsGrass
            - Interception
            - OxygenStress
            - DroughtStress
            - SaltStress
            - CompensateRWUStress
            - Preparation
            - GrasslandManagement
            - CO2Correction
            - AMAXTB
            - CFTB
            - CHTB
            - CROPROTATION
            - DMGRZTB
            - DMMOWDELAY
            - DMMOWTB
            - DTSMTB
            - FOTB
            - FLTB
            - FRTB
            - FSTB
            - GCTB
            - KYTB
            - LOSSGRZTB
            - LOSSMOWTB
            - LSDATB
            - LSDBTB
            - MRFTB
            - RDCTB
            - RDRRTB
            - RDRSTB
            - RDTB
            - RFSETB
            - RLWTB
            - SLATB
            - TMNFTB
            - TMPFTB
            - VERNTB
            - WRTB

## Irrigation

::: pyswap.components.irrigation
    options:
        members:
        - FixedIrrigation
        - ScheduledIrrigation
        - IRRIGEVENTS

## Soil-water

::: pyswap.components.soilwater
    options:
        members:
        - Evaporation
        - SnowAndFrost
        - SoilMoisture
        - SoilProfile
        - SurfaceFlow
        - SOILHYDRFUNC
        - SOILPROFILE

## Drainage

::: pyswap.components.drainage
    options:
        members:
        - Flux
        - DraFile
        - Drainage
        - DATOWLTB1
        - DATOWLTB2
        - DATOWLTB3
        - DATOWLTB4
        - DATOWLTB5
        - DRAINAGELEVELTOPPARAMS
        - DRNTB
        - MANSECWATLVL
        - PRIWATLVL
        - QDRNTB
        - QWEIR
        - QWEIRTB
        - SECWATLVL

## Boundary conditions

::: pyswap.components.boundary
    options:
        members:
            - BottomBoundary
            - CSEEPARR
            - DATET
            - GWLEVEL
            - HAQUIF
            - HBOT5
            - INISSOIL
            - MISC
            - QBOT2
            - QBOT4
            - QTAB

## Transport

::: pyswap.components.transport
    options:
        members:
            - HeatFlow
            - SoluteTransport
            - INITSOILTEMP
            - SOILTEXTURES

<!-- prettier-ignore-end -->
