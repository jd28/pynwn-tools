#!/usr/bin/env BASH

declare -a arr=("tlkie" "ErfEd" "areaglob" "2dilate" "erfherder")

rm -rf dist
mkdir dist
#mkdir dist/library

for i in "${arr[@]}"
do
    cd "$i"
    rm -rf dist/
    python setup.py py2exe
    cp README.md "../dist/README - $i.md"
    cp -r dist/* ../dist
    cd ..
done

#7z a dist/library.zip dist/library/*
#rm -rf dist/library
