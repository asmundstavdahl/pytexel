#!/bin/bash

usage(){
    echo "$0 image( image)*"
}

if [ $# -lt 1 ]
then
    usage
else
    for img in $@
    do
        python3 texelate.py --width $(tput cols) --height $(tput lines) "$img"
        # --width $(tput cols) --height $(tput lines)
    done
fi
