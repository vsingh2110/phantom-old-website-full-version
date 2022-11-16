import urllib
from django.conf import settings
import urlparse
import json
import logging
logger = logging.getLogger('error')
class BaseAPIManager(object):
    def __init__(self, api_url=None):
        self.api_url = api_url
        self.http_url = None
 
    def request(self, args):                
        api_url = args.get('api_url',None)
        if api_url:
            self.api_url = api_url
            args.pop('api_url')
        if not self.api_url:
            raise Exception('api url is mandatory for api call')
            
        if args.get('method','').lower()=='get':
        	self.params = []
        	self.method = 'GET'
        	args.pop('method')
        	self._sort_request(args)        	
        	self._build_http_request()
        else:
        	args.pop('method',None)
                data=args.pop('_data',None)
                if data is not None:
                    self.params = data
                else:
        	    self.params = args
        	self.method = 'POST'
        	self._build_http_request()
 
    def _sort_request(self, args):
        keys = sorted(args.keys())
 
        for key in keys:
            self.params.append(str(key) + '=' + urllib.quote_plus(str(args[key])))
 
    def _build_http_request(self):
		if self.method == 'GET':
			self.query = '&'.join(self.params)
			self.value = self.api_url + '?' + self.query
		else:
			self.value = urllib.urlencode(self.params)

class APIManager(BaseAPIManager):
    def __getattr__(self, name):
        if name in ('lms','cms','solr'):
            def serviceHandler(*args, **kwargs):
                if kwargs:
                    return self._make_request(name, kwargs)
                return self._make_request(name, args[0])
            return serviceHandler
        else:
            return self.__getattribute__(name)

    def __repr__(self):
    	return '<%s object for "%s">' %(self.__class__.__name__,self.api_url)

    def _http_request(self, command, value):

	 	def get_host(command):
			cms_uri = urlparse.urlparse(settings.CMS_URL)
			cms_url = cms_uri.netloc if cms_uri.netloc else cms_uri.path

			lms_uri = urlparse.urlparse(settings.LMS_IP)
			lms_url = lms_uri.netloc if lms_uri.netloc else lms_uri.path

			host_dict = {'cms':cms_url,'lms':lms_url}			
			return host_dict.get(command,lms_url)

		host = get_host(command)
		if self.method=='GET':
			url = "%s/%s" % (self.http_url,value) if self.http_url else "http://%s/api/%s" % (host,value)
			response = urllib.urlopen(url)
		else:
			url = "%s/%s" % (self.http_url,self.api_url) if self.http_url else  "http://%s/api/%s/" % (host,self.api_url)
			response = urllib.urlopen(url,value)
                #import pdb;pdb.set_trace()
		try:			
			return response.read()
		except:
			logger.error('IOError in API Calling: '+self.api_url+' from system: '+command)
 
    def _make_request(self, command, args):
        self.request(args)
        try:
                data = self._http_request(command,self.value)
        	return json.loads(data)
        except (ValueError,IOError),e:
        	logger.error('Value Error in API Calling: '+self.api_url+' from system: '+command)
