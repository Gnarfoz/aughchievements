#!/usr/bin/env python

"dump meta data from the armory"

import urllib
import urllib2

import xml.etree.ElementTree as ET


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1'
YAMAKI_URL = 'http://www.wowarmory.com/character-achievements.xml?r=Dragonblight&n=Yamaki&c=168'


def main():
	req = urllib2.Request(YAMAKI_URL, headers={ 'User-Agent': USER_AGENT })
	u = urllib2.urlopen(req)
	data = u.read()
	
	categories = ET.fromstring(data).findall('category/category')
	
	for i, cat in enumerate(categories):
		print
		print "m = Meta('', '', %d)" % (i)
		print 'm.add_achievements('
		
		for achievement in cat.findall('achievement'):
			print '(%r, %s, %r),' % (achievement.get('title'), achievement.get('id'), achievement.get('icon'))
		
		print ')'

if __name__ == '__main__':
	main()
