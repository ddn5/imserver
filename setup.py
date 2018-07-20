from distutils.core import setup
# from setuptools import setup
setup(name = "imserver",
    version = "1.0",
    description = "A image / .md / python-code-server ",
    author = "bboy",
    author_email = "bboy@qq.com",
    url = "http://10.24.36.130:8100/imserver/",
    packages = ['imserver'],
    install_requires = ['paste','bottle','markdown'],
    # scripts = ["imserv"],
)
