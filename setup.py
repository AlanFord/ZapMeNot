import setuptools

# To prevent importing about and thereby breaking the coverage info we use this
# exec hack
about = {}
with open('zap_me_not/__about__.py') as fh:
    exec(fh.read(), about)

if __name__ == '__main__':
    setuptools.setup(
        include_package_data=True,
        name=about['__package_name__'],
        version=about['__version__'],
        author=about['__author__'],
        author_email=about['__author_email__'],
        description=about['__description__'],
        url=about['__url__'],
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3"
        ],
        python_requires='>=3.4',
        intall_requires=[
            'pyvista',
            'scipy>=0.14',
            'numpy>=1.18.1',
            'pyyaml>=5.3'],
        test_requires=[
            'pytest',
            'pandas'],
        setup_requires=['pytest-runner']
    )
