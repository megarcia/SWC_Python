# Download function, just provide full URL (with path) and file name
# Uses pycurl (web retrieval) and certifi (local SSL certification finder)
# For use with Software Carpentry Python exploratory data analysis
#
# before using this, at command prompt:
#     python -c "import pycurl"
#     python -c "import certifi"
#
# if one or both return an error, you need to install that package:
#     conda install <package name>
#
# (if you used Anaconda as your Python installer, you probably only need certifi)
#

import pycurl
try:
    import certifi
    https = 1
except ImportError:
    https = 0

def get_file(base_url,fname):
    """Download web-based file using pycurl with SSL security via certifi"""
    print('Downloading %s' % fname)
    print('from %s' % base_url)
    c = pycurl.Curl()
    f = open(fname,'wb')
    if https:
        c.setopt(pycurl.CAINFO, certifi.where())
        print('- Using http-secure transfer protocol')
    else:
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        print('- Using unsecure http transfer protocol')
    c.setopt(c.URL, base_url+fname)
    c.setopt(c.WRITEDATA, f)
    c.perform()
    responsecode = c.getinfo(c.RESPONSE_CODE)
    if responsecode == 200:
        print('- Status: OK')
        print('- Elapsed time: %f sec' % c.getinfo(c.TOTAL_TIME))
    else:
        print('- Status: ERROR, response code %d' % responsecode)
    c.close()
    print(' ')
    return
