# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 16:02:10 2022

@author: DELL
"""

import base64
open_icon = open("followme.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = '%s'" % b64str
f = open("icon.py","w+")
f.write(write_data)
f.close()