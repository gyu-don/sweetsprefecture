#!/bin/bash

awk 'BEGIN{ c=0;print "" } c{print $0} /add_newsite/{ c=1 }' newsite.py >> scraper.py
