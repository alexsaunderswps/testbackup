import sys
import os

# Replace this with the path you got from `python -m site --user-site`
new_path = r"C:\Users\teamw\AppData\Roaming\Python\Python312\site-packages"

# Check if the new path is not already in sys.path
if new_path not in sys.path:
    sys.path.append(new_path)

# To make this change permanent, you can add it to your PYTHONPATH environment variable
if 'PYTHONPATH' in os.environ:
    os.environ['PYTHONPATH'] = new_path + os.pathsep + os.environ['PYTHONPATH']
else:
    os.environ['PYTHONPATH'] = new_path

print("Updated sys.path:", sys.path)
print("Updated PYTHONPATH:", os.environ.get('PYTHONPATH', ''))