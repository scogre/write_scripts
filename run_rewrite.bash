#!/bin/bash
#################20070311002015030807##################################################
#PBS -l nodes=1:ppn=6
#PBS -l walltime=1:00:00
#PBS -A gsienkf
#PBS -q batch 


#datapath=$1

echo path= $datapath
python /scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/write_scripts/write_auto.py $datapath

hpsspath=$hpsspath
htar -cv -f $hpsspath $datapath


