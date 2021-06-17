#!/bin/bash

set -e

# -----------------------------------------------------------------------
# configure paths

dsPath="example-source/sources/recursive_mono_casual.designspace"

outputDir="ArrowType-ExampleFontBuild"
desktopDir="$outputDir/Desktop"
webDir="$outputDir/Web"
vf="RecursiveMonoCasual-Variable.ttf"

vfPath="$desktopDir/$vf"

# -----------------------------------------------------------------------
# prep UFOs

# prep feature code include paths
python example-source/build-helpers/set-fea-code.py $dsPath -o variable

# -----------------------------------------------------------------------
# build variable font

# make directory if it doesn’t yet exist
mkdir -p $desktopDir

echo "Building Variable Font..."
fontmake -m $dsPath -o variable --output-path $vfPath --verbose WARNING

# -----------------------------------------------------------------------
# post-processing fixes

# add STAT table
python example-source/build-helpers/add-STAT.py $desktopDir

# fix nonhinting
gftools fix-nonhinting "$vfPath" "$vfPath"
rm "${vfPath/.ttf/-backup-fonttools-prep-gasp.ttf}"

# add family name suffix to avoid installation conflicts with full Recursive typeface
python example-source/build-helpers/add-familyname-suffix.py $vfPath --suffix "TL21" --inplace

# [NOTE: a full build would usually include more fixing scripts]

# -----------------------------------------------------------------------
# make web font

echo "Making WOFF2..."
woff2_compress "$desktopDir/$vf"

# make directory if it doesn’t yet exist
mkdir -p "$webDir"

# move woff2 into webDir
mv ${vfPath/".ttf"/".woff2"} $webDir/${vf/".ttf"/".woff2"}

# -----------------------------------------------------------------------
# copy license

cp example-source/sources/OFL.txt $outputDir/LICENSE.txt

echo "These fonts are used for demo purposes only. Please visit github.com/arrowtype/recursive to find official Recursive fonts." > $outputDir/BEFORE_YOU_INSTALL.txt
