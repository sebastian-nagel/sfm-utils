from setuptools import setup

setup(
    name='sfmutils',
    version='2.3.0',
    url='https://github.com/gwu-libraries/sfm-utils',
    author='Social Feed Manager',
    author_email='sfm@gwu.edu',
    packages=['sfmutils'],
    description="Utilities to support Social Feed Manager.",
    platforms=['POSIX'],
    test_suite='tests',
    scripts=['sfmutils/stream_consumer.py', 'sfmutils/find_warcs.py'],
    install_requires=['pytz==2019.3',
                      'requests==2.22.0',
                      'kombu==5.0.2',
                      'librabbitmq==2.0.0',
                      'warcio==1.5.3',
                      'iso8601==0.1.12',
                      'petl==1.2.0',
                      'xlsxwriter==1.1.2',
                      'idna==2.7'],
    tests_require=['mock==2.0.0',
                   'vcrpy==2.0.1',
                   'python-dateutil==2.7.5'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
    ],
)
