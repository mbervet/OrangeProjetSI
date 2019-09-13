from setuptools import setup

setup(
    name="SIProject",
    packages=["OrangeSIProject"],
    package_data={"OrangeSIProject": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "SIProject = OrangeSIProject"},
)
