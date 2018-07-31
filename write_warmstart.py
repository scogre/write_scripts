# program to write the ensemble of restart files 
# that have had the resolution changed from C128 to C384
# from George Gayno's CHGRES code
# written to the 'control' template at C384 res
# in the filenames expected for restart application
# written by Scott Gregory; CIRES-NOAA-ESRL-PSD-FMD
from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index
from subprocess import call
nan=float('nan')

ensatmfilename='out.atm.tile'
corefilename='fv_core.res.tile'
tracerfilename='fv_tracer.res.tile'


#path2ens='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts1/C384_mem001/'
#path2ensmean='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts1/C384_ens001/'
#path2ctrl='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts1/control2/INPUT/'

path2ens='/lustre/f1/unswept/Scott.Gregory/2003112900/restarts/chgres_mem001/'
path2ensmean='/lustre/f1/unswept/Scott.Gregory/2003112900/restarts/chgres_ensmean/'
path2ctrl='/lustre/f1/unswept/Scott.Gregory/2003112900/restarts/control2/INPUT/'

for tileno in range(6):
   chgresd_file = path2ens+ensatmfilename+str(tileno+1)+'.nc'
   chgresd_ensmean_file = path2ensmean+ensatmfilename+str(tileno+1)+'.nc'
   warmfile_core = path2ens+corefilename+str(tileno+1)+'.nc'
   warmfile_tracer = path2ens+tracerfilename+str(tileno+1)+'.nc'
   core_restart_ctrl = path2ctrl+corefilename+str(tileno+1)+'.nc'
   tracer_restart_ctrl = path2ctrl+tracerfilename+str(tileno+1)+'.nc'
   print('newcore=',warmfile_core)
   print('oldcore=',core_restart_ctrl)
   ## make copy of core and tracer
   call(["cp", core_restart_ctrl, warmfile_core])
   call(["cp", tracer_restart_ctrl, warmfile_tracer])
   #open files
   chgres_emem = Dataset(chgresd_file,'r')   
   chgres_emean = Dataset(chgresd_ensmean_file,'r')
   chgres_core = Dataset(warmfile_core,'a')
   chgres_tracer = Dataset(warmfile_tracer,'a')
   ####################
   ####################
   ##CORE member
   w_emem = chgres_emem['w'][:]
   u_emem = chgres_emem['u_s'][:] 
   v_emem = chgres_emem['v_w'][:]
   T_emem = chgres_emem['T'][:]
   delp_emem = chgres_emem['delp'][:]
   ##TRACERS member
   sphum_emem = chgres_emem['sphum'][:]
   o3mr_emem = chgres_emem['o3mr'][:]
   liq_wat_emem = chgres_emem['liq_wat'][:]
   rainwat_emem = chgres_emem['rwmr'][:]
   ice_wat_emem = chgres_emem['icmr'][:]
   snowwat_emem = chgres_emem['snmr'][:]
   graupel_emem = chgres_emem['grle'][:]
   ##CORE ensmean
   w_emean = chgres_emean['w'][:]
   u_emean = chgres_emean['u_s'][:]
   v_emean = chgres_emean['v_w'][:]
   T_emean = chgres_emean['T'][:]
   delp_emean = chgres_emean['delp'][:]
   ##TRACERS ensmean
   sphum_emean = chgres_emean['sphum'][:]
   o3mr_emean = chgres_emean['o3mr'][:]
   liq_wat_emean = chgres_emean['liq_wat'][:]
   rainwat_emean = chgres_emean['rwmr'][:]
   ice_wat_emean = chgres_emean['icmr'][:]
   snowwat_emean = chgres_emean['snmr'][:]
   graupel_emean = chgres_emean['grle'][:]
   ####################
   ####################
   ## Perturbations
   w_pert = w_emem-w_emean
   u_pert = u_emem-u_emean
   v_pert = v_emem-v_emean
   T_pert = T_emem-T_emean
   delp_pert = delp_emem-delp_emean
   sphum_pert = sphum_emem-sphum_emean
   o3mr_pert = o3mr_emem-o3mr_emean
   liq_wat_pert = liq_wat_emem-liq_wat_emean
   rainwat_pert = rainwat_emem-rainwat_emean
   ice_wat_pert = ice_wat_emem-ice_wat_emean
   snowwat_pert = snowwat_emem-snowwat_emean
   graupel_pert = graupel_emem-graupel_emean
   ## 3d to 4d
   w_pert =np.expand_dims(w_pert, axis=0)
   u_pert =np.expand_dims(u_pert, axis=0)
   v_pert =np.expand_dims(v_pert, axis=0)
   T_pert =np.expand_dims(T_pert, axis=0)
   delp_pert =np.expand_dims(delp_pert, axis=0)
   sphum_pert =np.expand_dims(sphum_pert, axis=0)
   o3mr_pert =np.expand_dims(o3mr_pert, axis=0)
   liq_wat_pert =np.expand_dims(liq_wat_pert, axis=0)
   rainwat_pert =np.expand_dims(rainwat_pert, axis=0)
   ice_wat_pert =np.expand_dims(ice_wat_pert, axis=0)
   snowwat_pert =np.expand_dims(snowwat_pert, axis=0)
   graupel_pert =np.expand_dims(graupel_pert, axis=0)
   ##reassign varbs
   chgres_core['W'][:]=chgres_core['W'][:]+w_pert
   chgres_core['u'][:]=chgres_core['u'][:]+u_pert
   chgres_core['v'][:]=chgres_core['v'][:]+v_pert
   chgres_core['T'][:]=chgres_core['T'][:]+T_pert
   chgres_core['delp'][:]=chgres_core['delp'][:]+delp_pert
   chgres_tracer['sphum'][:]=chgres_tracer['sphum'][:]+sphum_pert
   chgres_tracer['o3mr'][:]=chgres_tracer['o3mr'][:]+o3mr_pert
   chgres_tracer['liq_wat'][:]=chgres_tracer['liq_wat'][:]+liq_wat_pert
   chgres_tracer['rainwat'][:]=chgres_tracer['rainwat'][:]+rainwat_pert
   chgres_tracer['ice_wat'][:]=chgres_tracer['ice_wat'][:]+ice_wat_pert
   chgres_tracer['snowwat'][:]=chgres_tracer['snowwat'][:]+snowwat_pert
   chgres_tracer['graupel'][:]=chgres_tracer['graupel'][:]+graupel_pert
   ### Test
   origcore=Dataset(core_restart_ctrl,'r')
   uorig = origcore['u'][:]
   udiff = uorig-chgres_core['u'][:]
   print('udiff/uorig=',udiff/uorig)
   ## close 
   chgres_core.close
   chgres_emem.close
   chgres_emean.close
   chgres_tracer.close
   origcore.close




