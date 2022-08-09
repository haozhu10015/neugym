from setuptools import setup, find_packages
import neurl.version

version = neurl.version.__version__
requirements = open("requirements.txt").readlines()

setup(
    name="neurl",
    version=version,
    author="Hao Zhu",
    author_email="hao.zhu.10015@gmail.com",
    url="https://github.com/HaoZhu10015/neurl",
    description="Library for reinforcement learning modeling of rodent behavior.",
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=True
)