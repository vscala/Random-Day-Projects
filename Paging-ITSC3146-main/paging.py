from math import log2
'''
	Class for handling memory management paging and page replacement policies.
'''

class Paging:
	
	def __init__(self, output = log2):
		self.OUTPUT_FORMAT = log2
		
		### Logical and Physical Memory Sizes ###
		# Size of main memory
		self.PHYSICAL_MAIN_MEMORY_SIZE = None
		# Size of process
		self.LOGICAL_ADDRESS_SIZE = None
		# Size of pages / frames
		self.PAGE_FRAME_SIZE = None
		# Number of pages (logical memory)
		self.LOGICAL_PAGES = None
		# Number of frames (physical memory)
		self.PHYSICAL_PAGE_FRAMES = None
		
		### Page Replacement ###
		# Page frame values
		self.frameValues = []
		# First-in first-out index
		self.FIFOindex = 0
		# Second chance reference bits
		self.refBits = []
		# Least recently used queue
		self.lru = []
		
	def compute(self):
		# Initialize page replacement variables
		if self.PHYSICAL_PAGE_FRAMES: 
			self.frameValues = [None] * self.PHYSICAL_PAGE_FRAMES
			self.refBits = [0] * self.PHYSICAL_PAGE_FRAMES
			self.lru = [i for i in range(self.PHYSICAL_PAGE_FRAMES)[::-1]]
			
		if not self.PAGE_FRAME_SIZE: return
		
		# Computer logical address size / number of pages
		if self.LOGICAL_PAGES: 
			self.LOGICAL_ADDRESS_SIZE = self.LOGICAL_PAGES * self.PAGE_FRAME_SIZE
		elif self.LOGICAL_ADDRESS_SIZE: 
			self.LOGICAL_PAGES = self.LOGICAL_ADDRESS_SIZE // self.PAGE_FRAME_SIZE
		
		# Compute physical memory size / number of frames
		if self.PHYSICAL_PAGE_FRAMES: 
			self.PHYSICAL_MAIN_MEMORY_SIZE = self.PHYSICAL_PAGE_FRAMES * self.PAGE_FRAME_SIZE
		elif self.PHYSICAL_MAIN_MEMORY_SIZE: 
			self.PHYSICAL_PAGE_FRAMES = self.PHYSICAL_MAIN_MEMORY_SIZE // self.PAGE_FRAME_SIZE
		
	def __str__(self):
		out = f"{id(self)}:\n"
		func = self.OUTPUT_FORMAT
		if self.PAGE_FRAME_SIZE: 
			out += f"\tPAGE_FRAME_SIZE: {func(self.PAGE_FRAME_SIZE)}\n"
		if self.PHYSICAL_MAIN_MEMORY_SIZE: 
			out += f"\tPHYSICAL_MAIN_MEMORY_SIZE: {func(self.PHYSICAL_MAIN_MEMORY_SIZE)}\n"
		if self.LOGICAL_ADDRESS_SIZE: 
			out += f"\tLOGICAL_ADDRESS_SIZE: {func(self.LOGICAL_ADDRESS_SIZE)}\n"
		if self.LOGICAL_PAGES: 
			out += f"\tPAGES: {func(self.LOGICAL_PAGES)}\n"
		if self.PHYSICAL_PAGE_FRAMES: 
			out += f"\tFRAMES: {func(self.PHYSICAL_PAGE_FRAMES)}\n"
		out += f"(Note: output format {self.OUTPUT_FORMAT})\n"
		
		return out
		
	# First In First Out
	def addFIFO(self, page):
		if not self.frameValues:
			self.compute()
			if not self.frameValues: 
				print("error")
				return False
		for i in range(len(self.frameValues)):
			if self.frameValues[i] == None or self.frameValues[i] == page:
				ret = self.frameValues[i] == page
				self.frameValues[i] = page
				return ret
		self.frameValues[self.FIFOindex] = page
		self.FIFOindex += 1
		self.FIFOindex %= len(self.frameValues)
		return False
		
	# Second Chance
	def addSC(self, page):
		if not self.frameValues:
			self.compute()
			if not self.frameValues: 
				print("error")
				return False
		
		for i in range(len(self.frameValues)):
			if self.frameValues[i] == None or self.frameValues[i] == page:
				ret = self.frameValues[i] == page
				self.frameValues[i] = page
				if ret: self.refBits[i] = 1
				return ret
		
		while self.refBits[self.FIFOindex]:
			self.refBits[self.FIFOindex] = 0
			self.FIFOindex += 1
			self.FIFOindex %= len(self.frameValues)
				
		
		self.frameValues[self.FIFOindex] = page
		self.FIFOindex += 1
		self.FIFOindex %= len(self.frameValues)
		return False
	
	# Least Recently Used
	def addLRU(self, page):
		if not self.frameValues:
			self.compute()
			if not self.frameValues: 
				print("error")
				return False
		if page in self.frameValues:
			pi = self.frameValues.index(page)
			ind = self.lru.index(pi)
			self.lru.pop(ind)
			self.lru.insert(0, pi)
			return True
		pi = self.lru.pop()
		self.frameValues[pi] = page
		self.lru.insert(0, pi)
		return False
	
	# Add page with verbose output
	def addVerbose(self, page, policy = addFIFO):
		isHit = policy(self, page)
		out = f"{page}"
		out += f" \t {'hit' if isHit else 'fault'}"
		out += f" \t {str(self.frameValues):<20}"
		out += f" \t {chr(ord('A') + self.frameValues.index(page))}"
		return out
		
