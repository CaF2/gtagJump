# -*- coding:utf-8 -*-

import os
from collections import defaultdict

from pprint import pprint

def read_etags(path,identifier):
	cur_path = path
	etags = None
	while 1:
		try:
			etags = open(
				cur_path + '/TAGS',
				'r',
				encoding='ascii',
				errors='surrogateescape'
			)
			break
		except FileNotFoundError:
			val = os.path.split(cur_path)
			cur_path = val[0]
			prev_dir = val[1]
			if not prev_dir:
				return None
	data = etags.read().split('\x0c')
	defs = defaultdict(list)

	if data[0]:
		raise Exception("etags TAGS should start with x0c")
	for section in data[1:]:
		lines = section.split('\n')
		if len(lines) < 3:
			raise Exception("etags TAGS section should have at least 3 lines")
		if lines[-1]:
			raise Exception(
				"etags TAGS data lines should have end of line character"
			)
		if lines[0]:
			raise Exception("etags TAGS should have x0c on separate line")
		val = lines[1].rsplit(',', 1)
		filename = val[0]
		data_size = val[1]
		if not data_size.isdigit():
			raise Exception("etags TAGS data_size should be integer number")
		for line in lines[2:-1]:
			val = line.split('\x7f',1)
			tag_definition = val[0]
#			print("val "+ line)
			if len(val)>=2:
				rest = val[1]
			else:
				rest = ""
			
			tag_definition = tag_definition.strip()
			if '\x01' in rest:
				val = rest.split('\x01',1)
				tagname = val[0]
				location = val[1]
			else:
				tagname = tag_definition
				location = rest
			val = location.split(',',1)
			line_number = val[0]
			
			if len(val)>=2:
				byte_offset = val[1]
			else:
				byte_offset = ""
			
			if tagname.find(identifier)!=-1:
				rpath=cur_path + "/"+filename
				
				if os.path.isfile(rpath) != True:
					rpath=filename
				
				defs[tagname].append([
					rpath,
					line_number,
					byte_offset,
					tag_definition
				])
				
	return defs


class EtagsNavigator:
	"""
	parses etags TAGS format https://en.wikipedia.org/wiki/Ctags#Etags_2
	"""

	def getDefinitions(self, doc, identifier):
		doc_path = os.path.dirname(
			os.path.realpath(doc.get_location().get_path())
		)
		
		vararr=read_etags(doc_path, identifier)
		
		realval=None
		
		for k,v in vararr.items():
			
			if k.find(identifier)!=-1:
				
				for vv in v:
					yield vv[0], int(vv[1]), vv[2], doc.get_location().get_path()

	def getReferences(self, doc, identifier):
		pass

