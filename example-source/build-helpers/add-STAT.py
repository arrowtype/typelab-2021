"""
   python3 example/build-helpers/add-STAT.py <variable_font_path>

   This file is adapted from an example originally in https://github.com/Omnibus-Type/Texturina
"""

from fontTools.otlLib.builder import buildStatTable, _addName
from fontTools.ttLib import TTFont
import sys
import os


UPRIGHT_AXES = [
    dict(
        tag="wght",
        name="Weight",
        ordering=0,
        values=[
            dict(nominalValue=300, rangeMinValue=300, rangeMaxValue=350,name="Light"),
            dict(nominalValue=400, rangeMinValue=351, rangeMaxValue=450,name="Regular", flags=0x2, linkedValue=700),
            dict(nominalValue=500, rangeMinValue=451, rangeMaxValue=550,name="Medium"),
            dict(nominalValue=600, rangeMinValue=551, rangeMaxValue=650,name="SemiBold"),
            dict(nominalValue=700, rangeMinValue=651, rangeMaxValue=750,name="Bold"),
            dict(nominalValue=800, rangeMinValue=751, rangeMaxValue=800,name="ExtraBold"),
        ],
    ),
    dict(
        tag="slnt",
        name="Slant",
        ordering=1,
        values=[
            dict(value=0, name="Roman", flags=0x2, linkedValue=-15),
            dict(value=-15, name="Italic", linkedValue=0),
        ],
    ),
]

## [Not relavent to Recursive] adds STAT to separate Italic variable font, if roman/italic VFs are split
# ITALIC_AXES = [
#     dict(
#         tag="wght",
#         name="Weight",
#         ordering=0,
#         values=[
#             dict(nominalValue=100, rangeMinValue=100, rangeMaxValue=150,name="Thin"),
#             dict(nominalValue=200, rangeMinValue=151, rangeMaxValue=250,name="ExtraLight"),
#             dict(nominalValue=300, rangeMinValue=251, rangeMaxValue=350,name="Light"),
#             dict(nominalValue=400, rangeMinValue=351, rangeMaxValue=450,name="Regular", flags=0x2, linkedValue=700),
#             dict(nominalValue=500, rangeMinValue=451, rangeMaxValue=550,name="Medium"),
#             dict(nominalValue=600, rangeMinValue=551, rangeMaxValue=650,name="SemiBold"),
#             dict(nominalValue=700, rangeMinValue=651, rangeMaxValue=750,name="Bold"),
#             dict(nominalValue=800, rangeMinValue=751, rangeMaxValue=850,name="ExtraBold"),
#             dict(nominalValue=900, rangeMinValue=751, rangeMaxValue=850,name="Black"),
#         ],
#     ),
#     dict(
#         tag="ital",
#         name="Italic",
#         ordering=1,
#         values=[
#             dict(value=1, name="Italic"),
#         ],
#     ),
# ]

def update_fvar(ttfont):
    fvar = ttfont['fvar']
    nametable = ttfont['name']
    family_name = nametable.getName(16, 3, 1, 1033) or nametable.getName(1, 3, 1, 1033)
    family_name = family_name.toUnicode()
    font_style = "Italic" if "Italic" in ttfont.reader.file.name else "Roman"
    ps_family_name = f"{family_name.replace(' ', '')}{font_style}"
    nametable.setName(ps_family_name, 25, 3, 1, 1033)
    for instance in fvar.instances:
        instance_style = nametable.getName(instance.subfamilyNameID, 3, 1, 1033).toUnicode()
        instance_style = instance_style.replace("Italic", "").strip()
        if instance_style == "":
            instance_style = "Regular"
        ps_name = f"{ps_family_name}-{instance_style}"
        instance.postscriptNameID = _addName(nametable, ps_name, 256)


def main():
    buildDir = sys.argv[1]

    for filename in os.listdir(buildDir):
        filepath = os.path.join(buildDir, filename)

        # get variable font files
        if os.path.isfile(filepath) and "ttf" in filename:

            # process upright files
            if "italic" not in filename.lower():
                tt = TTFont(filepath)
                buildStatTable(tt, UPRIGHT_AXES)
                update_fvar(tt)
                tt.save(filepath)
                print(f"[STAT TABLE] Added STAT table to {filepath}")

            # [Not relavent to Recursive] process italics files
            # if "italic" in filename.lower():
            #     tt = TTFont(filepath)
            #     buildStatTable(tt, ITALIC_AXES)
            #     update_fvar(tt)
            #     tt.save(filepath)
            #     print(f"[STAT TABLE] Added STAT table to {filepath}")


if __name__ == "__main__":
    main()