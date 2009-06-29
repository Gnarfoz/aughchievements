#!/usr/bin/env python

"Augh!chievements - parse achievement data from the WoW Armory and display it in a pretty fashion."

__author__ = "Freddie (freddie@madcowdisease.org)"

import cPickle
import os
import random
import sys
import time
import urllib
import urllib2
import xml.etree.ElementTree as ET
from optparse import OptionParser, OptionGroup

import achievement_data

# ---------------------------------------------------------------------------

BASE_URL = 'http://www.wowarmory.com/character-achievements.xml?r=%s&n=%s&c=168'
GUILD_URL = 'http://www.wowarmory.com/guild-info.xml?r=%s&gn=%s'
ICON_URL = 'http://www.wowarmory.com/wow-icons/_images/51x51/%s.jpg'

CACHE_TIME = 8 * 60 * 60
CHAR_LEVEL = '80'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6'

# ---------------------------------------------------------------------------

class Augh():
	def __init__(self, options):
		self.options = options
		
		# Characters from a guild list on the armory
		if self.options.guild:
			self.chars = self.FetchGuildPlayers()
		
		# Characters from a text file
		elif self.options.charfile:
			self.chars = []
			for line in open(self.options.charfile):
				self.chars.append(line.strip())
		
		# Characters from the command line
		else:
			self.chars = self.options.chars.split(',')
		
		self.data = {}
		self.metas = achievement_data.get_data()
		
		self.CacheExpire()
	
	# -----------------------------------------------------------------------
	# Slightly nasty workaround to get quoted UTF-8 URLs that the Armory expects
	def ArmoryQuote(self, url):
		return urllib.quote(unicode(url, 'latin1').encode('utf-8'))
	
	# Delete any outdated cache files
	def CacheExpire(self):
		expire_time = time.time() - CACHE_TIME
		for filename in os.listdir('cache'):
			if not filename.endswith('.pickle'):
				continue
			filepath = os.path.join('cache', filename)
			if os.stat(filepath).st_mtime < expire_time:
				os.remove(filepath)
	
	# Load data from cache
	def CacheLoad(self, character):
		# Skip cache if we have to
		if self.options.ignorecache is True:
			return {}
		
		filename = '%s_%s.pickle' % (self.options.realm, character)
		filepath = os.path.join('cache', filename)
		if os.path.exists(filepath):
			return cPickle.load(open(filepath))
		else:
			return {}
	
	# Save data to cache
	def CacheSave(self, character, data):
		filename = '%s_%s.pickle' % (self.options.realm, character)
		filepath = os.path.join('cache', filename)
		cPickle.dump(data, open(filepath, 'w'))
	
	# -----------------------------------------------------------------------
	
	def go(self):
		# Blow up if there's no valid characters
		if not self.chars:
			print 'ERROR: no valid character names'
			sys.exit(2)
		
		# Load any useful people from cache
		fetchme = self.chars[:]
		for char in self.chars:
			c_data = self.CacheLoad(char)
			if c_data:
				fetchme.remove(char)
			self.data[char] = c_data
		
		# Fetch data for up to 4 characters at a time to save time
		for i in range(0, len(fetchme), 4):
			chars = fetchme[i:i+4]
			
			xml = self.FetchXML(chars)
			root = ET.fromstring(xml)
			
			# Find all of the nested categories
			categories = root.findall('category/category')
			
			for meta in self.metas:
				p = {}
				for char in chars:
					p[char] = {}
				
				for achievement in categories[meta.section].findall('achievement'):
					a_title = achievement.get('title')
					
					if len(chars) == 1:
						p[chars[0]][a_title] = achievement.get('dateCompleted', None)
					
					else:
						for j, complete in enumerate(achievement.findall('c')):
							p[chars[j]][a_title] = complete.get('dateCompleted', None)
				
				for char in chars:
					self.data[char][meta.name] = meta.check_achievements(p[char])
			
			# Cache data for these characters
			for char in chars:
				self.CacheSave(char, self.data[char])
			
			# Sleep for a little while
			time.sleep(random.randint(5, 10))
		
		# Fetch any missing icons
		self.FetchIcons()
		
		# Spit out the HTML
		self.OutputHTML()
	
	# -----------------------------------------------------------------------
	# Fetch the guild player list from the Armory
	def FetchGuildPlayers(self):
		url = GUILD_URL % (self.ArmoryQuote(self.options.realm), self.ArmoryQuote(self.options.guild))
		req = urllib2.Request(url, headers={ 'User-Agent': USER_AGENT })
		xml = urllib2.urlopen(req).read()
		root = ET.fromstring(xml)
		
		chars = []
		for character in root.findall('guildInfo/guild/members/character'):
			if character.get('level') == CHAR_LEVEL:
				chars.append(character.get('name').encode('latin-1'))
		print chars
		return chars
	
	# Fetch some XML comparison data from the Armory
	def FetchXML(self, characters):
		qrealm = self.ArmoryQuote(self.options.realm)
		realms = ','.join([qrealm] * len(characters))
		# This is kind of a nasty way to get the right UTF encoding for names
		# containing annoying upper ASCII characters
		chars = [self.ArmoryQuote(c) for c in characters]
		#for character in characters:
		#	c = urllib.quote(unicode(character, 'latin1').encode('utf-8'))
		#	chars.append(c)
		
		url = BASE_URL % (realms, ','.join(chars))
		
		req = urllib2.Request(url, headers={ 'User-Agent': USER_AGENT })
		xml = urllib2.urlopen(req).read()
		#open('temp.xml', 'w').write(xml)
		#xml = open('temp.xml').read()
		return xml
	
	# Fetch any missing achievement icons
	def FetchIcons(self):
		for meta in self.metas:
			for a_id, a_img in meta.achievements.values():
				if a_img == '-':
					continue
				
				filename = '%s.jpg' % (a_img)
				filepath = os.path.join('files', filename)
				if os.path.exists(filepath):
					continue
				
				url = ICON_URL % (a_img)
				req = urllib2.Request(url, headers={ 'User-Agent': USER_AGENT })
				data = urllib2.urlopen(req).read()
				open(filepath, 'wb').write(data)
	
	# -----------------------------------------------------------------------
	# Dump some horrible HTML to our output file
	def OutputHTML(self):
		if self.options.filename:
			outfile = open(self.options.filename, 'w')
		else:
			outfile = sys.stdout
		
		# Massage data into a sorted list of player names
		players = self.data.items()
		players.sort()
		
		# Done parsing, now spit out some horrible HTML
		if self.options.title:
			title = 'Augh!chievements: %s' % (self.options.title)
		else:
			title = 'Augh!chievements'
		
		outfile.write(
"""<html>
<head>
<title>%s</title>
<link href="files/augh.css" rel="stylesheet" type="text/css">
<script src="http://www.wowhead.com/widgets/power.js"></script>
</head>
<body>
""" % (title))
		
		# Only output metas they were interested in
		interested = self.options.metas.split(',')
		
		for findme in interested:
			metas = [z for z in self.metas if z.name == findme]
			if not metas:
				print 'ERROR: unknown meta %r' % (findme)
				continue
			
			meta = metas[0]
			
			
			# Meta table head
			outfile.write(
"""<table>
<thead>
<div class="meta">%s</div>
<tr>
<th></th>
""" % (meta.name))
			
			# Meta table header row
			for a_name in meta.order:
				a_id, a_img = meta.achievements[a_name]
				if a_img == '-':
					a_img = 'unspecified'
				
				if a_id == 0:
					outfile.write(
"""<th><img width=51 height=51 src="files/%s.jpg" title="%s"></th>
""" % (a_img, a_name))
				
				else:
					outfile.write(
"""<th><a href="http://www.wowhead.com/?achievement=%s"><img width=51 height=51 src="files/%s.jpg"></a></th>
""" % (a_id, a_img))
			
			outfile.write(
"""<th></th>
</tr>
""")
			
			# Player rows
			n = 1
			for name, p_data in players:
				n = (n + 1) % 2
				outfile.write('<tr class="row%s"><td class="name">%s</td>' % (n, name))
				
				for p_ok in p_data[meta.name]:
					if p_ok is False:
						outfile.write('<td><img src="files/no.png"></td>')
					elif len(p_ok) == 10:
						outfile.write('<td><img src="files/yes.png" title="%s"></td>' % (p_ok))
					else:
						outfile.write('<td class="meta">%s</td>' % (p_ok))
				
				# All complete?
				trues = [t for t in p_data[meta.name] if t is not False and len(t) == 10]
				if len(trues) == len(p_data[meta.name]):
					outfile.write('<td class="star"><img src="files/star.png"></td>')
				else:
					outfile.write('<td class="star"></td>')
				
				outfile.write('</tr>\n')
			
			outfile.write('</table>\n<br>\n')
		
		now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
		outfile.write('Last updated: %s\n' % (now))
		
		outfile.write(
"""</body>
</html>
""")
		
		outfile.close()

