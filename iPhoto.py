import argparse
import glob
import md5
import os
import plistlib

xmp_template = '''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:exif="http://ns.adobe.com/exif/1.0/">
    <exif:GPSLatitude>{0}</exif:GPSLatitude>
    <exif:GPSLongitude>{1}</exif:GPSLongitude>
    <exif:GPSMapDatum>WGS-84</exif:GPSMapDatum>
    <exif:GPSVersionID>2.2.0.0</exif:GPSVersionID>
  </rdf:Description>
</rdf:RDF>
<?xpacket end="w"?>
'''

def setup_args():
	args = argparse.ArgumentParser(description='Write iPhoto/Aperture geotag metadata to XMP sidecar files.')
	args.add_argument( 'path', type=str, help='Path of the iPhoto/Aperture library. Ex: ~/Pictures/iPhoto\\ Library')
	args.add_argument( '--verbose', action='store_true', help='Output paths of XMP files')
	args.parse_args()
	return args

def format_coord( coord, dir ):
	dir = dir[0] if coord < 0 else dir[1]
	coord = abs( coord )
	output = '%i,%f%s' % ( int(coord), ( coord - int(coord) ) * 60, dir )
	return output

args = setup_args()

# Read locations
album_data = plistlib.readPlist( os.path.join( args.path, 'AlbumData.xml' ) )
image_list = album_data['Master Image List']
for key, image in image_list.iteritems():
	try:
		path = image['OriginalPath']
	except KeyError:
		path = image['ImagePath']
	if not '/Masters/' in path:
		# Only update the original images
		continue
	try:
		latitude = format_coord( image['latitude'], 'SN' )
		longitude = format_coord( image['longitude'], 'WE' )
	except KeyError:
		# No Geotag data
		continue
	xmp_path = '.'.join( [ path.rsplit( '.', 1 )[0], 'xmp' ] )
	if args.verbose:
		print xmp_path
	xmp_data = xmp_template.format( latitude, longitude )
	xmp = open( xmp_path, 'w' )
	xmp.write( xmp_data )
	xmp.close()
