from setuptools import setup

setup(
    name="SIProject",
    packages=["OrangeSIProject"],
    package_data={"OrangeSIProject": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    entry_points={"orange.widgets": "SIProject = OrangeSIProject"},
)
