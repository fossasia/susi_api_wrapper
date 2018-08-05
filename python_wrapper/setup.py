from setuptools import setup

setup(
    name='susi_python',
    version="0.0.1",
    author='SUSI.AI',
    author_email='susiai@googlegroups.com',
    url='http://susi.ai',
    description='SUSI AI API Wrapper',
    long_description_markdown_filename='README.md',
    license='Apache',
    packages=['susi_python'],
    install_requires=['requests', 'youtube-dl'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache License",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: SunOS/Solaris",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
