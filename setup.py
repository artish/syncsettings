from setuptools import setup

setup(
    name = 'sync_settings',
    version = '0.4.1',
    author = 'Florian Schrödl',
    author_email = 'flo.schroedl@gmail.com',
    description = 'Synchronize your settings',
    packages = ['sync_settings'],
    install_requires = [
        'click',
        'send2trash'
    ],
    entry_points = {
        'console_scripts': [
            'sync_settings = sync_settings:cli',
            'ss = sync_settings:cli'
        ]
    }
)
