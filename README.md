# iphoto-xmp
Save iPhoto geotags to XMP sidecar files

Since Apple no longer supports iPhoto or Aperture, existing libraries must be migrated to new photo management tools.  Adobe Lightroom is one option and it has import support, but it doesn't capture all of the data.  It will migrate geotag data in the original/master file, but not location information that was added through the iPhoto/Aperture UI.

This is a simple script that will go through all photos in your library and write out the geotagged location data to an XMP sidecar file to preserve it.  This will overwrite any existing XMP file since iPhoto doesn't use them.

## Requirements
Written for Python 2.7.10 and iPhoto 9.6.1 or Aperture 3.6