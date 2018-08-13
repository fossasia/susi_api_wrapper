from setuptools import setup

setup(
    name='susi_python',
    version="0.0.1",
    author='SUSI.AI',
    author_email='susiai@googlegroups.com',
    url='http://susi.ai',
    description='SUSI AI API Python Wrapper',
    long_description_markdown_filename='README.md',
    license='Apache',
    packages=['susi_python'],
    install_requires=['requests', 'youtube-dl', 'geocoder'],
    setup_requires=["setuptools-markdown"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache License",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
