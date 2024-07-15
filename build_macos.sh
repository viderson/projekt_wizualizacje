#!/bin/bash

ROOT=$(pwd)

if [ ! -d $ROOT/bin ]; then
    mkdir $ROOT/bin
fi

if [ ! -d $ROOT/bin/MacOS ]; then
    mkdir $ROOT/bin/MacOS
fi

pushd $ROOT/bin/MacOS

gcc $ROOT/src/run.c -D SETUP -o setup
gcc $ROOT/src/run.c -o run

cp -r $ROOT/src/templates $ROOT/bin/MacOS/

cp $ROOT/src/dataHandler.py $ROOT/bin/MacOS/
cp $ROOT/src/generate_map.py $ROOT/bin/MacOS/
cp $ROOT/src/main.py $ROOT/bin/MacOS/
cp $ROOT/src/requirements.txt $ROOT/bin/MacOS/
cp $ROOT/src/mapa_gmina_fredropol.png $ROOT/bin/MacOS/

popd
