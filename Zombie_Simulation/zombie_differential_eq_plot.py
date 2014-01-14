
from udacityplots import *

step_size = 0.5 # hours
cinfections = 1.0/10000 # /hour*people
cinfection_time = 35. # hours
cdeath_time = 105. # hours

end_time = 250.0 # hours
num_steps = int(end_time / step_size)
times = step_size * numpy.array(range(num_steps + 1))

def HIZ():

    h = numpy.zeros(num_steps + 1)
    i = numpy.zeros(num_steps + 1)
    z = numpy.zeros(num_steps + 1)

    h[0] = 2000.0 
    i[0] = 1.0
    z[0] = 50.0

    for step in range(num_steps):
        infections = step_size * cinfections * h[step]*z[step]
        newzombies = step_size / cinfection_time * i[step]
        zombiedeaths = step_size / cdeath_time * z[step]
        h[step + 1] = h[step] - infections
        i[step + 1] = i[step] + infections - newzombies
        z[step + 1] = z[step] + newzombies - zombiedeaths
        
    return h, i, z

h, i, z = HIZ()

@show_plot
def plot_me():
    h_plot = matplotlib.pyplot.plot(times, h, label = 'Healthy_People')
    i_plot = matplotlib.pyplot.plot(times, i, label = 'Infected_People')
    z_plot = matplotlib.pyplot.plot(times, z, label = 'Zombies')

    matplotlib.pyplot.legend(('Healthy_People', 'Infected_People', 'Zombies'), loc = 'upper right')
    
    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Time in hours')
    axes.set_ylabel('Number of people')
    matplotlib.pyplot.xlim(xmin = 0.)
    matplotlib.pyplot.ylim(ymin = 0.)
    
plot_me()
