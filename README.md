# Automatic Chicken Coop Door

Test project for using Micropython.

Designed for an ESP32, connected with a light sensor and a stepper motor. Upon the light sensor changing conditions, the stepper motor will drive the specified
number of steps required to either open or close the chicken coop door, depending on whether it has become light or dark. It will use a debouncing period of 2 minutes
to verify that the light state change is true.

## Setup

Connect the light sensor to GPIO25 as an input.

The stepper motor driver should be connected with:

- Step pin: GPIO18
- Dir pin: GPIO19

## Installation

Download Micropython and flash it onto target following [instructions](https://micropython.org/download/ESP32_GENERIC/).
