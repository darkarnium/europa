# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

class TDDP(object):
	# Encryption for TP-Link Smart Home Protocol
	# XOR Autokey Cipher with starting key = 171
	# https://github.com/softScheck/tplink-smartplug/
	@staticmethod
	def encrypt(string):
		key = 171
		result = "\0\0\0\0"
		for i in string: 
			a = key ^ ord(i)
			key = a
			result += chr(a)
		return result


	# Decryption for TP-Link Smart Home Protocol
	# XOR Autokey Cipher with starting key = 171
	# https://github.com/softScheck/tplink-smartplug/
	@staticmethod
	def decrypt(string):
		key = 171 
		result = ""
		for i in string: 
			a = key ^ ord(i)
			key = ord(i) 
			result += chr(a)
		return result
