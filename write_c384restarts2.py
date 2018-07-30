from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index
from subprocess import call
nan=float('nan')

ensatmfilename='out.atm.tile'
corefilename='fv_core.res.tile'
tracerfilename='fv_tracer.res.tile'

#path2ens='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts2/C384_mem001/'
path2ensmean='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts2/C384_ensmean/'
path2ctrl='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts2/control2/INPUT/'


for tileno in range(6):

   for memno in range(10):
      memstr=str(memno+1)
      if len(memstr)<2:
         memtext='mem00'+memstr
      else:
         memtext='mem0'+memstr
      path2ens='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts2/C384_'+memtext+'/'
      print('ensfile=',path2ens)
      chgresd_file = path2ens+ensatmfilename+str(tileno+1)+'.nc'
      #chgresd_ensmean_file = path2ensmean+ensatmfilename+str(tileno+1)+'.nc'
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
      if memno==0:
         print('STARTsum, mem=',memno)
         w_sum = np.zeros(w_emem.shape)
         u_sum = np.zeros(u_emem.shape)
         v_sum = np.zeros(v_emem.shape)
         T_sum = np.zeros(T_emem.shape)
         delp_sum = np.zeros(delp_emem.shape)
         sphum_sum =np.zeros(sphum_emem.shape)
         o3mr_sum = np.zeros(o3mr_emem.shape)
         liq_wat_sum = np.zeros(liq_wat_emem.shape)
         rainwat_sum = np.zeros(rainwat_emem.shape)
         ice_wat_sum = np.zeros(ice_wat_emem.shape)
         snowwat_sum = np.zeros(snowwat_emem.shape)
         graupel_sum = np.zeros(graupel_emem.shape)
      w_sum       = w_sum       +  w_emem  
      u_sum       = u_sum       +  u_emem    
      v_sum       = v_sum       +  v_emem  
      T_sum       = T_sum       +  T_emem
      delp_sum    = delp_sum    +  delp_emem 
      sphum_sum   = sphum_sum   +  sphum_emem 
      o3mr_sum    = o3mr_sum    +  o3mr_emem 
      liq_wat_sum = liq_wat_sum +  liq_wat_emem
      rainwat_sum = rainwat_sum +  rainwat_emem
      ice_wat_sum = ice_wat_sum +  ice_wat_emem
      snowwat_sum = snowwat_sum +  snowwat_emem
      graupel_sum = graupel_sum +  graupel_emem

      del w_emem  
      del u_emem    
      del v_emem  
      del T_emem
      del delp_emem 
      
      del sphum_emem 
      del o3mr_emem 
      del liq_wat_emem
      del rainwat_emem
      del ice_wat_emem
      del snowwat_emem
      del graupel_emem

      chgres_emem.close

   ##CORE ensmean
   w_emean       = w_sum      /10 
   u_emean       = u_sum      /10  
   v_emean       = v_sum      /10  
   T_emean       = T_sum      /10  
   delp_emean    = delp_sum   /10 
   ##TRACERS ensmean
   sphum_emean   = sphum_sum  /10
   o3mr_emean    = o3mr_sum   /10 
   liq_wat_emean = liq_wat_sum/10
   rainwat_emean = rainwat_sum/10
   ice_wat_emean = ice_wat_sum/10
   snowwat_emean = snowwat_sum/10
   graupel_emean = graupel_sum/10
   for memno in range(10):
      memstr=str(memno+1)
      if len(memstr)<2:
         memtext='mem00'+memstr
      else:
         memtext='mem0'+memstr
      path2ens='/scratch3/BMC/gsienkf/Scott.Gregory/CHGRES/experiments/2003122800_restarts2/C384_'+memtext+'/'
      print('ensfile=',path2ens)
      chgresd_file = path2ens+ensatmfilename+str(tileno+1)+'.nc'
      #chgresd_ensmean_file = path2ensmean+ensatmfilename+str(tileno+1)+'.nc'
      warmfile_core = path2ens+corefilename+str(tileno+1)+'.nc'
      warmfile_tracer = path2ens+tracerfilename+str(tileno+1)+'.nc'
      core_restart_ctrl = path2ctrl+corefilename+str(tileno+1)+'.nc'
      tracer_restart_ctrl = path2ctrl+tracerfilename+str(tileno+1)+'.nc'
      print('newcore=',warmfile_core)
      print('oldcore=',core_restart_ctrl)
      #open files
      chgres_emem = Dataset(chgresd_file,'r')
      #chgres_emean = Dataset(chgresd_ensmean_file,'r')
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
      #chgres_emean.close
      chgres_tracer.close
      origcore.close








