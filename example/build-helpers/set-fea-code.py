"""
	Make sure path to fea code is uncommented (it gets commented to enable test installs from RoboFont)
"""

import sys
from fontTools.designspaceLib import DesignSpaceDocument
from fontParts.world import OpenFont
from ufonormalizer import normalizeUFO

def main():
    args = parser.parse_args()
    designspacePath = args.designspacePath[0]
    output = args.output

    ds = DesignSpaceDocument.fromfile(designspacePath)
    sources = [source.path for source in ds.sources]

    for fontPath in sources:

        font = OpenFont(fontPath, showInterface=False)

        print(f"Updating feature include paths in {font.info.styleName}")

        # for static build
        if output == "static":
            font.features.text = "include(../features-static.fea);"

        # for variable build
        if output == "variable":
            font.features.text = "include(./features-variable.fea);"

        font.save()
        font.close()
        
    print()

    normalizeUFO(fontPath, writeModTimes=False)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Adjust font feature paths for a variable vs static build.')
    parser.add_argument('designspacePath', 
                        help='Path to a designspace file',
                        nargs=1)
    parser.add_argument("-o", "--output",
                        default="",
                        required=True,
                        help='Output font type. Choose between: variable, static')

    main()