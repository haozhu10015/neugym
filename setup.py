from setuptools import setup, find_packages


VERSION = "0.0.1"
requirements = open("requirements.txt").readlines()

setup(
    name="neurl",
    version=VERSION,
    author="Hao Zhu",
    author_email="hao.zhu.10015@gmail.com",
    url="https://github.com/HaoZhu10015/neurl",
    description="Library for reinforcement learning modeling of rodent behavior.",
    packages=find_packages(),
    install_requires=requirements
)