from setuptools import setup

setup(
    name='SyncSettings',
    version='0.2',
    py_modules=['setup_settings'],
    install_requires=[
        "Click",
        "send2trash"
    ],
    entry_points='''
        [console_scripts]
        setup_settings=setup_settings:cli
    ''',
)
