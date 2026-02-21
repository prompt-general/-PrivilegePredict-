from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="privilegepredict",
    version="0.1.0",
    author="PrivilegePredict Team",
    author_email="team@privilegepredict.example.com",
    description="A multi-cloud identity graph platform for privilege escalation analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/privilegepredict/privilegepredict",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi==0.110.0",
        "uvicorn[standard]==0.29.0",
        "pydantic==2.6.4",
        "neo4j==5.18.0",
        "boto3==1.34.69",
        "msgraph-core==1.0.0",
        "msgraph-sdk==1.0.0",
        "python-multipart==0.0.9",
        "azure-identity==1.15.0",
        "python-jose==3.3.0",
        "passlib==1.7.4",
    ],
    entry_points={
        "console_scripts": [
            "privilegepredict=privilegepredict:main",
        ],
    },
)