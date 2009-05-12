#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Payyans Ascii to Unicode Convertor
# Copyright 2008-2009 Santhosh Thottingal <santhosh.thottingal@gmail.com>,
# Nishan Naseer <nishan.naseer@gmail.com>, Manu S Madhav <manusmad@gmail.com>,
# Rajeesh K Nambiar <rajeeshknambiar@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# If you find any bugs or have any suggestions email: santhosh.thottingal@gmail.com
# URL: http://www.smc.org.in

'''
പയ്യന്‍ ആളു തരികിടയാകുന്നു. ആസ്കി വേറൊരു തരികിടയും.
തരികിടയെ തരികിടകൊണ്ടു നേരിടുന്നതാണു് ബുദ്ധി.
അമേരിക്കാ-ഇറാഖ് യുദ്ധം താഴെപ്പറയും വിധമാകുന്നു.
'''

'''ആവശ്യത്തിനുള്ള കോപ്പുകള്‍ കൂട്ടുക '''
import sys #കുന്തം
import codecs #കൊടച്ചക്രം
import os #ശീലക്കുട
from common import * 
'''പയ്യന്റെ ക്ലാസ് ഉന്നതകുലമാകുന്നു. ച്ചാല്‍ ആഢ്യന്‍ തന്നെ. ഏ ക്ലാസ് പയ്യന്‍...!'''
class Payyans(SilpaModule):

	def __init__(self):
		self.input_filename =""
		self.output_filename=""
		self.mapping_filename=""
		self.rulesDict=None
		self.pdf=0
		
	def word2ASCII(self, unicode_text):
		index = 0
		prebase_letter = ""
		ascii_text=""
		self.direction = "u2a"
		self.rulesDict = self.LoadRules()
		while index < len(unicode_text):
			'''കൂട്ടക്ഷരങ്ങള്‍ക്കൊരു കുറുക്കുവഴി'''
			for charNo in [3,2,1]:
				letter = unicode_text[index:index+charNo]
				if letter in self.rulesDict:
					ascii_letter = self.rulesDict[letter]
					letter = letter.encode('utf-8')
					'''കിട്ടിയ അക്ഷരങ്ങളുടെ അപ്പുറത്തും ഇപ്പുറത്തും സ്വരചിഹ്നങ്ങള്‍ ഫിറ്റ് ചെയ്യാനുള്ള ബദ്ധപ്പാട്'''
					if letter == 'ൈ':	# പിറകില്‍ രണ്ടു സാധനം പിടിപ്പിക്കുക
						ascii_text = ascii_text[:-1] + ascii_letter*2 + ascii_text[-1:]
					elif (letter == 'ോ') | (letter == 'ൊ') | (letter == 'ൌ'):		#മുമ്പിലൊന്നും പിറകിലൊന്നും
						ascii_text = ascii_text[:-1] + ascii_letter[0] + ascii_text[-1:] + ascii_letter[1]
					elif (letter == 'െ') | (letter == 'േ') |(letter == '്ര'):		#പിറകിലൊന്നുമാത്രം
						ascii_text = ascii_text[:-1] + ascii_letter + ascii_text[-1:]
					else:
						ascii_text = ascii_text + ascii_letter						
					index = index+charNo
					break
				else:
					if(charNo==1):
						index=index+1
						ascii_text = ascii_text + letter
						break;
					'''നോക്കിയിട്ടു കിട്ടുന്നില്ല ബായി'''				
					ascii_letter = letter
					#ascii_text = ascii_text + ascii_letter
					#index = index+1

		return ascii_text
		
	def Uni2Ascii(self):
		'''പണിതുടങ്ങട്ടെ'''
		if self.input_filename :
			uni_file = codecs.open(self.input_filename, encoding = 'utf-8', errors = 'ignore')
		else :
			uni_file = codecs.open(sys.stdin, encoding = 'utf-8', errors = 'ignore')			
		text = ""
		if self.output_filename :
			output_file = codecs.open(self.output_filename, encoding = 'utf-8', errors = 'ignore',  mode='w+')			
		while 1:
   			text =uni_file.readline()
			if text == "":
				break
			ascii_text = ""	
			# ഹീന ജാതിയിലേയ്ക്ക് തരം താഴ്ത്ത്വാ !
			ascii_text = self.word2ASCII(text)
									
			if self.output_filename :
				output_file.write(ascii_text)
			else:
				print ascii_text.encode('utf-8')
		''' പയ്യന്‍ നല്ലോരു യൂണിക്കോട് ഫയലില്‍ കേറി നെരങ്ങി ആസ്ക്കിയാക്കി. ദൈവമേ, ഈ പയ്യനു നല്ലബുദ്ധി തോന്നിക്കണേ... '''
		return 0
		
	def word2Unicode(self, ascii_text):
		index = 0
		post_index = 0
		prebase_letter = ""
		postbase_letter = ""	# "‌‌്യ", "്വ"
		unicode_text = ""
		next_ucode_letter = ""
		self.direction="a2u"
		self.rulesDict = self.LoadRules()
		while index < len(ascii_text):
			for charNo in [2,1]:
				letter = ascii_text[index:index+charNo]
				if letter in self.rulesDict:
					unicode_letter = self.rulesDict[letter]
					if(self.isPrebase(unicode_letter)):	#സ്വരചിഹ്നമാണോ?
						prebase_letter = unicode_letter
					else:					#സ്വരചിഹ്നമല്ല
						#എങ്കില്‍ വ്യഞ്ജനത്തിനു ശേഷം പോസ്റ്റ്-ബേസ് ഉണ്ടോ എന്നു നോക്കൂ
						post_index = index+charNo
						if post_index < len(ascii_text):
							letter = ascii_text[post_index]
							if letter in self.rulesDict:
								next_ucode_letter = self.rulesDict[letter]
								if self.isPostbase(next_ucode_letter):
									postbase_letter = next_ucode_letter
									index = index + 1
						if  ((unicode_letter.encode('utf-8') == "എ") |
						    ( unicode_letter.encode('utf-8') == "ഒ" )):
							unicode_text = unicode_text + postbase_letter + self.getVowelSign(prebase_letter , unicode_letter)
						else:
							unicode_text = unicode_text + unicode_letter + postbase_letter + prebase_letter
						prebase_letter=""
						postbase_letter=""
					index = index + charNo
					break
				else:
					if charNo == 1:
						unicode_text = unicode_text + letter
						index = index + 1
						break
					unicode_letter = letter
		return unicode_text	# മതം മാറ്റി തിരിച്ചു കൊടുക്ക്വാ ! 
	
	def Ascii2Uni(self):
		if self.pdf :
			command = "pdftotext '" + self.input_filename +"'"
			process = os.popen(command, 'r')
			status = process.close()
			if status:
				print "The input file is a PDF file. To convert this the  pdftotext  utility is required. "
				print "This feature is available only for GNU/Linux Operating system."
				'''ഊഹും. കൊന്നാലും ഇനി മുന്നോട്ടില്ല. മുന്നില്‍ മറ്റവനാകുന്നു. ഏതു്? '''
				return 1	# Error - no pdftotext !
			else:
				self.input_filename =  os.path.splitext(self.input_filename)[0] + ".txt"
		if self.input_filename :
			ascii_file = codecs.open(self.input_filename, encoding = 'utf-8', errors = 'ignore')
		else :
			ascii_file = codecs.open(sys.stdin, encoding = 'utf-8', errors = 'ignore')			
		
		text = ""
		if self.output_filename :
			output_file = codecs.open(self.output_filename, encoding = 'utf-8', errors = 'ignore',  mode='w+')			
	
		'''സത്യമുള്ളടത്തോളം... അതുകൊണ്ടു തന്നെ ടെര്‍മിനേഷന്‍ ഉറപ്പു്'''	
		while 1:
   			text =ascii_file.readline()
			if text == "":
				break
			unicode_text = ""
			''' അങ്ങട്ട് മതം മാറ്റ്വാ... ആസ്കിതനും നാസ്തികനും ഒന്നന്നെ! '''
			unicode_text = self.word2Unicode(text)
			
			if self.output_filename :
				output_file.write(unicode_text)
			else:
				print unicode_text.encode('utf-8')

		''' പയ്യന്റെ അവതാരോദ്ദേശ്യം പൂര്‍ണ്ണമായിരിക്കുന്നു. ഇനി മടക്കം. റിട്ടേണ്‍...! '''
		return 0

	def getVowelSign(self, vowel_letter, vowel_sign_letter):
		vowel=  vowel_letter.encode('utf-8')
		vowel_sign=  vowel_sign_letter.encode('utf-8')
		if vowel == "എ":
			if vowel_sign == "െ":
				return "ഐ"
		if vowel == "ഒ":
			if vowel_sign == "ാ":
				return "ഓ"
			if vowel_sign =="ൗ":
				return "ഔ"
		return (vowel_letter+ vowel_sign_letter)

	def isPrebase(self, letter):
		 '''
		 ഇതെന്തിനാന്നു ചോദിച്ചാ, ഈ അക്ഷരങ്ങളുടെ ഇടതു വശത്തെഴുതുന്ന സ്വര ചിഹ്നങ്ങളുണ്ടല്ലോ?
		 അവ ആസ്കി തരികിടയില്‍ എഴുതുന്നതു് ഇടതു വശത്തു തന്നെയാ. യൂണിക്കോഡില്‍ അക്ഷരത്തിനു ശേഷവും
		 അപ്പൊ ആ വക സംഭവങ്ങളെ തിരിച്ചറിയാനാണു് ഈ സംഭവം.
		 "തരികിട തരികിടോ ധീംതരികിട" (തരികിട തരികിടയാല്‍)  എന്നു പയ്യന്റെ ഗുരു പയ്യഗുരു പയ്യെ മൊഴിഞ്ഞിട്ടുണ്ടു്. 
		 '''
		 unicode_letter = letter.encode('utf-8')
		 if(   ( unicode_letter == "േ"  ) | (   unicode_letter ==  "ൈ" ) |   ( unicode_letter ==  "ൊ" ) 	| ( unicode_letter ==  "ോ"  ) |  ( unicode_letter == "ൌ"  )
		 			|  ( unicode_letter == "്ര"  )  |  ( unicode_letter == "െ"  ) 
		 			 ):
			return True #"ഇതു സത്യം... അ...സത്യം.... അസത്യം...!"
		 else:
			return False
			
	def isPostbase(self, letter):
		'''
		"ക്യ" എന്നതിലെ "്യ", "ക്വ" എന്നതിലെ "്വ" എന്നിവ പോസ്റ്റ്-ബേസ് ആണ്.
		"ത്യേ" എന്നത് ആസ്കിയില്‍ "ഏ+ത+്യ" എന്നാണ് എഴുതുന്നത്. അപ്പോള്‍ വ്യഞ്ജനം കഴിഞ്ഞ് പോസ്റ്റ്-ബേസ്
		ഉണ്ടെങ്കില്‍ വ്യഞ്ജനം+പോസ്റ്റ്-ബേസ് കഴിഞ്ഞേ പ്രീ-ബേസ് ചേര്‍ക്കാവൂ! ഹൊ, പയ്യന്‍ പാണിനീശിഷ്യനാണ്!!
		'''
		unicode_letter = letter.encode('utf-8')
		if ( (unicode_letter == "്യ") | (unicode_letter == "്വ") ):
			return True
		else:
			return False
					
	def LoadRules(self):	
		'''
		ഈ സംഭവമാണു് മാപ്പിങ്ങ് ഫയല്‍ എടുത്തു് വായിച്ചു പഠിക്കുന്നതു്.
		'''
		if(self.rulesDict):
			return self.rulesDict
		rules_dict = dict()
		line = []
		line_number = 0
		rules_file = codecs. open(self.mapping_filename,encoding='utf-8', errors='ignore')
		while 1:
			''' ലൈന്‍ നമ്പര്‍ , മാപ്പിങ്ങ് ഫയലില്‍ തെറ്റുണ്ടെങ്കില്‍ പറയാന്‍ ആവശ്യാണു് '''
			line_number = line_number +1 
   			text = unicode( rules_file.readline())
			if text == "":
			      break
			'''കമന്റടിച്ചേ മത്യാവൂന്നു വെച്ചാ ആവാം. ഒട്ടും മുഷിയില്ല്യ'''      
			if text[0] == '#': 
			      continue 
			      ''' കമന്റടി പതിവുപോലെ മൈന്റ് ചെയ്യണ്ട ഒന്നും കണ്ടില്യാ കേട്ടില്യാന്നു വെച്ചു നടന്നോളൂ(മനസ്സില്‍ ചിരിച്ചോളൂ) ''' 
			line = text.strip()
			if(line == ""):
				  continue 
				  '''ലൈനൊന്നും ല്യാ, മോശം.. ങും പോട്ടെ. വേറെ ലൈന്‍ പിടിക്കാം'''
			if(len(line.split("=")) != 2):
					'''എന്തോ പ്രശ്നണ്ടു്. ന്നാ അതങ്ങടു തുറന്നു പറഞ്ഞേക്കാം'''
					print "Error: Syntax Error in the Ascii to Unicode Map in line number ",  line_number
				  	print "Line: "+ text
				  	'''പരിപാടി നിര്‍ത്താം '''
				  	return 2	# Error - Syntax error in Mapping file 
			'''ഇടതന്‍'''				  	
	 		lhs = line.split("=") [ 0 ]  
	 		'''വലതന്‍'''
	 		rhs = line.split("=") [ 1 ]  
	 		'''ഇതിനിടക്കിനി മൂന്നാമനു സ്കോപ്പിണ്ടോ? '''
	 		'''മറക്കാതെ ഇരിക്കട്ടെ. ആവശ്യം വരും '''
			if self.direction == 'a2u':
				rules_dict[lhs]=rhs
			else:
				rules_dict[rhs]=lhs
		return rules_dict
	
	def process(self,form):
		response = """
		<h2>ASCII to Unicode Conversion</h2></hr>
		<p>Enter the text for detecting the language in the below text area.
		</p>
		<form action="" method="post">
		<textarea  name='input_text' id='id1'>%s</textarea><br/>
		Select Font : <select id="font" name="%s" style="width:12em;">
		<option value="karthika">Karthika</option>
		<option value="bhavana">Bhavana</option>
		<option value="revathi">Revathi</option>
		<option value="ambili">Ambili</option>
		<option value="manorama">Manorama</option>
		</select>
		<input  type="submit" id="Convert To Unicode" value="%s"  name="action" style="width:12em;"/>
		</br>
		</form>
		"""
		action=form['action'].value.decode('utf-8')	
		if(action=="To Unicode"):
			if(form.has_key('input_text')):
				text = form['input_text'].value	.decode('utf-8')
				response=response % (text,"a2ufont", form['action'].value.decode('utf-8')	)
				if(form.has_key('a2ufont')):
					font = form['a2ufont'].value	.decode('utf-8')
					self.mapping_filename="./modules/payyans/maps/"+font+".map"
					if (len(text)>0):
						result = "<p> "+self.word2Unicode(text) .replace('\n', '<br/>') +"</p>"
					else :
						result=""
					response=response+result
			else:
				response=response % ("","a2ufont", form['action'].value.decode('utf-8')	)			
		if(action=="To ASCII"):
			if(form.has_key('input_text')):
				text = form['input_text'].value	.decode('utf-8')
				response=response % (text,"u2afont", form['action'].value.decode('utf-8')	)
				if(form.has_key('u2afont')):
					font = form['u2afont'].value	.decode('utf-8')
					self.mapping_filename="./modules/payyans/maps/"+font+".map"
					if (len(text)>0):
						result = "<p> "+self.word2Unicode(text) .replace('\n', '<br/>') +"</p>"
					else :
						result=""
					response=response+result	
			else:
				response=response % ("","u2afont", form['action'].value.decode('utf-8')	)						
		return response	
	def get_module_name(self):
		return "Payyans Unicode-ASCII Converter"
	def get_info(self):
		return 	"ASCII data - Unicode Convertor based on font maps"	
def getInstance():
	return Payyans()
	

	
