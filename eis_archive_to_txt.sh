#!/bin/bash

# use this command if you want to repeat the action over multiple dirs.
# find . -type d -print0 | xargs -0 -n1 ./script.sh 
# parses the the folder name from arg
FOLDER=$1


# cycle through all folders, convert PDFs inside them into txt
#find . -name '*.pdf' -print0 | xargs -0 -n1 pdftotext

cd "$FOLDER"

for f in *.pdf; do
  pdftotext "$f"
done


# merge all individual TXTs into one TXT with name of the folder
cat *.txt > ../"$FOLDER".txt

