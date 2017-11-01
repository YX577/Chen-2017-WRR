#!/usr/bin/env python

import numpy as np
import netCDF4 as nc
import sys
from calendar import monthrange

model = sys.argv[1]
year = sys.argv[2]  # e.g.   1970
month = sys.argv[3]  # e.g.  1
indir = sys.argv[4]  # e.g.  /raid/xiaodong.chen/lulcc/data.../remap_by_month
file_pattern = sys.argv[5]  # e.g.   day.CMCC-CM
outdir = sys.argv[6]  # e.g. /raid/xiaodong.chen/lulcc/data...monthly_ext

yearp_num = int(year)
monthp_num = int(month)-1
if monthp_num==0:
	yearp_num = yearp_num-1
	monthp_num = 12
yearp = str(yearp_num)
monthp = str(monthp_num)

def get_nc_var(infile, var):
    ingroup = nc.Dataset(infile, 'r', format='NETCDF4')
    outdata = ingroup.variables[var][:]
    ingroup.close()
    
    return outdata

def interpolate_24h_to_12h_4d(indata):
    nt, nlev, nx, ny = indata.shape[0:4]
    nt_h = nt*2-1
    outdata = np.zeros((nt_h, nlev, nx, ny))
    for i in np.arange(nt_h):
        if i%2==0:
            outdata[i,:,:,:] = indata[i/2,:,:,:]
        if i%2==1:
            outdata[i,:,:,:] = (indata[i/2,:,:,:] + indata[i/2+1,:,:,:])/2
            
    return outdata

def interpolate_24h_to_12h_3d(indata):
    nt, nx, ny = indata.shape[0:4]
    nt_h = nt*2-1
    outdata = np.zeros((nt_h, nx, ny))
    for i in np.arange(nt_h):
        if i%2==0:
            outdata[i,:,:] = indata[i/2,:,:]
        if i%2==1:
            outdata[i,:,:] = (indata[i/2,:,:] + indata[i/2+1,:,:])/2
            
    return outdata

def interpolate_24h_to_12h_1d(indata):
    nt = indata.shape[0]
    nt_h = nt*2-1
    outdata = np.zeros((nt_h))
    for i in np.arange(nt_h):
        if i%2==0:
            outdata[i] = indata[i/2]
        if i%2==1:
            outdata[i] = (indata[i/2] + indata[i/2+1])/2
            
    return outdata

#lat_data = get_nc_var(indir + '/ta.'+file_pattern+'.'+year+'.'+month+'.nc', 'lat')
lat_data = np.arange(-88.6,88.7,1.8653)
lon_data = get_nc_var(indir + '/ta.'+file_pattern+'.'+year+'.'+month+'.nc', 'lon')
level_data = get_nc_var(indir + '/ta.'+file_pattern+'.'+year+'.'+month+'.nc', 'plev')

## current month
# atmos data
ta_data_current = get_nc_var(indir + '/ta.'+file_pattern+'.'+year+'.'+month+'.nc', 'ta')
ua_data_current = get_nc_var(indir + '/ua.'+file_pattern+'.'+year+'.'+month+'.nc', 'ua')
va_data_current = get_nc_var(indir + '/va.'+file_pattern+'.'+year+'.'+month+'.nc', 'va')
wap_data_current = get_nc_var(indir + '/wap.'+file_pattern+'.'+year+'.'+month+'.nc', 'wap')
z_data_current = get_nc_var(indir + '/zg.'+file_pattern+'.'+year+'.'+month+'.nc', 'zg')

# surface data
tas_data_current = get_nc_var(indir + '/tas.'+file_pattern+'.'+year+'.'+month+'.nc', 'tas')
uas_data_current = get_nc_var(indir + '/uas.'+file_pattern+'.'+year+'.'+month+'.nc', 'uas')
vas_data_current = get_nc_var(indir + '/vas.'+file_pattern+'.'+year+'.'+month+'.nc', 'vas')


