# Toy Box Calc (HFJ-350M Calculator)

A command-line tool to calculate configurations for the Comet HFJ-350M antenna (Toy Box).

## Installation

### From PyPI (Recommended)
The easiest way to install the tool is via [PyPI](https://pypi.org/project/toybox-calc/):

```bash
pip install toybox-calc
```

### For Arch Linux Users (AUR)
If you are running Arch Linux or its derivatives, you can install the package from the [AUR](https://aur.archlinux.org/packages/python-toybox-calc):

```bash
pikaur -S python-toybox-calc
```

### From Source
You can also install this tool directly from the repository:

```bash
git clone https://github.com/frankenstein91/Comet-HFJ-350M-Toy-Box.git
cd Comet-HFJ-350M-Toy-Box
pip install .
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
toybox-calc 28.074
```

### Version Check
Check your installed version:
```bash
toybox-calc --version
```

## i18n
The tool supports multiple languages (German, English, Japanese) based on your system locale.

## Disclaimer
See [DISCLAIMER.md](DISCLAIMER.md) for safety instructions and liability information.
