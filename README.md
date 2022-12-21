# Maya Fill Selection

A small script written in Python 3 to add the capability of fill selection in Maya. I loved this feature in 3ds Max so thought of implementing it in Maya.

## Demo Video
https://youtu.be/G5mm3X4Sy8s

## How to use
1. Load the script in script editor or save to shelf
2. Delete history on mesh before use.
3. Select a boundary of face loops.
4. Then select ONE face inside the loop, this will tell maya what is inside and what is outside of the loop you selected.
5. Run the script from shelf or from script editor

## Note
1. Written in python 3 may not work in older version of Maya
2. Will only select faces that are part of that element (or shell)
3. Delete history before using.
4. May take some seconds to work on high poly models, wait for it to complete.
