from setuptools import setup, find_packages


setup(
    name='zaifdata',
    version='0.0.1',
    description='Open datasets of zaif exchange for traders',
    long_description='',
    url='https://github.com/techbureau/zaifdata',
    author='DaikiShiroi',
    author_email='daikishiroi@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    license='MIT',
    keywords='zaif bit-coin btc xem mona jpy virtual currency block chain bot trading',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'requests',
        'pandas',
    ],
    extras_require={
        'indicators': ['TA-Lib']
    },
)
