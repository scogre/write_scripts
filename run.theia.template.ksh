#!/bin/ksh

#-----------------------------------------------------------
# Run test case on Theia.  MUST BE RUN WITH A 
# MULTIPLE OF SIX MPI TASKS.  Could not get it to
# work otherwise.
#-----------------------------------------------------------

#PBS -l nodes=1:ppn=6
#PBS -l walltime=0:05:00
#PBS -A gsienkf
#PBS -q batch 
#PBS -N fv3
#PBS -o ./log
#PBS -e ./log

set -x

#np=$PBS_NP
np=6


source /apps/lmod/lmod/init/ksh
module purge
module load intel/15.1.133
module load impi/5.1.1.109 
module load netcdf/4.3.0

WORKDIR=RESTART_PATH/C384_MEMBER_NUMBER_PATH
rm -fr $WORKDIR
mkdir -p $WORKDIR
cd $WORKDIR

ln -fs ${PBS_O_WORKDIR}/NAMELIST_FILE ./fort.41

mpirun -np $np /scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/chgres_cube/exec/global_chgres.exe

DATADIR=RESTART_PATH/MEMBER_NUMBER_PATH
#rm -fr $DATADIR
exit 0


