from setuptools import setup
from glob import glob
import os

package_name = "task14"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        (
            "share/" + package_name,
            ["package.xml"],
        ),
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.launch.py"),
        ),
        (
            os.path.join("share", package_name, "worlds"),
            glob("worlds/*.sdf"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Karim",
    maintainer_email="karim@example.com",
    description="Task 14",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "autonomous_mover = task14.autonomous_mover:main",
        ],
    },
)
