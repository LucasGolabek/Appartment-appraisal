from setuptools import setup

import algorithm
import data_scraper
import location_specifier

setup(
    name="apartment-appraisal",
    version=1.0,
    packages=["algorithm", "data_scraper", "location_specifier"],
    url="https://github.com/PKozicki/apartment-appraisal",
    license="",
    author="PKozicki",
    description="",
    requires_python=">=3.8",
    install_requires=[
        "asgiref==3.4.1",
        "beautifulsoup4==4.11.1",
        "bs4==0.0.1",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.12",
        "defusedxml==0.7.1",
        "Django==3.2.4",
        "django-debug-toolbar==3.2.4",
        "django-filter==21.1",
        "djangorestframework==3.13.1",
        "djangorestframework-xml==2.0.0",
        "djangorestframework-yaml==2.0.0",
        "geographiclib==1.52",
        "geopy==2.2.0",
        "idna==3.3",
        "pkg-resources==0.0.0",
        "pytz==2022.1",
        "PyYAML==6.0",
        "requests==2.27.1",
        "soupsieve==2.3.2.post1",
        "sqlparse==0.4.2",
        "typing-extensions==4.1.1",
        "urllib3==1.26.9",
    ],
    entry_points={
        "console_scripts": [
            #"algorithm = algorithm.__main__:main",
            #"data_scraper = data_scraper.__main__:main",
            #"location_specifier = location_specifier.__main__:main"
        ]
    }
)
