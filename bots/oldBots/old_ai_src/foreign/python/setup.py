from distutils.core import setup, Extension

module1 = Extension('xpai',
                    sources = ['pyxpilotai.c'],
					libraries = ['xpilot_ai'])


setup (name = 'xpai',
       version = '1.0',
       description = 'Xpilot-AI',
       ext_modules = [module1])