## previous month
# atmos data
ta_data_prev = get_nc_var(indir + '/ta.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'ta')
ua_data_prev = get_nc_var(indir + '/ua.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'ua')
va_data_prev = get_nc_var(indir + '/va.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'va')
wap_data_prev = get_nc_var(indir + '/wap.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'wap')
z_data_prev = get_nc_var(indir + '/zg.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'zg')

# surface data
tas_data_prev = get_nc_var(indir + '/tas.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'tas')
uas_data_prev = get_nc_var(indir + '/uas.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'uas')
vas_data_prev = get_nc_var(indir + '/vas.'+file_pattern+'.'+yearp+'.'+monthp+'.nc', 'vas')


# concatenate them
ta_data = np.concatenate((ta_data_prev, ta_data_current), axis=0)
ua_data = np.concatenate((ua_data_prev, ua_data_current), axis=0)
va_data = np.concatenate((va_data_prev, va_data_current), axis=0)
wap_data = np.concatenate((wap_data_prev, wap_data_current), axis=0)
z_data = np.concatenate((z_data_prev, z_data_current), axis=0)
tas_data = np.concatenate((tas_data_prev, tas_data_current), axis=0)
uas_data = np.concatenate((uas_data_prev, uas_data_current), axis=0)
vas_data = np.concatenate((vas_data_prev, vas_data_current), axis=0)

# convert 24-hr data to 12-hr data
ta_data_12h = interpolate_24h_to_12h_4d(ta_data)
ua_data_12h = interpolate_24h_to_12h_4d(ua_data)
va_data_12h = interpolate_24h_to_12h_4d(va_data)
wap_data_12h = interpolate_24h_to_12h_4d(wap_data)
z_data_12h = interpolate_24h_to_12h_4d(z_data)

tas_data_12h = interpolate_24h_to_12h_3d(tas_data)
uas_data_12h = interpolate_24h_to_12h_3d(uas_data)
vas_data_12h = interpolate_24h_to_12h_3d(vas_data)

totaldays = monthrange(int(year),int(month))[1] # days in current month
totalsnaps = 21+2*totaldays-1 # snaps in current, plus 21 from previous month
time_data_12h = np.arange(totalsnaps)*12
begin_day = monthrange(int(yearp),int(monthp))[1]-10+1 #extra 10 days

nt, nlev, nx, ny = ta_data.shape[0:4]

outfile = outdir + '/' +model+ '.'+year+'.'+month+'.12hr.ext.nc'
print outfile
outgroup = nc.Dataset(outfile, 'w', format='NETCDF4')

# define dimensions
londim = outgroup.createDimension('lon', ny)
latdim = outgroup.createDimension('lat', nx)
levdim = outgroup.createDimension('lev', nlev)
timedim = outgroup.createDimension('time', 0)

# define variables
lonvar = outgroup.createVariable('lon', 'f8', ('lon'))
lonvar.standard_name = 'longitude'
lonvar.long_name = 'longitude'
lonvar.units = 'degrees_east'
lonvar.axis = 'X'

latvar = outgroup.createVariable('lat', 'f8', ('lat'))
latvar.standard_name = 'latitude'
latvar.long_name = 'latitude'
latvar.units = 'degrees_north'
latvar.axis = 'Y'

levvar = outgroup.createVariable('lev', 'f8', ('lev'))
levvar.standard_name = 'air_pressure'
levvar.long_name = 'pressure'
levvar.units = 'Pa'
levvar.positive = 'down'
levvar.axis = 'Z'

timevar = outgroup.createVariable('time', 'f8', ('time'))
timevar.standard_name = 'time'
timevar.units = 'hours since '+yearp+'-'+monthp+'-'+str(begin_day)+' 00:00:00'
timevar.calendar = 'proleptic_gregorian'
timevar.axis = 'T'

latvar[:] = lat_data
lonvar[:] = lon_data
levvar[:] = level_data
timevar[:] = time_data_12h

# atmos
var129var = outgroup.createVariable('var129', 'f4', ('time','lev','lat','lon'))  # geopotential, m2/s2
var129var.table = 128
var130var = outgroup.createVariable('var130', 'f4', ('time','lev','lat','lon'))  # temperature, K
var130var.table = 128
var135var = outgroup.createVariable('var135', 'f4', ('time','lev','lat','lon'))  # vertical velocity, Pa/s
var135var.table = 128
var131var = outgroup.createVariable('var131', 'f4', ('time','lev','lat','lon'))  # U wind, m/s
var131var.table = 128
var132var = outgroup.createVariable('var132', 'f4', ('time','lev','lat','lon'))  # V wind, m/s
var132var.table = 128

var129var[:] = z_data_12h[-1*totalsnaps::,:,:,:]*9.80665  # this is geopotential, not geopotential height
var130var[:] = ta_data_12h[-1*totalsnaps::,:,:,:]
var135var[:] = wap_data_12h[-1*totalsnaps::,:,:,:]
var131var[:] = ua_data_12h[-1*totalsnaps::,:,:,:]
var132var[:] = va_data_12h[-1*totalsnaps::,:,:,:]

# surface
var165var = outgroup.createVariable('var165', 'f4', ('time','lat','lon'))  # 10m U wind, m/s
var165var.table = 128
var166var = outgroup.createVariable('var166', 'f4', ('time','lat','lon'))  # 10m V wind, m/s
var166var.table = 128
var167var = outgroup.createVariable('var167', 'f4', ('time','lat','lon'))  # 2m temperature, K
var167var.table = 128

var165var[:] = uas_data_12h[-1*totalsnaps::,:,:]
var166var[:] = vas_data_12h[-1*totalsnaps::,:,:]
var167var[:] = tas_data_12h[-1*totalsnaps::,:,:]                                                                          

# global attribute
outgroup.CDI = 'Climate Data Interface version 1.7.2 (http://mpimet.mpg.de/cdi)'
outgroup.Conventions = 'CF-1.4'
outgroup.history = 'Created from python script'
outgroup.institution = 'European Centre for Medium-Range Weather Forecasts'
outgroup.CDO = 'Climate Data Operators version 1.7.2 (http://mpimet.mpg.de/cdo)'

outgroup.close()