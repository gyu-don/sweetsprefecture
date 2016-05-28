#!/bin/bash

awk 'BEGIN{ c=0;print "" } c&&length()>0{print "   ",$0} c&&length()==0{ print "" } /add_newsite/{ c=1 }' newsite.py >> scraper.py
