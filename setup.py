from pip.req import parse_requirements
from setuptools import setup, find_packages


def get_reqs(reqs):
    return [str(ir.req) for ir in reqs]

try:
    install_reqs = get_reqs(parse_requirements("requirements.txt"))
except TypeError:
    from pip.download import PipSession
    install_reqs = get_reqs(
        parse_requirements("requirements.txt", session=PipSession())
    )

setup(
    name="Tsidii",
    version=__import__("tsidii").__version__,
    packages=find_packages(),
    url="example.com",
    author="Forrest York",
    author_email="forrest.york@gmail.com",
    description="Tsidii Email Content Manager",
    long_description=open("README.rst").read(),
    license="BSD",
    keywords="email",
    install_requires=install_reqs,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7, 3.4",
        "Natural Language :: English"
    ]
)
