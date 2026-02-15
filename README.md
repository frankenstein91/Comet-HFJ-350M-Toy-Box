# Toy Box Calc (HFJ-350M Calculator)

A command-line tool to calculate configurations for the Comet HFJ-350M antenna (Toy Box).

## Installation

You can install this tool directly from the source directory:

```bash
pip install .
```

Or for development (so changes to the code are immediately reflected):

```bash
pip install -e .
```

## Usage

Once installed, the command `toybox-calc` will be available in your terminal.

### Interactive Mode
Just run the command without arguments:
```bash
toybox-calc
```

### Direct Query
You can pass a band or frequency as an argument:
```bash
toybox-calc 40m
toybox-calc 7.1
```

## i18n
The tool supports multiple languages (German, English, Japanese) based on your system locale.

## Disclaimer
See [DISCLAIMER.md](DISCLAIMER.md) for safety instructions and liability information.
