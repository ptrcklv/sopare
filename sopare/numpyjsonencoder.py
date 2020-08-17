#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 - 2018 Martin Kauss (yo@bishoph.org)

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

import base64
import json
import numpy
import sys


class numpyjsonencoder(json.JSONEncoder):

    def default(self, obj):
        #print ("DEBUG numpyjsonencoder:obj" , obj, type(obj)) #pl

        if isinstance(obj, numpy.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = numpy.ascontiguousarray(obj)
                if (cont_obj.flags['C_CONTIGUOUS']):
                    obj_data = cont_obj.data
                else:
                    raise Exception("numpyjsonencoder err: C_CONTIGUOUS not present in object!")
            data_base64 = base64.b64encode(obj_data)
            return dict(__ndarray__= data_base64.decode(), dtype = str(obj.dtype), shape = obj.shape)  #macht ärger in py3.6 - fun fact: in py2.7 b64encode returns a string, in py3 a byte
        # return json.JSONEncoder(self, obj)
        try:
            if isinstance(obj, numpy.int64):
                """ This is a sucking Python bug: https://bugs.python.org/issue24313
                The workaround recommended there is implemented in the following.
                """
                return int(obj)
                #return json.JSONEncoder.default(self, puff) #json has some trouble
            else:
                return json.JSONEncoder.default(self, obj) #pl
        except:
            print (sys.exc_info())
            print ("numpyjsonencoder had to skip an object of type", type(obj))
            print (obj)
        #return json.JSONEncoder(obj) #pl



def numpyjsonhook(obj):
    if isinstance(obj, dict) and '__ndarray__' in obj:
        data = base64.b64decode(obj['__ndarray__'].encode())
        return numpy.frombuffer(data, obj['dtype']).reshape(obj['shape'])
    return obj

