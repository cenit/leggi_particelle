from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [Extension(
          name="read_field",
          sources=["lampy/fastread/read_field.pyx"]),
          Extension(
          name="read_phase_space",
          sources=["lampy/fastread/read_phase_space.pyx"])
]

lib_read_binary = ('lib_read_binary',
                 {'sources': ['lampy/fastread/clibs/lib_read_binary.c']})
lib_read_phase_space = ('lib_read_phase_space',
                 {'sources': ["lampy/fastread/clibs/lib_read_phase_space.c"]})

requirements = ['numpy', 'matplotlib', 'Cython', 'scipy']
setup(
    name='lampy',
    version='0.1.dev2',
    description="Python suite to access, manipulate and plot ALaDyn's datas",
    packages=find_packages('.'),
    author='ALaDyn Collaboration',
    maintainer='Davide Terzani',
    maintainer_email='davide.terzani@ino.it',
    license='GNU GPLv3',
    url='https://github.com/ALaDyn/ALaDyn',
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3.7'],
    ext_modules=cythonize(extensions),
    install_requires=[requirements],
    ext_package='lampy/compiled_cython',
    libraries=[lib_read_binary, lib_read_phase_space],
    include_dirs=[numpy.get_include()]
)
