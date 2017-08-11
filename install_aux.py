import os
import shutil
import subprocess
import _winreg

def get_VAST_dir():
	try:
		with _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE) as reg:
			sub_key = r'Software\WOW6432node\VIVOTEK, Inc.\VAST' if 'PROGRAMFILES(X86)' in os.environ else r'Software\VIVOTEK, Inc.\VAST'
			with _winreg.OpenKey(reg, sub_key) as key:
				return _winreg.QueryValueEx(key, 'INSTALL_PATH')[0]
	except WindowsError:
		print 'get_VAST_dir() failed'


def enable_UI_remote_control():
	dst = os.path.join(get_VAST_dir(), 'Client', 'VAST2', 'plugin')
	shutil.copy2('PluginUIRemoteControl.dll', dst)
	
def replace_software_license():
	dst = os.path.join(get_VAST_dir(), 'Server')
	if 'PROGRAMFILES(X86)' in os.environ :
		print 'copy x64 lic'
		shutil.copy2('UAT\\automation\\x64_lic\\License.dat', dst)
	else:
		print 'copy x86 lic'
		shutil.copy2('UAT\\automation\\x86_lic\\License.dat', dst)
	'''shutil.copy2('UAT\\automation\\License.dat', dst)'''
	'''TODO:  change this function to automaticly replace right license to right position'''
	

def disable_vm_checking():
	subprocess.call('NET STOP "VAST Uranus Watch Dog"')

	cwd = os.getcwd()
	os.chdir(os.path.join(get_VAST_dir(), 'Server'))

	targets = ['ConfigurationCmdModule.dll',
			   'VMSConfigurationServer.exe',
			   'VMSQueryServer.exe',
			   'VMSRecordingServer.exe',
			   os.path.join('QTSSModules', 'QTSSVivotekModule.dll'),
			   os.path.join('Utility', 'SystemManager', 'VMSSystemManager.exe')]

	for target in targets:
		with open(target, 'rb') as f:
			buf = f.read()
		with open(target, 'wb') as f:
			f.write(buf.replace(b'vmware', b'vmdiro'))

	os.chdir(cwd)

def main():
	replace_software_license()
	enable_UI_remote_control()
	disable_vm_checking()

if __name__ == "__main__":
	main()
