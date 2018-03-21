import csv
import os 



class SaveToCSV:
	def __init__(self, afile, s_input):
		self.f_name = afile 
		self.someinput = s_input
		self.save(self.f_name, self.someinput)
		
	def _create_csv(self, afile, someinput):
		try:
			with open(afile, 'wb') as af:
				f = csv.writer(af)
				f.writerows(someinput)
		except IOError as e:
			return e, 'had a problem creating {0}'.format(afile)
		
	def _append_csv(self, afile):
		def _create_csv(self, afile, someinput):
		try:
			with open(afile, 'a') as af:
				f = csv.writer(af)
				f.writerows(someinput)
		except IOError as e:
			return e, 'had a problem opening and appending to {0}'.format(afile)
		
	def _check_file(self, afile):
		return os.path.exists(afile)
	
	def save(self, afile, someinput):
		if self._check_file(afile):
			self._append_csv(afile, someinput)
		else:
			self._create_csv(afile, someinput)


