import setuptools
setuptools.setup(
    name="qwiktiff",
    version="0.0.1",
    author="Greg Bubnis",
    author_email="gregory.bubnis@ucsf.edu",
    description="Performant lazy (not actually a contradiction) tiff reader",
    long_description_content_type=open('README.md').read(),
    packages=['qwiktiff'],
    install_requires=[
          'numpy>=1.22.4',
          'tifffile>=2022.5.4',
    ],
    python_requires='>=3.7',
)