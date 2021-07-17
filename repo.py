import sys
import subprocess
import pathlib

if len(sys.argv) <= 1:
  print('Commands: size, clean')
  sys.exit(0)

command = sys.argv[1]
here = pathlib.Path(__file__).parent

if command == 'size':
  env_path = subprocess.check_output(['pipenv', '--venv']).decode().strip()
  subprocess.call(['du', '-shc', str(here), env_path])
elif command == 'clean':
  print('Deleting virtualenv...')
  subprocess.call('pipenv', '--rm')
else:
  print('Unrecognized command')
