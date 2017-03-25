from setuptools import setup, find_packages
setup(
    name='origin-core',
    version='1.0',
    packages=find_packages(),
    license='',
    long_description=open('README.txt').read(),
    author='e-tuchs',
    author_email='xuwulin0@gmail.com',
    maintainer='origin',
    url='http://www.lapduck.com/',
    package_data = {
            "origincore": ['locale/zh_CN/LC_MESSAGES/*.mo'],
        }
)

