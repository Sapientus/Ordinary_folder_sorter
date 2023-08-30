from setuptools import setup, find_namespace_packages

setup(
    name='Unuseful_folder_cleaning',
    version='0.0.2',
    description='Some stupid code',
    url='https://github.com/Sapientus',
    author='Zeyneb Akber',
    author_email='zeinabkhaalilova@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': ['cleanfolder = clean_folder.clean:find_path']},
    include_package_data=True
)