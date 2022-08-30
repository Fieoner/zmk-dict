#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <dictionary file>')
    exit(1)

keycodes = {
    " ": "SPC",
    "-": "MINUS",
    ".": "DOT",
    ",": "COMMA",
    "/": "SLSH"
}

combos = []

with open('macros.dtsi', 'w') as outf:
    outf.write(
"""
/ {
    macros {

"""
    )

    with open(sys.argv[1],'r') as f:
        for line in f.readlines():
            combo, output = line.replace('\n', '').split(':')
            macroname = line.rstrip().replace(":", "_")
            outkeys = [keycodes[x] if x in keycodes else x for x in output]
            bindings = ' '.join(f'&kp {x.upper()}' for x in outkeys)
            outf.write(f'{" "*8}ZMK_MACRO({macroname}_macro, wait-ms = <1>; tap-ms = <1>; bindings = <{bindings}>;)\n')
            combos.append(f"""
        combo_"""+macroname+""" {
            timeout-ms = <80>;
            key-positions = <0 1>;
            bindings = <&"""+macroname+"""_macro>;
        };
            """)

    outf.write(
"""
    };
};
"""
    )

with open('combos.dtsi', 'w') as f:
    f.write('\n'.join(combos))
