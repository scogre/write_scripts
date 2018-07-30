from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index
from subprocess import call
nan=float('nan')

ensatmfilename='out.atm.tile'
corefilename='fv_core.res.tile'
tracerfilename='fv_tracer.res.tile'


path2all=sys.argv[1]
#'/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES_restarts/'+DATE+'/restarts/C384_mem'
path2ensmean=path2all+'/C384_ensmean/'
path2ctrl=path2all+'/control2/INPUT/'


for memno in range(10):
   memstr=str(memno+1)
   if len(memstr)<2:
      memtext='mem00'+memstr
   else:
      memtext='mem0'+memstr
   path2ens=path2all+'/C384_'+memtext+'/'
   print('ensfile=',path2ens)
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








