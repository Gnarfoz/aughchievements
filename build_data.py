#!/usr/bin/env python

"Quick script to get new meta info."

import os
import sys
import urllib


def main():
	if len(sys.argv) < 2:
		print 'supply some arguments, fool'
		sys.exit(1)
	
	for url in sys.argv[1:]:
		data = urllib.urlopen(url).read()
		
		a_id = FindChunk(data, '<h4>Achievement #', '</h4>')
		a_title = FindChunk(data, ' /></a> ', '</h1>')
		
		print "m = Meta(%r, )" % (a_title)
		print 'm.add_achievements('
		
		tooltip = FindChunk(data, '<div id="dview-tooltip" class="tooltip">', '<div style=')
		for td in FindChunks(tooltip, '<td >', '</td>'):
			s_id = FindChunk(td, '"/a/', '/')
			s_title = FindChunk(td, '/">', '</a>')
			print "\t(%r, %s, '-')," % (s_title, s_id)
		
		print ')'

# ---------------------------------------------------------------------------
# Search through text, finding the chunk between start and end.
def FindChunk(text, start, end, pos=None):
	# Can we find the start?
	if pos is None:
		startpos = text.find(start)
	else:
		startpos = text.find(start, pos)
	
	if startpos < 0:
		return None
	
	startspot = startpos + len(start)
	
	# Can we find the end?
	endpos = text.find(end, startspot)
	#if endpos <= startpos:
	if endpos < 0:
		return None
	
	# Ok, we have some text now
	chunk = text[startspot:endpos]
	
	# Return!
	if pos is None:
		return chunk
	else:
		return (endpos+len(end), chunk)

# As above, but return all matches.
def FindChunks(text, start, end, limit=0):
	chunks = []
	n = 0
	
	while 1:
		result = FindChunk(text, start, end, n)
		if result is None:
			return chunks
		else:
			chunks.append(result[1])
			if limit and len(chunks) == limit:
				return chunks
			n = result[0]

# ---------------------------------------------------------------------------

if __name__ == '__main__':
	main()