# ---------------------------------------------------------------------------

def main():
	# Parse command line options
	parser = OptionParser()
	parser.add_option('-m', '--metas', dest='metas', help='comma seperated list of meta achievement names')
	parser.add_option('-r', '--realm', dest='realm', help='realm characters come from')
	parser.add_option('-f', '--file', dest='filename', help='file to output generated HTML to', metavar='FILE')
	parser.add_option('-t', '--title', dest='title', help='title of HTML page')
	parser.add_option('-i', '--ignore-cache', action='store_true', dest='ignorecache', help='ignore cached data')
	
	group = OptionGroup(parser, 'Character Options', "Pick one of these or I'll cut you")
	group.add_option('-g', '--guild', dest='guild', help='guild to load character names from')
	group.add_option('', '--charfile', dest='charfile', help='filename to read character names from')
	group.add_option('-c', '--chars', dest='chars', help='comma seperated list of character names')
	parser.add_option_group(group)
	
	parser.set_defaults(metas='Glory of the Ulduar Raider,Heroic: Glory of the Ulduar Raider', ignorecache=False)
	
	(options, args) = parser.parse_args()
	
	# Basic sanity checking
	if options.realm is None:
		parser.error('--realm is required!')
	if options.guild is None and options.charfile is None and options.chars is None:
		parser.error('--guild, --charfile or --chars is required!')
	
	# Go!
	augh = Augh(options)
	augh.go()

if __name__ == '__main__':
	main()
