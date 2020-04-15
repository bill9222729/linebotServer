from datetime import datetime
ntime = datetime.now()
hour = ntime.hour
print(11*3600+30*60)
print(13*3600+50*60)
print(17*3600)
print(19*3600+50*60)
print(ntime.strftime("%Y%m%d%H%M%S"))