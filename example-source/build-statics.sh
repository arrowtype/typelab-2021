#!/bin/bash

set -e

dsPath="example-source/sources/recursive_mono_casual.designspace"


outputDir="ArrowType-ExampleFontBuild"
desktopDir="$outputDir/Desktop"
webDir="$outputDir/Web"
staticDir="$desktopDir/Static"

# -----------------------------------------------------------------------
# prep UFOs

python example-source/build-helpers/set-fea-code.py $dsPath -o static

# -----------------------------------------------------------------------
# build static fonts

echo "Building Static TTFs..."
fontmake -m $dsPath -o ttf --output-dir $staticDir --interpolate

# -----------------------------------------------------------------------
# post-processing fixes

function fixfont {
    static="$1"

    # get otf/ttf extension to use below
    ext=${static##*.}
    echo "$ext"

    # fix nonhinting
    gftools fix-nonhinting "$static" "$static"
    rm "${static/.$ext/-backup-fonttools-prep-gasp.$ext}"

    # [NOTE: a full build would usually include more fixing scripts]

    # add family name suffix to avoid installation conflicts with full Recursive typeface
    python example-source/build-helpers/add-familyname-suffix.py "$static" --suffix "TL21" --inplace

}

# this style of looping through files allows file paths to include spaces
find "$staticDir" -path '*.*tf' -print0 | while read -d $'\0' file
do
    fixfont "$file"
done

# -----------------------------------------------------------------------------------
# web fonts

mkdir -p "$webDir/Static"

find "$staticDir" -path '*.ttf' -print0 | while read -d $'\0' ttf
do
    woff2_compress "$ttf"

    woff2name=$(basename "${ttf/.ttf/.woff2}")
    mv "${ttf/.ttf/.woff2}" "$webDir/Static/$woff2name"
done
