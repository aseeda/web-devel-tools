#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import os

def doIt(projName):
    os.mkdir(projName)
    os.mkdir(os.path.join(projName,'templates'))
    
    yamlFilePath = os.path.join(os.getcwd(), projName, 'app.yaml');

    yamlFileHandle = open(yamlFilePath, 'w')

    yamlFileHandle.write("""
application: aelseed-%s
version: 1
runtime: python27
api_version: 1
threadsafe: true

handlers: 
- url: /.*
  script: %s.app

libraries:
- name: jinja2
  version: latest

""" % (projName, projName));

    yamlFileHandle.close();

    scriptFilePath = os.path.join(os.getcwd(), projName, projName + ".py");

    scriptFile = open(scriptFilePath, 'w').write("""
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')

# Setup jinja to look for template files in template/ sub-folder
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **params):
        self.response.out.write(*a, **params)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_str(template, **params))

class MainPage(Handler):
    def get(self):
        self.write("%s is running");
    def post(self):
        pass

app = webapp2.WSGIApplication([("/", MainPage)], debug=True)
""" % projName);

    os.system("dev_appserver.py %s" % projName)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise Exception("Need to specify name of project!");

    doIt(sys.argv[1])
