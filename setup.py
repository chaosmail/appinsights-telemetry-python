from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='appinsights_telemetry_logger',
    version='0.0.1',
    description='Python AppInsights Telemetry Logger',
    packages=['appinsights_telemetry_logger',],
    author='Christoph Koerner',
    author_email='office@chaosmail.at',
    url='https://github.com/chaosmail/appinsights-telemetry-python',
    download_url='https://github.com/chaosmail/appinsights-telemetry-python/releases',
    license='MIT',
    long_description=long_description,
    install_requires=[
        'applicationinsights',
        'psutil'
    ],
    entry_points = {
        'console_scripts': ['appinsights-telemetry-logger=appinsights_telemetry_logger:main'],
    }
)
