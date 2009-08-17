#!/usr/bin/env python

"Augh!chievements - parse achievement data from the WoW Armory and display it in a pretty fashion."

__author__ = "Freddie (freddie@madcowdisease.org)"

import cPickle
import logging
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
LINK_URL = 'http://www.wowarmory.com/character-sheet.xml?r=%s&n=%s'

CHAR_LEVEL = '80'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6'

DEFAULT_EXPIRE = 8

# ---------------------------------------------------------------------------

class Augh():
	def __init__(self, options):
		self.options = options
		self.qrealm = self.ArmoryQuote(self.options.realm)
		
		# Set up logging
		self.logger = logging.getLogger('augh')
		console = logging.StreamHandler()
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		console.setFormatter(formatter)
		self.logger.addHandler(console)
		
		if self.options.verbose == 1:
			self.logger.setLevel(logging.INFO)
		elif self.options.verbose >= 2:
			self.logger.setLevel(logging.DEBUG)
		
		self.expire_time = time.time() - (self.options.expiretime * 60 * 60)
		
		self.data = {}
		self.metas = achievement_data.get_data()
	
	# -----------------------------------------------------------------------
	# Slightly nasty workaround to get quoted UTF-8 URLs that the Armory expects
	def ArmoryQuote(self, url):
		return urllib.quote(unicode(url, 'latin1').encode('utf-8'))
	
	# -----------------------------------------------------------------------
	# Load data from cache
	def CacheLoad(self, character, force=False):
		# Skip cache if we have to
		if self.options.ignorecache is True and force is False:
			return {}
		
		filename = '%s_%s.pickle' % (self.options.realm, character)
		filepath = os.path.join('cache', filename)
		fexists = os.path.exists(filepath)
		
		load = False
		if force is False:
			if fexists and os.stat(filepath).st_mtime > self.expire_time:
				load = True
		else:
			load = True
		
		if load is True and fexists:
			return cPickle.load(open(filepath))
		else:
			return {}
	
	# Save data to cache
	def CacheSave(self, character):
		filename = '%s_%s.pickle' % (self.options.realm, character)
		filepath = os.path.join('cache', filename)
		cPickle.dump(self.data[character], open(filepath, 'w'))
	
	# -----------------------------------------------------------------------
	
	def go(self):
		self.logger.debug('go() starting')
		
		# Fetch any missing icons
		self.FetchIcons()
		
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
			self.chars = [c for c in self.options.chars.split(',') if c]
		
		# Blow up if there's no valid characters
		if self.chars == []:
			self.logger.error('no valid character names!')
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
			
			broken = self.ParseArmory(*chars)
			if broken is True:
				self.logger.warning('ParseArmory() failed for %r, going single' % (chars))
				
				for char in chars:
					broken = self.ParseArmory(char)
					if broken is True:
						self.logger.warning('giving up on player %s')
		
		# Spit out the HTML
		self.OutputHTML()
		
		self.logger.debug('go() finished')
	
	# -----------------------------------------------------------------------
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
	
	# Fetch the guild player list from the Armory
	def FetchGuildPlayers(self):
		url = GUILD_URL % (self.ArmoryQuote(self.options.realm), self.ArmoryQuote(self.options.guild))
		req = urllib2.Request(url, headers={ 'User-Agent': USER_AGENT })
		
		start = time.time()
		try:
			xml = urllib2.urlopen(req).read()
		except urllib2.HTTPError, e:
			self.logger.warning('FetchGuild() %r HTTP %s!' % (url, e.code))
			return []
		else:
			self.logger.debug('FetchGuild() %r took %.2fs' % (url, time.time() - start))
			root = ET.fromstring(xml)
			
			chars = []
			for character in root.findall('guildInfo/guild/members/character'):
				if character.get('level') == CHAR_LEVEL:
					if self.options.maxrank > 0:
						rank = int(character.get('rank'))
						if rank > self.options.maxrank:
							continue
					
					chars.append(character.get('name').encode('latin-1'))
			
			chars.sort()
			return chars
	
	# Fetch some XML comparison data from the Armory
	def FetchXML(self, characters):
		realms = ','.join([self.qrealm] * len(characters))
		chars = [self.ArmoryQuote(c) for c in characters]
		clist = ','.join(chars)
		
		url = BASE_URL % (realms, clist)
		
		start = time.time()
		req = urllib2.Request(url, headers={ 'User-Agent': USER_AGENT })
		
		try:
			u = urllib2.urlopen(req)
		
		except urllib2.HTTPError, e:
			self.logger.warning('FetchXML() %r/%r HTTP %s!' % (self.options.realm, clist, e.code))
			return None
		
		else:
			xml = u.read()
			self.logger.debug('FetchXML() %r/%r took %.2fs' % (self.options.realm, clist, time.time() - start))
			#open('dump.xml', 'w').write(xml)
			
			# Check for a redirect, that's a failed fetch... sort of. Ugh.
			if not u.geturl().endswith('c=168'):
				return False
			else:
				return xml
	
	# -----------------------------------------------------------------------
	# Fix comment
	def ParseArmory(self, *chars):
		xml = self.FetchXML(chars)
		
		# Got redirected, fail
		if xml is False:
			return True
		
		# FetchXML error of some sort, force a cache load and try the next set
		elif xml is None:
			self.logger.warning('FetchXML() returned None for %r, forcing cache load' % (chars))
			for char in chars:
				c_data = self.CacheLoad(char, force=True)
				if c_data:
					self.data[char] = c_data
				else:
					for meta in self.metas:
						self.data[char][meta.name] = meta.check_achievements({})
			return False
		
		# Find all of the nested categories
		categories = ET.fromstring(xml).findall('category/category')
		
		for meta in self.metas:
			p = {}
			for char in chars:
				p[char] = {}
			
			for achievement in categories[meta.section].findall('achievement'):
				a_title = achievement.get('title')
				
				if len(chars) == 1:
					p[chars[0]][a_title] = achievement.get('dateCompleted', None)
				
				else:
					cs = achievement.findall('c')
					# Someone didn't exist or whatever, we'll have to do them singly. Ugh.
					if len(cs) < len(chars):
						return True
					
					for j, complete in enumerate(cs):
						p[chars[j]][a_title] = complete.get('dateCompleted', None)
			
			for char in chars:
				self.data[char][meta.name] = meta.check_achievements(p[char])
		
		# Cache data for these characters
		for char in chars:
			self.CacheSave(char)
		
		# Sleep for a little while
		time.sleep(random.randint(3, 6))
		
		return False
	
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
				meta_complete, meta_cutoff = meta.check_meta_cutoff(p_data[meta.name])
				
				# Skip people with no meta progress
				if self.options.noslackers and meta_complete is None:
					continue
				
				if p_data.get('url', None) is None:
					p_data['url'] = LINK_URL % (self.qrealm, self.ArmoryQuote(name))
				
				n = (n + 1) % 2
				outfile.write('<tr class="row%s"><td class="name"><a href="%s">%s</a></td>' % (n, p_data['url'], name))
				
				for p_ok in p_data[meta.name]:
					if p_ok is False:
						outfile.write('<td><img src="files/no.png"></td>')
					elif len(p_ok) == 10:
						outfile.write('<td><img src="files/yes.png" title="%s"></td>' % (p_ok))
					else:
						outfile.write('<td class="meta">%s</td>' % (p_ok))
				
				# Completion info
				if meta_complete is True:
					if meta_cutoff is True:
						outfile.write('<td class="star"><img src="files/star.png"></td>')
					else:
						outfile.write('<td class="star"><img src="files/yes.png"></td>')
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
	parser.add_option('-v', '--verbose', dest='verbose', action='count', help="Increase verbosity (specify multiple times for more)")
	parser.add_option('', '--metas', dest='metas', help='comma seperated list of meta achievement names')
	parser.add_option('', '--realm', dest='realm', help='realm characters come from')
	parser.add_option('', '--file', dest='filename', help='file to output generated HTML to', metavar='FILE')
	parser.add_option('', '--title', dest='title', help='title of HTML page')
	parser.add_option('', '--expire-time', dest='expiretime', help='expire cache after N hours', metavar='N')
	parser.add_option('', '--max-rank', type='int', dest='maxrank', help='maximum guild rank to include when using --guild', metavar='N')
	parser.add_option('-i', '--ignore-cache', action='store_true', dest='ignorecache', help='ignore cached data')
	parser.add_option('-n', '--no-slackers', action='store_true', dest='noslackers', help="don't display characters with no meta progress")
	
	group = OptionGroup(parser, 'Character Options', "Pick one of these or I'll cut you")
	group.add_option('', '--guild', dest='guild', help='guild to load character names from')
	group.add_option('', '--charfile', dest='charfile', help='filename to read character names from')
	group.add_option('', '--chars', dest='chars', help='comma seperated list of character names')
	parser.add_option_group(group)
	
	parser.set_defaults(
		verbose=0,
		metas='Glory of the Raider (25 player),Glory of the Ulduar Raider (25 player)',
		ignorecache=False,
		noslackers=False,
		expiretime=8,
		maxrank=0,
	)
	
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
