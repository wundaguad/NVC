import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'packages': ['tkinter', 'PIL'],
    'excludes': ['matplotlib', 'numpy', 'scipy'],
    'include_files': [('logo.png', 'logo.png')] if os.path.exists('logo.png') else []
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('nominalwert_rechner.py', 
              base=base, 
              target_name='NominalwertRechner',
              icon='logo.png' if os.path.exists('logo.png') else None)
]

setup(name='NominalwertRechner',
      version='1.0',
      description='Professional Trading Position Calculator',
      options={'build_exe': build_options},
      executables=executables)
