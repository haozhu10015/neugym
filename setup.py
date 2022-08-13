from setuptools import setup, find_packages
import neugym.version

version = neugym.version.__version__
requirements = open("requirements.txt").readlines()

setup(
    name="neugym",
    version=version,
    author="Hao Zhu",
    author_email="hao.zhu.10015@gmail.com",
    url="https://github.com/HaoZhu10015/neugym",
    description="Package for reinforcement learning modeling of rodent behavior.",
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=True
)
