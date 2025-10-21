from setuptools import setup, find_packages

setup(
    name="maps-service",
    version="0.1.0",
    packages=find_packages(include=['app', 'app.*']),
    install_requires=[
        "fastapi==0.115.11",
        "uvicorn==0.34.0",
        "pandas==2.1.1",
        "numpy==1.25.2",
        "joblib==1.5.2",
        "geopandas==1.1.1",
        "shapely==2.1.1",
        "scikit-learn==1.7.2",
        "python-multipart==0.0.20",
        "starlette==0.46.1",
        "pytest==7.4.4",
        "pytest-asyncio==0.21.1",
        "httpx==0.28.1",
        "pytest-cov==4.1.0"
    ],
    python_requires=">=3.11",
)