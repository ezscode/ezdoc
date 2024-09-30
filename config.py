import os 
import getpass 
import platform


login_user = getpass.getuser()
system = platform.system()

if system == 'Darwin':
    quickdoc_root_dir = f'/Users/{login_user}/Documents/quickdoc' 
elif system == 'Linux':
    quickdoc_root_dir = f'/home/{login_user}/quickdoc' 
else:
    quickdoc_root_dir = 'quickdoc' 



