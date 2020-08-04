# Read the "README.rst" for project description
with open('README.rst', 'r', encoding='utf8') as f:
    readme = f.read()
    
from setuptools import setup, Extension
from IRFLife import __version__

if __name__ == '__main__':
    setup(
        name='IRFLife',
        version=__version__,
        author='Lorenzo Capponi',
        author_email='lorenzocapponi@outlook.it',
        description='Termoelasticity-based fatigue life identification',
        url='https://github.com/LolloCappo/IR-FLife',
        py_modules='IRFLife',
        long_description=readme,
        long_description_content_type="text/markdown",
        install_requires = ['numpy','tqdm','FLife']
    )
