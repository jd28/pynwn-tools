#!/usr/bin/env BASH

declare -a arr=("tlkie" "ErfEd" "areaglob" "2dilate" \
                "erfherder" "clothing_renamer" \
                "head_renamer" "nwsublime")

rm -rf dist
mkdir dist

for i in "${arr[@]}"
do
    cd "$i"
    rm -rf dist/
    python setup.py py2exe
    cp README.md "../dist/README - $i.md"
    cp -r dist/* ../dist
    cd ..
done
