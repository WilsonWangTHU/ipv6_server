#!/bin/bash

myvar=1
while [ $myvar -le 10 ]
do 
    python testRun.py
    sleep 3
    myvar=$(($myvar + 1))
done
