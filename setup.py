from setuptools import setup, find_packages

packages = find_packages()
packages.remove('tests')

setup(
    name='ImageTask',
    version='0.1.0',
    author='Local Projects',
    description="An image processing service.",
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'boto>=2.38.0',
        'Flask>=0.10.1',
        'itsdangerous>=0.24',
        'Jinja2>=2.8',
        'MarkupSafe>=0.23',
        'pilkit>=1.1.13',
        'Pillow>=3.0.0',
        'PyYAML>=3.11',
        'requests>=2.5.1',
        'Werkzeug>=0.11.11',
    ],
    test_requires=[
        'pytest==2.9.2',
    ]
)