### chgres'd
#lon = 384 ;
#lat = 384 ;
#lonp = 385 
#latp = 385 
#ps(lat, lon) ;
#w(lev, lat, lon) ;-------------->core W
#zh(levp, lat, lon) ;
#T(lev, lat, lon) ;-------------->core T
#delp(lev, lat, lon) ;----------->core delp
#sphum(lev, lat, lon) ;---------->tracer sphum
#o3mr(lev, lat, lon) ; ---------->tracer o3mr
#liq_wat(lev, lat, lon) ;-------> tracer liq_wat
#rwmr(lev, lat, lon) ;---------->tracer rainwat
#icmr(lev, lat, lon) ;--------> tracer ice_wat
#snmr(lev, lat, lon) ;--------> tracer snowwat
#grle(lev, lat, lon) ;-------->tracer graupel
#u_w(lev, lat, lonp) ; (384,385)
#v_w(lev, lat, lonp) ; (384,385)-->core v
#u_s(lev, latp, lon) ; (385,384)-->core u
#v_s(lev, latp, lon) ; (385,384)

### core
#xaxis_1 = 384
#xaxis_2 = 385
#yaxis_1 = 385
#yaxis_2 = 384
#DZ(Time, zaxis_1, yaxis_2, xaxis_1)
#T(Time, zaxis_1, yaxis_2, xaxis_1)                 T
#delp(Time, zaxis_1, yaxis_2, xaxis_1)             delp
#u(Time, zaxis_1, yaxis_1, xaxis_1) (time,z,385,384)..... u_s
#v(Time, zaxis_1, yaxis_2, xaxis_2) (time,z,384,385)..... v_w
#W(Time, zaxis_1, yaxis_2, xaxis_1) (time,z,384,384).....w
#phis(Time, yaxis_2, xaxis_1)
#ua(Time, zaxis_1, yaxis_2, xaxis_1)
#va(Time, zaxis_1, yaxis_2, xaxis_1)

### tracer
#ice_wat(Time, zaxis_1, yaxis_1, xaxis_1)   (time,z,385,384)..... icmr
#rainwat(Time, zaxis_1, yaxis_1, xaxis_1)   (time,z,385,384)..... rwmr
#liq_wat(Time, zaxis_1, yaxis_1, xaxis_1)   (time,z,385,384)..... liq_wat
#sphum(Time, zaxis_1, yaxis_1, xaxis_1)     (time,z,385,384)..... sphum
#snowwat(Time, zaxis_1, yaxis_1, xaxis_1)
#graupel(Time, zaxis_1, yaxis_1, xaxis_1)   (time,z,385,384)..... grle?
#o3mr(Time, zaxis_1, yaxis_1, xaxis_1)      (time,z,385,384)..... o3mr
#cld_amt(Time, zaxis_1, yaxis_1, xaxis_1)   

