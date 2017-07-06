import urllib2

def getGPScoord(bd):

	map_str = bd.gps_str

	p1 = map_str.find('http')

	mp_url = map_str[p1:]

	pg = urllib2.urlopen(mp_url)
	newstr = pg.read()
	newstr = newstr.decode("utf8")

	k1 = newstr.find("cacheResponse(")
	ext_str = newstr[k1:k1+100]

	k2 = ext_str.find(']')

	coord = ext_str[17:k2]
	coord = coord.split(',')

	gpsy = float(coord[1])
	gpsx = float(coord[2])

	psx = round(gpsx, 7)
	gpsy = round(gpsy, 7)

	bd.gps_x = gpsx
	bd.gps_y = gpsy