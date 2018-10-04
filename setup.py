from distutils.core import setup, Extension
setup(name='dotstar',
      version='0.2.1',
      ext_modules=[Extension('dotstar', 
                            ['dotstar.c'],
                             include_dirs=['/opt/vc/include'],
                             library_dirs=['/opt/vc/lib'],                                                                                                               libraries=['bcm_host'])])
