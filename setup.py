from setuptools import setup, find_packages
import neugym as ng

version = ng.__version__
requirements = open("requirements.txt").readlines()

name = "neugym"
description = "Python package for reinforcement learning environment of animal behavior modeling."
authors = {
    "Hao": ("Hao Zhu", "hao.zhu.10015@gmail.com")
}
project_urls = {
    "Bug Tracker": "https://github.com/HaoZhu10015/neugym/issues"
}
setup(
    name=name,
    license="LICENSE",
    readme="README.md",
    version=version,
    author="Hao Zhu",
    author_email="hao.zhu.10015@gmail.com",
    url="https://github.com/HaoZhu10015/neugym",
    description=description,
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=True
)
