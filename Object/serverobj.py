#!/usr/bin/python
# -*- coding: utf-8 -*-
#License BSD
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import ConfigParser
import os
import io
import StringIO

class Server:
	def __init__(self):
		self.loginserverport = 0
		self.mapserverport = 0
		self.webserverport = 0
		self.serveraddress = ""
		self.defaultgmlevel = 0
		self.gmlevel = {}
		self.loginevent = 0
		self.clientlistcount = 0
		self.clientlist = {}
		self.packethandle = {}
		self.clientlistcount_map = 0
		self.clientlist_map = {}
		self.packethandle_map = {}
		self.enableattackhandle = False
		self.cfg = None #ConfigParser.SafeConfigParser()
		self.readhandle = None #open(path, "rb")
		self.writehandle = None #open(path, "wb")
	
	def setlibdic(self, libdic, selfx=None):
		if not selfx:
			selfx = self
		selfx.libdic = libdic
		#selfx.__dict__.update(self.libdic) #danger
		for attr, value in selfx.libdic.items():
			if attr in selfx.__dict__.keys():
				print "[ lib ]", "error / attribute repeated /", attr
				continue
			selfx.__dict__[attr] = value
	
	def csv(self, var):
		var = var.split(",")
		while True:
			try:
				var.remove("")
			except:
				break
		return var
	
	def loadallconfig(self, ConfigFileName):
		self.readhandle = open("./%s"%ConfigFileName, "rb")
		content = self.readhandle.read()
		self.readhandle.close()
		contentcopy = content
		contenthead_typea = content[:2].encode("hex").upper()
		contenthead_typeb = content[:3].encode("hex").upper()
		if contenthead_typea == "FEFF": #if do not upper, use typea == "feff"
			content = content[2:]
		elif contenthead_typea == "FFFE":
			content = content[2:]
		elif contenthead_typeb == "EFBBBF":
			content = content[3:]
		if len(content) != len(contentcopy):
			self.readhandle = open("./%s"%ConfigFileName, "wb")
			self.readhandle.write(content)
			self.readhandle.close()
		self.readhandle.close()
		
		vmcfg = StringIO.StringIO(content.replace("\r\n", "\n"))
		self.cfg = ConfigParser.SafeConfigParser()
		self.cfg.readfp(vmcfg)
		vmcfg.close()
		try:
			self.loginserverport = int(self.cfg.get("main", "loginserverport"))
			self.mapserverport = int(self.cfg.get("main", "mapserverport"))
			self.webserverport = int(self.cfg.get("main", "webserverport"))
			self.serveraddress = self.cfg.get("main", "serveraddress")
			self.defaultgmlevel = int(self.cfg.get("player", "defaultgmlevel"))
			self.loginevent = int(self.cfg.get("player", "loginevent"))
			cmds = self.cfg.options("gmlevel")
			for cmd in cmds:
				self.gmlevel[cmd] = int(self.cfg.get("gmlevel", cmd))
		except ConfigParser.NoOptionError, e:
			print e
	
	def saveallconfig(self, ConfigFileName):
		if ConfigFileName.find("..") != -1:
			return
		self.cfg = ConfigParser.SafeConfigParser()
		self.cfg.add_section("main")
		self.cfg.add_section("player")
		self.cfg.add_section("gmlevel")
		self.cfg.set("main","loginserverport", str(self.loginserverport))
		self.cfg.set("main","mapserverport", str(self.mapserverport))
		self.cfg.set("main","webserverport", str(self.webserverport))
		self.cfg.set("main","serveraddress", str(self.serveraddress))
		self.cfg.set("player","defaultgmlevel", str(self.defaultgmlevel))
		self.cfg.set("player","loginevent", str(self.loginevent))
		for cmd, gmlevel in self.gmlevel.iteritems():
			self.cfg.set("gmlevel", cmd, str(gmlevel))
		vmcfg = StringIO.StringIO()
		self.writehandle = open("./%s"%ConfigFileName, "wb")
		self.cfg.write(vmcfg)
		self.writehandle.write(vmcfg.getvalue().replace("\r\n", "\n").replace("\n", "\r\n"))
		self.writehandle.close()