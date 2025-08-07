from setuptools import find_packages, setup

setup(
    name="jwt_handler",
    version="0.1.0",
    author="Aliaksandr Fedaraka",
    author_email="fedorakooo@gmail.com",
    description="A JWT token handling library for microservices",
    packages=find_packages(
        include=["handlers*", "exceptions*", "generators*", "interfaces*", "value_objects*"],
        exclude=["tests*", "test*", "*.tests*", "*.test*"],
    ),
    install_requires=[
        "pyjwt==2.10.1",
        "pydantic-settings==2.10.1",
        "pydantic==2.11.7",
    ],
    python_requires=">=3.9",
)
