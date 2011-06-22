#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, string, codecs;
#from xml.dom import minidom;
#from xml import xpath;

sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);
sys.stdin = codecs.getwriter('utf-8')(sys.stdin);

def calc_tabs(par): #{
	tabs = '\t';
	if len(par.decode('utf-8')) <= 23: #{
		tabs = tabs + '\t';
	#}
	if len(par.decode('utf-8')) <= 15: #{
		tabs = tabs + '\t';
	#}
	if len(par.decode('utf-8')) < 8: #{
		tabs = tabs + '\t';
	#}
	return tabs;
#}

if len(sys.argv) < 2: #{
	print 'paradigm-review.py <dix file>';
	sys.exit(-1);
#}

d = sys.argv[1];

pardefs = {};
e_count = 0;
u_count = 0;
inpar = False;
inmain = False;
parname = '';
pos = {};

for line in file(d).read().split('\n'): #{
#	print >> sys.stderr , line;
	if line.strip()[0:4] == '<!--': #{
		continue;
	#} 

	if line.count('<pardef n="') > 0: #{
		inpar = True;
		parname = line.split('"')[1];
		pardefs[parname] = {};
		pardefs[parname]['e'] = 0;
		pardefs[parname]['u'] = 0;
		if line.count('__') < 1: #{
			continue;
		#}
		ppos = line.split('__')[1].split('"')[0];
		if ppos in pos: #{
			pos[ppos] = pos[ppos] + 1;
		else: #{
			pos[ppos] = 0;
		#}
	#}

	if inpar == True and line.count('<e') > 0: #{
		pardefs[parname]['e'] = pardefs[parname]['e'] + 1;
	#}

	if line.count('</pardef>') > 0: #{
		inpar = False;
	#}
	
	if line.count('<section') > 0: #{
		inmain = True;
	#}

	if line.count('</section>') > 0: #{
		inmain = False;
	#}
	
	if inmain == True and line.count('<e') > 0: #{
		parname = line.replace('<par n="', '@').split('@')[1].split('"')[0];
		if parname not in pardefs: #{
			print 'Paradigm "' + parname + '" not found.';
#			sys.exit(-1);
			continue;
		#}
		pardefs[parname]['u'] = pardefs[parname]['u'] + 1;
		parname = '';
	#}
#}

unused_pars = {};

for c in pos.keys(): #{
	print '';
	print '====== ' + c + ' ' + ('=' * (76 - len('=== ' + c)));
	print 'Name\t\t\t\tEntries\t\tUsed by';
	print '================================================================================';
	print '';
	for p in pardefs.keys(): #{
		if p.count('__') < 1: #{
			continue;
		#}
		if p.split('__')[1] == c > 0: #{
			print p + calc_tabs(p) + str(pardefs[p]['e']) + '\t\t' + str(pardefs[p]['u']);
		#}
		if pardefs[p]['u'] == 0: #{
			unused_pars[p] = pardefs[p];
		#}
	#}
#}

print '================================================================================';
print '================================================================================';
print 'Name\t\t\t\tEntries\t\tUsed by';

for c in pos.keys(): #{
	for p in unused_pars.keys(): #{

		if p.count('__') < 1: #{
			continue;
		#}
		if p.split('__')[1] == c > 0: #{
			print p + calc_tabs(p) + str(pardefs[p]);
		#}
	#}
#}
