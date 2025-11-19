# Model components

Each SWAP model is composed of components like lego blocks. This module defines
all the components that can be used to build a SWAP model.

<!-- prettier-ignore-start -->

## General settings

::: pyswap.components.metadata
::: pyswap.components.simsettings

## Meteorological settings

::: pyswap.components.meteorology
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.meteorology
    options:
        filters:
            - "^[A-Z0-9_]+$"

## Crop settings

::: pyswap.components.crop
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.crop
    options:
        filters:
            - "^[A-Z0-9_]+$"

## Irrigation

::: pyswap.components.irrigation
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.irrigation
    options:
        filters:
            - "^[A-Z0-9_]+$"

## Soil-water

::: pyswap.components.soilwater
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.soilwater
    options:
        filters:
            - "^[A-Z0-9_]+$"

## Drainage

::: pyswap.components.drainage
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.drainage
    options:
        filters:
            - "^[A-Z0-9_]+$"

## Boundary conditions

::: pyswap.components.boundary
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.boundary
    options:
        filters:
            - "^[A-Z0-9_]+$"

## Transport

::: pyswap.components.transport
    options:
        filters:
            - "!^[A-Z0-9_]+$"
::: pyswap.components.transport
    options:
        filters:
            - "^[A-Z0-9_]+$"

<!-- prettier-ignore-end -->
