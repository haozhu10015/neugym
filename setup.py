from setuptools import setup, find_packages
import neugym as ng

version = ng.__version__
requirements = open("requirements.txt").readlines()

setup(
    name="neugym",
    version=version,
    author="Hao Zhu",
    author_email="hao.zhu.10015@gmail.com",
    url="https://github.com/HaoZhu10015/neugym",
    description="Python package for reinforcement learning environment of animal behavior modeling.",
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=True
)
