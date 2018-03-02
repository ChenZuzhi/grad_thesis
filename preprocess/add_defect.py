import numpy as npimport cv2 as cvimport osclass AddDefect(object):	def __init__(self, m, n):		self.m = m # ordinal of background picture		self.n = n # ordinal of defect picture		self.img = cv.imread('./origin_images/'+str(self.m)+'.png')		self.draw = self.img		self.row, self.col, chl = self.img.shape		# supporting functions		def get_point(self):		# randomly choose a point in the image		edge = 20		x = int(np.random.uniform(edge, self.row-edge))		y = int(np.random.uniform(edge, self.col-edge))		return x,y		def get_channel(self,x,y):		return self.img[x,y]	def light_dark(self,channel):		# light return  1		# dark  return  0		a = np.asscalar(channel[0])		b = np.asscalar(channel[1])		c = np.asscalar(channel[2])				if sum([a,b,c])>256*3/2:			return 1		else:			return 0		def dark_color(self):		# return a dark color channel		a = np.random.uniform(1,256/4)		b = np.random.uniform(1,256/4)		c = np.random.uniform(1,256/4)		return int(a),int(b),int(c)			def light_color(self):		# return a light color channel		a = np.random.uniform(256*3/4,255)		b = np.random.uniform(256*3/4,255)		c = np.random.uniform(256*3/4,255)		return int(a),int(b),int(c)			def random_color(self):		# return a random color channel		a = np.random.uniform(1,255)		b = np.random.uniform(1,255)		c = np.random.uniform(1,255)		return int(a),int(b),int(c)		def defect_color(self,light,dark):		# randomly generate a defect color channel		# the shares of light color,		# dark color and random color		# are light:dark:random color		rd = np.random.uniform(0,1)		if rd<light:			a,b,c = self.light_color()		elif rd>(1-dark):			a,b,c = self.dark_color()		else:			a,b,c = self.random_color()		return a,b,c		def get_slope(self):		# randomly get a slope value		x = np.random.uniform(0,np.pi)		return np.sin(x),np.cos(x),np.tan(x)			def lighten(self,x,y,flag,mu,sgm):		# return a channel lighter than the original channel		# d represent the degree		# that each channels add		# flag: 1 refers lighten; -1 refers darken		channel = self.get_channel(x,y)		a = np.asscalar(channel[0])		b = np.asscalar(channel[1])		c = np.asscalar(channel[2])				a += np.random.normal(mu,sgm)*flag		b += np.random.normal(mu,sgm)*flag		c += np.random.normal(mu,sgm)*flag				a = min(a,255)		b = min(b,255)		c = min(c,255)				a = max(a,1)		b = max(b,1)		c = max(c,1)				return int(a),int(b),int(c)		def in_abrasion_band(self,x0,y0,x,y,sin,cos,k,w,fluctuate):		# give a point(x0,y0), slope(k), width(w)		# test if the point(x,y) locates		# in the band or not				x1 = x0+w*sin		y1 = y0-w*cos				dx0 = x-x0 + np.random.normal(0,w*fluctuate)*sin		dx1 = x-x1 + np.random.normal(0,w*fluctuate)*sin				_y0 = dx0*k+y0 + np.random.normal(0,w*fluctuate)*cos		_y1 = dx1*k+y1 + np.random.normal(0,w*fluctuate)*cos				if k>=0:			# (x0,y0)'s line is higher than (x1,y2)'s line			if y<=_y0 and y>=_y1:				return True			else:				return False		else:			# (x0,y0)'s line is lower than (x1,y2)'s line			if y>=_y0 and y<=_y1:				return True			else:				return False		def write_image(self,directory):		cv.imwrite(directory, self.draw)		cv.destroyAllWindows()		# main functions	def add_dot(self):		x,y = self.get_point()		r = int(np.random.uniform(4, 10))		a,b,c = self.defect_color(0.3,0.3)		cv.circle(self.draw, (x, y), r, (a,b,c), -1)				if not os.path.exists("./generated_images/dot"):			os.makedirs("./generated_images/dot")				self.name = "./generated_images/dot/dot_"+str(self.n)+".png"	def add_spot(self):	# note the last input in cv.circle()		x,y = self.get_point()		a,b,c = self.defect_color(0.45,0.45)		array_x = []		array_y = []		df_range = int(abs(np.random.normal(4,0.01)))		r = int(np.random.uniform(2,4))		for i in range(1, df_range**2):			df_x = int(np.random.normal(x,df_range))			df_y = int(np.random.normal(y,df_range))			cv.circle(self.draw, (df_x, df_y), r, (a,b,c), 2)						array_x.append(df_x)			array_y.append(df_y)					max_x = np.amax(array_x)		min_x = np.amin(array_x)		max_y = np.amax(array_y)		min_y = np.amin(array_y)				# smooth the image around the defect, using filtering		offset = 5		roi_img = self.draw[(min_y - offset):(max_y +offset), (min_x - offset):(max_x + offset)]		roi_img = cv.blur(roi_img, (3, 3))		self.draw[(min_y - offset):(max_y +offset), (min_x - offset):(max_x + offset)] = roi_img				if not os.path.exists("./generated_images/spot"):			os.makedirs("./generated_images/spot")				self.name = "./generated_images/spot/spot_"+str(self.n)+".png"		def add_cut(self):		# cuts may comes from glue overflow		# or sharp object scratch		x0,y0 = self.get_point()		r = int(np.random.uniform(1, 3))		a,b,c = self.defect_color(0.8,0.1)		sin,cos,k = self.get_slope()						s = 3		x = x0		y = y0		while x>=0 and x<=self.row and y>=0 and y<=self.col:			# extend line along the direction of slope			# while the point in the image			cv.circle(self.draw, (int(x),int(y)), r, (a,b,c), -1)			dx = np.random.uniform(0,1)/np.sqrt(k**2+1)*r			x += dx+np.random.normal(0,r/s)			y += dx*k+np.random.normal(0,r/s)			"""			# blur the nearby area			offset = 2*r			roi_img = self.draw[(int(y) - offset):(int(y) +offset), (int(x) - offset):(int(x)+ offset)]			roi_img = cv.blur(roi_img, (r, r))			self.draw[(int(y) - offset):(int(y) +offset), (int(x) - offset):(int(x)+ offset)] = roi_img			"""					x = x0		y = y0			while x>=0 and x<=self.row and y>=0 and y<=self.col:			# opposite direction			cv.circle(self.draw, (int(x), int(y)), r, (a,b,c), -1)			dx = -np.random.uniform(0,1)/np.sqrt(k**2+1)*r			x += dx+np.random.normal(0,r/s)			y += dx*k+np.random.normal(0,r/s)				if not os.path.exists("./generated_images/cut"):				os.makedirs("./generated_images/cut")				self.name = "./generated_images/cut/cut_"+str(self.n)+".png"		def add_abrasion(self):		# abrasions are paralle equal-width columns of defect color		# usually equal interval		mu = 20 # lighten the color		sgm = 2		fluctuate = 0.1 # in abrasion random.normal sigma				width = 20		interval = 60		x0,y0 = self.get_point()		sin,cos,k = self.get_slope() # tan				marks = [] # the signal points at left edge of bands		x = x0		y = y0		while x>=0 and x<=self.row and y>=0 and y<=self.col:			# find band marks to right			marks.append((x,y))			x += (width+interval)*sin			y -= (width+interval)*cos					x = x0		y = y0		while x>=0 and x<=self.row and y>=0 and y<=self.col:			# find band marks to left			marks.append((x,y))			x -= (width+interval)*sin			y += (width+interval)*cos				marks = list(set(marks)) # remain unique points				for i in range(0,self.row):			for j in range(0,self.col):				for z in marks:					if self.in_abrasion_band(z[0],z[1],i,j,sin,cos,k,width,fluctuate):						self.draw[i,j] = self.lighten(i,j,1,mu,sgm)						break		if not os.path.exists("./generated_images/abrasion"):			os.makedirs("./generated_images/abrasion")				self.name = "./generated_images/abrasion/abrasion_"+str(self.n)+".png"