from setuptools import setup, find_packages

packages = find_packages()
packages.remove('tests')

setup(
    name='ImageTask',
    version='0.0.1',
    author='Local Projects',
    description="An image processing service.",
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'boto==2.42.0',
        'click==6.6',
        'Flask==0.11.1',
        'itsdangerous==0.24',
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'pilkit==1.1.13',
        'Pillow==3.3.0',
        'py==1.4.31',
        'PyYAML==3.11',
        'requests==2.10.0',
        'Werkzeug==0.11.10',
    ],
    test_requires=[
        'pytest==2.9.2',
    ]
)
