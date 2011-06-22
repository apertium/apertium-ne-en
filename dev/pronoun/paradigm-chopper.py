#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy, Ft, os;
from Ft.Xml.Domlette import NonvalidatingReader;
from Ft.Xml.XPath import Evaluate;

#from xml.dom import minidom;
#from xml import xpath;

sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

sys.setrecursionlimit(20000);

format = '';

dictionary = sys.argv[1];
print len(sys.argv);
if len(sys.argv) < 2: #{
	print 'python paradigm-chopper.py <dix file> [-1|-1line]';
	sys.exit(-1);
#}
if len(sys.argv) == 3: #{
	if sys.argv[2] == '-1line' or sys.argv[2] == '-1': #{
		format = '1line';
	#}	
#}


if dictionary == os.path.basename(dictionary): #{
	dictionary = os.getcwd() + '/' + dictionary;
#}

doc = NonvalidatingReader.parseUri('file:///' + dictionary);
path = '/dictionary/pardefs/pardef';

paradigms = {};

def return_symlist(symlist): #{
	if len(symlist) < 1: #{
		return '';
	#}
	if symlist[0] == '.': #{
		symlist = symlist[1:];
	#}
	symlist = symlist.replace(':', '.');
	output = '';

	for symbol in symlist.split('.'): #{
		output = output + '<s n="' + symbol + '"/>';
	#}

	return output;
#}

def roll_right(name): #{
	bar_idx = name.find(u'/') + 1;
	udr_idx = name.find(u'_');

	rstring = name[bar_idx:udr_idx];

	if name.find('/') == -1: #{
		rstring = '';
	#}
	
	return rstring;	
#}

def compare_paradigms(paradigm1, paradigm2): #{
	# paradigm,stem,symbols !! paradigm,stem,symbols	
	common = 0;

	if len(paradigm1) != len(paradigm2): #{
		return 0;
	#}

	for pair1 in paradigm1: #{
		for pair2 in paradigm2: #{
			if pair1[0] == pair2[0] and pair1[1] == pair2[1]: #{
				common = common + 1;
			#}
		#}
	#}

	if common == len(paradigm1): #{
		return 1;
	#}
		
	return 0;
#}

def duplicate_exists(p1, p2, duplicates): #{
	for potential in duplicates.keys(): #{
		for potential2 in duplicates[potential]: #{
			if p1 == potential or p1 == potential2: #{
				return 1;
			#}
		#}
	#} 

	return 0;
#}

def string_length_compare(a, b): #{
	if len(a) == len(b): #{
		return 0;
	#}
	if len(a) > len(b): #{
		return 1;
	#}

	return -1;
#}

count = 0;

for node in Ft.Xml.XPath.Evaluate(path, contextNode=doc): #{
        pardef = node.getAttributeNS(None, 'n');

	if pardef not in paradigms: #{
		paradigms[pardef] = [];
	#}

	count = count + 1;
	if count % 1000 == 0: #{
		print >> sys.stderr, count , pardef;
	#}

	for child in Ft.Xml.XPath.Evaluate('.//e', contextNode=node): #{
		for pair in Ft.Xml.XPath.Evaluate('.//p', contextNode=child): #{
			suffix = '';
			left = Ft.Xml.XPath.Evaluate('.//l', contextNode=pair)[0].firstChild;

			if type(left) != type(None): #{
				suffix = left.nodeValue;
			else: #{
				suffix = ''
			#}

			symbols = '';
			right =  Ft.Xml.XPath.Evaluate('.//r', contextNode=pair)[0];
			for sym in Ft.Xml.XPath.Evaluate('.//s', contextNode=right): #{
				symbol = '';
				if type(sym) != type(None): #{
					symbol = sym.getAttributeNS(None, 'n');
				#}
				symbols = symbols + '.' + symbol;
			#}

			p = (suffix, symbols);

			paradigms[pardef].append(p);
		#}
	#}
#}

sorted_paradigms = [];

for item in paradigms.keys(): #{
	sorted_paradigms.append(item);
#}

sorted_paradigms.sort(string_length_compare);

duplicates = {};

def strip_duplicates(paradigms, duplicates, current): #{
#	print 'paradigms: ' , len(paradigms);
	
	for paradigm1 in paradigms.keys(): #{
		if paradigm1 in paradigms and current in paradigms and current != paradigm1: #{
			if current not in duplicates: #{
				duplicates[current] = [];
			#}

			if compare_paradigms(paradigms[paradigm1], paradigms[current]) == 1 and roll_right(paradigm1) == roll_right(current): #{
#				print paradigms[paradigm1] , '; ' , paradigms[current];
				duplicates[current].append(paradigm1);
				del paradigms[paradigm1];
				strip_duplicates(paradigms, duplicates, current);
			#}
		#}
	#}
	return;
#}

#z = copy.deepcopy(paradigms);
for k in sorted_paradigms: #{
	print >> sys.stderr, k;
	strip_duplicates(paradigms, duplicates, k);
#}

print >> sys.stderr, 'Paradigms: ' , len(paradigms);

print >> sys.stderr, '---';

print '<dictionary>';
print '  <pardefs>';
for paradigm in paradigms.keys(): #{
	bar_idx = paradigm.find(u'/') + 1;
	udr_idx = paradigm.find(u'_');

	print '    <pardef n="' + paradigm + '">';
	if format == '1line': #{
	
		for pair in paradigms[paradigm]: #{
			out = '';
			out = out + '      <e><p>';
			if type(pair[0]) == type(None): #{
				out = out + '<l></l>';
			else: #{
				out = out + '<l>' + pair[0] + '</l>';
			#}
			rpost = paradigm[bar_idx:udr_idx];
			if paradigm.find('/') == -1: #{
				rpost = '';
			#}
			out = out + '<r>' + rpost + return_symlist(pair[1]) + '</r></p></e>';
			print out;
		#}	
	else: #{

		for pair in paradigms[paradigm]: #{
			print '      <e>';
			print '        <p>';
			if type(pair[0]) == type(None): #{
				print '          <l/>';
			else: #{
				print('          <l>%s</l>' % (pair[0]));
			#}
			rpost = paradigm[bar_idx:udr_idx];
			if paradigm.find('/') == -1: #{
				rpost = '';
			#}
			print '          <r>' + rpost + return_symlist(pair[1]) + '</r>';
			print '        </p>';
			print '      </e>';
		#}
	#}
	print '    </pardef>';
#}
print '  </pardefs>';
print '  <section id="main" type="standard">';

d = file(dictionary);

output = '';
for line in d.readlines(): #{
        if line.count('<e lm="') > 0: #{
		output = output + line;
        #}

#}

total = 0;
for paradigm in duplicates.keys(): #{
	for p in duplicates[paradigm]: #{
		print >> sys.stderr, '+ ' , p , u' → ' , paradigm;
		output = output.replace('n="' + p + '"', 'n="' + paradigm + '"');
	#}
	total = total + len(duplicates[paradigm]) + 1;
#}

print output;

print '  </section>';
print '</dictionary>';


print >> sys.stderr, '---';
print >> sys.stderr, 'duplicates: ' , len(duplicates) , '; total: ' , total;
print >> sys.stderr, 'paradigms: ' , len(paradigms);
#print >> sys.stderr, 'z: ' , len(z);
