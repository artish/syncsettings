from setuptools import setup

setup(
    name='SyncSettings',
    version='0.3',
    py_modules=['sync_settings'],
    install_requires=[
        "Click",
        "send2trash"
    ],
    entry_points='''
        [console_scripts]
        sync_settings=sync_settings:cli
    ''',
)
