#!/usr/bin/sh

#touch .gitignore
#echo 1.sh > .gitignore

git add *
git commit -m "q1"
git commit


token=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
git push https://${token}@github.com/mashalas/pyvenv-hover.git
