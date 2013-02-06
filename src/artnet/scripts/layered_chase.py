import time

from artnet import dmx, fixtures

# set up test fixtures
g = fixtures.FixtureGroup([
	fixtures.Fixture.create(420, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(427, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(434, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(441, 'chauvet/slimpar-64.yaml'),
])

def all_red(secs=5.0):
	"""
	A simple all-red light generator.
	"""
	t = time.time()
	while(True):
		g.setColor('#0000ff')
		g.setIntensity(255)
		yield g.getFrame()
		if(secs and time.time() - t >= secs):
			return

def single_white_beat_chase(clock, secs=5.0):
	"""
	A simple white chase pattern.
	"""
	t = time.time()
	c = clock()
	while(c['running']):
		# Reset to white, but blacked out
		g.setColor('#ffffff')
		g.setIntensity(0)
		
		# Grab one fixture, set its intensity
		f = g.fixtures[c['beat'] - 1]
		f.setIntensity(255)
		
		# Grab just that fixture's DMX values
		frame = f.getFrame()
		yield frame
		if(secs and time.time() - t >= secs):
			return
		c = clock()

def main(config, controller=None):
	q = controller or dmx.Controller(config.get('base', 'address'), bpm=240, nodaemon=True, runout=True)
	# "base color" red
	q.add(all_red())
	# white chase layer
	q.add(single_white_beat_chase(q.get_clock()))
	if not controller:
		q.start()

