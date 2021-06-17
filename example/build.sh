#!/bin/bash

set -e

# -----------------------------------------------------------------------
# configure paths

dsPath="example/sources/recursive_mono_casual.designspace"

outputDir="ArrowType-RecursiveMonoCasual/Desktop"
desktopDir="$outputDir/Desktop"
webDir="$outputDir/Web"
vf="RecursiveMonoCasual-Variable.ttf"

vfPath="$desktopDir/$vf"

# -----------------------------------------------------------------------
# prep UFOs

# prep feature code include paths
python example/build-helpers/set-fea-code.py $dsPath -o variable

# -----------------------------------------------------------------------
# build variable font

echo "Building Variable Font..."
fontmake -m $dsPath -o variable --output-path $vfPath --verbose WARNING

# -----------------------------------------------------------------------
# post-processing fixes

# add STAT table
python example/build-helpers/add-STAT.py $desktopDir

# fix nonhinting
gftools fix-nonhinting "$vfPath" "$vfPath"
rm "${vfPath/.ttf/-backup-fonttools-prep-gasp.ttf}"

# [NOTE: a full build would usually include more fixing scripts]

# -----------------------------------------------------------------------
# make web font

echo "Making WOFF2..."
woff2_compress "$desktopDir/$vf"

# sort fonts
mkdir -p "$webDir"

mv ${vfPath/".ttf"/".woff2"} $webDir/${vf/".ttf"/".woff2"}

# -----------------------------------------------------------------------
# copy license

cp example/sources/OFL.txt $outputDir/LICENSE.txt
