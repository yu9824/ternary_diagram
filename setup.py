from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name='ternary_diagram',
    version='0.0.2',
    description='You can make ternary diagram easily.',
    author='yu-9824',
    author_email='yu.9824@gmail.com',
    install_requires=install_requirements,
    url='https://github.com/yu-9824/ternary_diagram',
    license=license,
    packages=find_packages(exclude=['example'])
)
