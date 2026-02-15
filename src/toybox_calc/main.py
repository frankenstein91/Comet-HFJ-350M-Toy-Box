#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comet HFJ-350M Toy Box - Konfigurations-Rechner (v0.0.1-preclt2026 i18n)
Skript: toybox_calc.py
Author: DO3EET
Date: 2026-02-15
License: MIT
"""

import sys
import argparse
import gettext
import os

# --- Internationalisierung (i18n) Setup ---
# Suche nach Übersetzungen im 'locale' Verzeichnis relativ zum Skript
locale_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
try:
    translation = gettext.translation('toybox_calc', locale_dir, fallback=True)
    _ = translation.gettext
except Exception:
    _ = lambda s: s
# ------------------------------------------

# ANSI Colors für Arch Linux Terminal Ästhetik
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\033[90m'
    MAGENTA = '\033[95m'

# Datenbank: Werte aus dem Toy Box Manual (Seite 2)
# std_freq: Die Frequenz, auf die sich die Standard-Länge bezieht
antenna_data = [
    {
        "band": "160m",
        "freq_range": (1.8, 2.0),
        "std_freq": 1.8,
        "coil": _("Basis + 3.5 Spule + 1.8 Spule"),
        "jumper": _("Kein Jumper"),
        "length_mm": 1170,
        "radial": _("> 20m (ideal 40m)"),
        "change_per_cm": 7, # 7 kHz/cm
        "note": _("Extrem schmalbandig! Tuner fast immer nötig.")
    },
    {
        "band": "80m",
        "freq_range": (3.5, 3.8),
        "std_freq": 3.5,
        "coil": _("Basis + 3.5 Spule"),
        "jumper": _("Kein Jumper"),
        "length_mm": 910,
        "radial": _("ca. 20m"),
        "change_per_cm": 20, # 20 kHz/cm
        "note": ""
    },
    {
        "band": "40m",
        "freq_range": (7.0, 7.2),
        "std_freq": 7.0,
        "coil": _("Basis (Keine Zusatzspule)"),
        "jumper": _("Kein Jumper"),
        "length_mm": 960,
        "radial": _("ca. 12m"),
        "change_per_cm": 25, # 25 kHz/cm
        "note": _("Standard-Band für Portable.")
    },
    {
        "band": "30m",
        "freq_range": (10.1, 10.15),
        "std_freq": 10.1, # Manual says 10 MHz, usually refers to start
        "coil": _("Basis"),
        "jumper": _("Terminal 1"),
        "length_mm": 990,
        "radial": _("ca. 7-8m"),
        "change_per_cm": 40, # 40 kHz/cm
        "note": ""
    },
    {
        "band": "20m",
        "freq_range": (14.0, 14.35),
        "std_freq": 14.0,
        "coil": _("Basis"),
        "jumper": _("Terminal 2"),
        "length_mm": 800,
        "radial": _("ca. 5m"),
        "change_per_cm": 60, # 60 kHz/cm
        "note": ""
    },
    {
        "band": "17m",
        "freq_range": (18.068, 18.168),
        "std_freq": 18.0, # Manual says 18 MHz
        "coil": _("Basis"),
        "jumper": _("Terminal 3 (oder 2)"),
        "length_mm": 1070,
        "radial": _("ca. 4m"),
        "change_per_cm": 50, 
        "note": _("Bei hohem SWR Terminal 2 testen.")
    },
    {
        "band": "15m",
        "freq_range": (21.0, 21.45),
        "std_freq": 21.0,
        "coil": _("Basis"),
        "jumper": _("Terminal 3"),
        "length_mm": 750,
        "radial": _("ca. 3.5m"),
        "change_per_cm": 80, # 80 kHz/cm
        "note": ""
    },
    {
        "band": "12m",
        "freq_range": (24.89, 24.99),
        "std_freq": 24.9, # Manual says 24 MHz, but 24.9 is band start
        "coil": _("Basis"),
        "jumper": _("Terminal 3"),
        "length_mm": 530,
        "radial": _("ca. 3m"),
        "change_per_cm": 100, # 100 kHz/cm
        "note": ""
    },
    {
        "band": "10m",
        "freq_range": (28.0, 29.7),
        "std_freq": 28.5, # Manual explicitly says 28.5 MHz
        "coil": _("Basis"),
        "jumper": _("Terminal 4"),
        "length_mm": 1000,
        "radial": _("ca. 2.5m"),
        "change_per_cm": 120, # 120 kHz/cm
        "note": _("Teleskop NICHT voll ausziehen! Reserve ~26cm.")
    },
    {
        "band": "6m",
        "freq_range": (50.0, 52.0),
        "std_freq": 51.0, # Manual says 51 MHz
        "coil": _("Basis"),
        "jumper": _("Terminal 5"),
        "length_mm": 950,
        "radial": _("ca. 1.5m"),
        "change_per_cm": 100, # 100 kHz/cm
        "note": _("Achtung: Terminal 5 = Common + 5")
    }
]

def find_config(query):
    query_str = str(query).lower().strip()
    target_freq = None

    # Check if input is a band name (e.g. "40m", "40")
    for data in antenna_data:
        band_name = data["band"].replace("m", "")
        if query_str == data["band"] or query_str == band_name:
            return data, None

    # Check if input is a frequency (float)
    try:
        target_freq = float(query_str)
        for data in antenna_data:
            low, high = data["freq_range"]
            # Add a buffer for finding nearby bands (e.g. 6.9 or 7.3)
            if (low - 0.5) <= target_freq <= (high + 1.0):
                return data, target_freq
    except ValueError:
        pass

    return None, None

def draw_bar(length_mm, max_len=1266, bar_len=25, color_code=""):
    # Clamp length for drawing
    display_len = max(0, min(length_mm, max_len))
    filled_len = int((display_len / max_len) * bar_len)
    bar = "█" * filled_len + "░" * (bar_len - filled_len)
    return f"[{color_code}{bar}{Colors.ENDC}]"

def print_config(data, target_freq=None):
    if not data:
        print(f"{Colors.FAIL}{_('Keine Konfiguration für diese Eingabe gefunden.')}{Colors.ENDC}")
        return

    print(f"\n{Colors.HEADER}{_('=== Comet HFJ-350M (Toy Box) ===')}{Colors.ENDC}")
    print(f"{Colors.BOLD}{_('Band:')}{Colors.ENDC}          {Colors.CYAN}{data['band']}{Colors.ENDC} ({data['freq_range'][0]} - {data['freq_range'][1]} MHz)")
    
    print(f"\n{Colors.UNDERLINE}{_('Setup:')}{Colors.ENDC}")
    print(f" • {_('Spulen:')}      {data['coil']}")
    print(f" • {_('Jumper:')}      {Colors.GREEN}{data['jumper']}{Colors.ENDC}")
    print(f" • {_('Radial:')}      {data['radial']}")

    print(f"\n{Colors.UNDERLINE}{_('Strahler (Teleskop):')}{Colors.ENDC}")
    
    # 1. Standard Wert
    std_bar = draw_bar(data['length_mm'], color_code=Colors.BLUE)
    print(f" • {_('Standard')} ({data['std_freq']} MHz): {Colors.WARNING}{data['length_mm']} mm{Colors.ENDC}")
    print(f"   {std_bar}")

    # 2. Errechneter Wert (nur wenn Frequenz angegeben)
    if target_freq:
        # Berechnung: 
        # Höhere Freq = Kürzerer Draht.
        # Delta Freq (kHz) = (Ziel - Std) * 1000
        # Delta Länge (cm) = Delta Freq / change_per_cm
        
        diff_khz = (target_freq - data['std_freq']) * 1000
        change_cm = diff_khz / data['change_per_cm']
        
        # Länge in mm berechnen (Achtung: pos Change heißt kürzer!)
        calc_len_mm = data['length_mm'] - (change_cm * 10)
        calc_len_mm = int(round(calc_len_mm))

        # Warnungen bei Grenzwerten
        warning = ""
        if calc_len_mm > 1266:
            warning = f" {Colors.FAIL}({_('Max überschritten!')}){Colors.ENDC}"
            calc_len_mm = 1266
        elif calc_len_mm < 100: # Mechanisches Minimum ca
            warning = f" {Colors.FAIL}({_('Zu kurz!')}){Colors.ENDC}"
            calc_len_mm = 100

        calc_bar = draw_bar(calc_len_mm, color_code=Colors.MAGENTA)
        
        print(f"\n • {Colors.MAGENTA}{Colors.BOLD}{_('Kalkuliert')} ({target_freq} MHz): {calc_len_mm} mm{Colors.ENDC}{warning}")
        print(f"   {calc_bar}")
        
        diff_mm = calc_len_mm - data['length_mm']
        diff_text = f"+{diff_mm}" if diff_mm > 0 else f"{diff_mm}"
        print(f"   {_('Diff zum Standard:')} {Colors.BOLD}{diff_text} mm{Colors.ENDC}")

    print(f"\n{Colors.UNDERLINE}{_('Feinabstimmung (SWR):')}{Colors.ENDC}")
    print(f" • {_('Empfindlichkeit:')} {Colors.BOLD}{data['change_per_cm']} {_('kHz pro cm')}{Colors.ENDC}")
    
    khz = data['change_per_cm']
    print(f"   {Colors.GREY}-> {_('Freq zu tief? 1cm einschieben = +{khz} kHz').format(khz=khz)}")
    print(f"   -> {_('Freq zu hoch? 1cm ausziehen  = -{khz} kHz').format(khz=khz)}{Colors.ENDC}")

    if data['note']:
        print(f"\n{Colors.FAIL}{_('HINWEIS:')}{Colors.ENDC} {data['note']}")
    print("")

def main():
    parser = argparse.ArgumentParser(description=_('HFJ-350M Antennen Rechner'))
    parser.add_argument('query', nargs='?', help=_('Band (z.B. 40m) oder Frequenz (z.B. 7.1)'))
    
    args = parser.parse_args()

    if args.query:
        config, freq = find_config(args.query)
        print_config(config, freq)
    else:
        print(f"{Colors.HEADER}{_('HFJ-350M Tool (DO3EET Edition)')}{Colors.ENDC}")
        while True:
            try:
                user_input = input(f"{Colors.BOLD}{_('Band/Freq > ')}{Colors.ENDC}")
                if user_input.lower() in ['q', 'exit']:
                    break
                config, freq = find_config(user_input)
                print_config(config, freq)
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception:
                pass

if __name__ == "__main__":
    main()