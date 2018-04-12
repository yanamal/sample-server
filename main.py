#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from flask import Flask,redirect,render_template,request
import logging, os

app = Flask(__name__)

# Set up debug messages, when not in "real world" production mode
production_environment = os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')
if not production_environment:
    app.debug = True
    logging.info('debugging!')

@app.route('/')
def hello():
    return redirect('/stat/form.html')

@app.route('/response')
def formresponse():
  fl = request.args.get('flavor')
  something = request.args.get('yourname')
  return render_template('filled_template.html', flavor=fl, name=something)