def testPageReplacementPolicty(frames, requests, policy):
	policyTest = Paging()
	policyTest.PHYSICAL_PAGE_FRAMES = frames
	print(f"Page \t Status  {'Frame Values':<20} \t Frame")
	for page in requests:
		print(policyTest.addVerbose(page, policy))
		
def testMemoryManagementPaging(pmemory, pfsize, lmemory):
	memoryManagementTest = Paging()
	memoryManagementTest.PHYSICAL_MAIN_MEMORY_SIZE = pmemory
	memoryManagementTest.PAGE_FRAME_SIZE = pfsize
	memoryManagementTest.LOGICAL_ADDRESS_SIZE = lmemory
	memoryManagementTest.compute()
	print(memoryManagementTest)

if __name__ == "__main__":
	testMemoryManagementPaging(2**12, 2**8, 2**13)
	testMemoryManagementPaging(2**20, 2**15, 2**19)
	testMemoryManagementPaging(2**15, 2**12, 2**16)
	
	testPageReplacementPolicty(4, [4, 1, 7, 10, 8, 4, 8, 7, 1, 4, 7, 10, 4, 8, 4, 1, 7, 10], Paging.addFIFO)
	testPageReplacementPolicty(4, [4, 1, 7, 10, 8, 4, 8, 7, 1, 4, 7, 10, 4, 8, 4, 1, 7, 10], Paging.addSC)
	testPageReplacementPolicty(4, [4, 1, 7, 10, 8, 4, 8, 7, 1, 4, 7, 10, 4, 8, 4, 1, 7, 10], Paging.addLRU)
	testPageReplacementPolicty(4, [2, 3, 6, 2, 7, 6, 3, 1, 5, 1, 2, 4, 7, 1, 2, 6, 9, 3], Paging.addFIFO)
	testPageReplacementPolicty(4, [2, 3, 6, 2, 7, 6, 3, 1, 5, 1, 2, 4, 7, 1, 2, 6, 9, 3], Paging.addLRU)
	testPageReplacementPolicty(4, [1, 5, 3, 7, 9, 5, 3, 1, 9, 5, 7, 3, 7, 5, 9, 1, 3, 5], Paging.addFIFO)
	testPageReplacementPolicty(4, [1, 5, 3, 7, 9, 5, 3, 1, 9, 5, 7, 3, 7, 5, 9, 1, 3, 5], Paging.addSC)
		
