#!/bin/bash

./get_gfs.pl data 2016013112 00 48 12 UGRD:VGRD 10_m_above_ground .
#./get-httpsubset.pl 2016013000 2016013021 UGRD-VGRD 10_m . gfs -nocheck
#./get-httpsubset.pl 2005040100 2005040121 TMP 2_m . gfs -nocheck

#     get_gfs.pl data DATE HR0 HR1 DHR VARS LEVS DIRECTORY

# DATE = start time of the forecast YYYYMMDDHH
#        note: HH should be 00 06 12 or 18

# HR0 = first forecast hour wanted
# HR1 = last forecast hour wanted
# DHR = forecast hour increment (forecast every 3, 6, 12, or 24 hours)
# VARS = list of variables or "all"
#         ex. HGT:TMP:OZONE
#         ex. all
# LEVS = list of levels, blanks replaced by an underscore, or "all"
#         ex. 500_mb:200_mb:surface
#         ex. all
# DIRECTORY = directory in which to put the output

# example:  perl get_gfs.pl data 2006101800 0 12 6 UGRD:VGRD 200_mb .
# example:  perl get_gfs.pl data 2006101800 0 12 6 UGRD:VGRD 200_mb:500_mb:1000_mb .
# example:  perl get_gfs.pl data 2006101800 0 12 12 all surface .


#
# define URL
#
# fhr=06
# hr=12
# date=20160130
# URL="http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?\
# file=gfs.t${hr}z.pgrbf${fhr}.grib2&\
# lev_500_mb=on&lev_700_mb=on&lev_1000_mb=on&\
# var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&\
# var_VGRD=on&subregion=&leftlon=250&\
# rightlon=330&toplat=60&bottomlat=20&\
# dir=%2Fgfs.${date}${hr}"

# # download file
# curl "$URL" -o download.grb
# # add a sleep to prevent a denial of service in case of missing file
# sleep 1