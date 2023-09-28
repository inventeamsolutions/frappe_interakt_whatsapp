from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_interakt_whatsapp/__init__.py
from frappe_interakt_whatsapp import __version__ as version

setup(
	name="frappe_interakt_whatsapp",
	version=version,
	description="Whatsapp for Frappe / ERPNext via Interakt",
	author="Inventeam Solutions Pvt. Ltd.",
	author_email="support@inventeam.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
