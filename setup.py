from setuptools import setup

setup(
    name="OrangeProjetSI",
    packages=["widgets"],
    entry_points={"orange.widgets": "OrangeProjetSI = widgets"},
)
