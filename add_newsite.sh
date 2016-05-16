#!/bin/bash

awk 'BEGIN{ print "" } NR>3&&length()>0{print "   ",$0} NR>3&&length()==0{ print "" }' newsite.py >> scraper.py
