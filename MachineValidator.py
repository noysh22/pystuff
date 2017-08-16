
import wmi
import win32evtlog
import psutil
import csv
from os import listdir
from os.path import isfile, join, getsize

SERVICE_NAME = 'MSSQLSERVER'
WIN_SERVICE_OK_STATE = 'Running'
WORKING_SERVICE_INDICATOR = 'INFO - Main Configuration Sanity is OK'
SIEMPLIFY_SERVICE_START_EVENTID = 900

ERROR_FILES_COUNT_DIR = r'.'
FILES_QUEUE_SIZE_DIR = r'.'

KB = 1024.0
MB = KB**2

RESULT_OBJ_FIELDS = {
	'is_running' : 'Is Running',
	'start_time' : 'Service Start',
	'cpu' : 'CPU%',
	'mem' : 'Available Memory',
	'file_num1' : ERROR_FILES_COUNT_DIR + ' Count',
	'file_num2' : FILES_QUEUE_SIZE_DIR + ' Count'
}

class MachineStatusValidator(object):
	"""docstring for MachineStatusValidator"""
	def __init__(self, **kwarg):
		self.__service_name = kwarg.pop('srv_name', None)
		self.__output_csv = kwarg.pop('output', None)

		super(MachineStatusValidator, self).__init__()

	def is_service_running(self, wmi_client):
		services = wmi_client.Win32_Service(Name=self.__service_name)

		if 1 != len(services):
			raise Exception("Failed to find service matching the name {}, services query result={}".format(self.__service_name, services))

		state = next(iter(services)).State
		print state
		return WIN_SERVICE_OK_STATE.title() == state.title()
			

	def find_event_log_entry(self):
		handle = win32evtlog.OpenEventLog('localhost', 'Siemplify')
		flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

		keep_running = True
		found_event = None
		while keep_running:
			events = win32evtlog.ReadEventLog(handle, flags, 0)
			for event in events:
				if SIEMPLIFY_SERVICE_START_EVENTID == event.EventID:
					if WORKING_SERVICE_INDICATOR in event.StringInserts[0]:
						print event.SourceName
						found_event = event
						keep_running = False

		win32evtlog.CloseEventLog(handle)
		return found_event

	def count_files_in_dir(self, base_dir):
		return len([f for f in listdir(base_dir) if isfile(join(base_dir, f))])

	def calc_size_of_dir(self, base_dir, use_mb=True):
		units = MB
		if not use_mb:
			units = KB
		return (sum([getsize(join(base_dir, f)) for f in listdir(base_dir) if isfile(join(base_dir, f))])) / units

	def get_system_resources_usage(self):
		cpu_percent = psutil.cpu_percent()
		virtual_mem = psutil.virtual_memory()
		available_memory = virtual_mem.available / MB
		used_memory = virtual_mem.used / MB

		return {'CPU' : cpu_percent, 'FREE_MEM' : available_memory, 'USED_MEM' : used_memory}


	def get_machine_status(self):
		wmi_client = wmi.WMI()
		result = {}

		is_service_running = self.is_service_running(wmi_client)
		if is_service_running: 
			start_event = self.find_event_log_entry()
			result[RESULT_OBJ_FIELDS['start_time']] = start_event.TimeGenerated.Format()

		result[RESULT_OBJ_FIELDS['is_running']] = is_service_running

		system_resources = self.get_system_resources_usage()

		result[RESULT_OBJ_FIELDS['cpu']] = system_resources.get('CPU')
		result[RESULT_OBJ_FIELDS['mem']] = system_resources.get('FREE_MEM')

		result[RESULT_OBJ_FIELDS['file_num1']] = self.count_files_in_dir(ERROR_FILES_COUNT_DIR)
		result[RESULT_OBJ_FIELDS['file_num2']] = self.count_files_in_dir(FILES_QUEUE_SIZE_DIR)
		# result[RESULT_OBJ_FIELDS['file_num2']] = self.calc_size_of_dir(FILES_QUEUE_SIZE_DIR)

		return result

	def validate_machine_status(self):
		print 'Getting machine status'
		status = self.get_machine_status()

		print 'Got machine status: ', status
		print 'Writing to csv file...'
		with open(self.__output_csv, 'w') as output:
			fields = RESULT_OBJ_FIELDS.values()
			writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
			writer.writeheader()
			writer.writerow(status)
			print 'Wrote status to: ', self.__output_csv

		print '===========Done============='

if __name__ == '__main__':
	validator = MachineStatusValidator(srv_name=SERVICE_NAME, output='status.csv')
	# validator.find_event_log_entry()
	# client = wmi.WMI()
	# print validator.is_service_running(client)
	# print validator.count_files_in_dir(r'C:\Projects\SimeplifyPy')
	# print validator.calc_size_of_dir(r'C:\Projects\SimeplifyPy')
	validator.validate_machine_status()


