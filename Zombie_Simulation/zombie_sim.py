#This code only runs on codeskulptor.com, just paste it in!

import simplegui
import simpleplot
import random

window_width = 800
window_height = 800
size_scale = 50

PROB_INFECTION = 0.8
PROB_KILLZOMBIE = 0.3
PROB_CONV = 0.3
ssc = 4

overture = simplegui.load_sound('https://ia601002.us.archive.org/32/items/01TheyreCallingMyFlightContagionMovieSoundtrackOSTCliffMartinez/01%20-%20They%27re%20Calling%20My%20Flight%20-%20Contagion%20%28Movie%29%20Soundtrack%20%28OST%29%20-%20Cliff%20Martinez.ogg')

BATTLEGROUND = simplegui.load_image('http://i.imgur.com/rByO9Cr.jpg')
ZOMBIEICON  = simplegui.load_image('http://icons.iconarchive.com/icons/yootheme/halloween/512/geek-zombie-icon.png')
# replace this with a color scheme, it should fade into dark as human turns into a zombie
sim_nodes = {}
copySimNodes = {}

zombies = []
infected = []
infect = []
kill = []

timesteps = 0
deadzombies = 0
livingpeople = 251 # since we start with one 5 zombies

graphHPop = []
graphIPop = []
graphZPop = []


def draw(canvas):
    global paintCopy
    #canvas.draw_image(BATTLEGROUND,(1104/2,786/2),(1104,786),(window_width/2,window_height/2),(window_width,window_height))
    
    timelabel.set_text(str(timesteps))
    zombieDeath.set_text(str(deadzombies))
    livezombies.set_text(str(len(zombies)))
    numpeople.set_text(str(livingpeople))
    infpeople.set_text(str(len(infected)))
             
    for node in sim_nodes:
        coords = [(a[0] + size_scale/2,a[1]) for a in [(node[0],node[1]), (node[0]+size_scale/ssc ,node[1]), (node[0] + size_scale/ssc, node[1] + size_scale/ssc), (node[0], node[1] + size_scale/ssc)]]
        if sim_nodes[node] == "Healthy":            
            canvas.draw_polygon(coords,1,"Black","White")
        elif sim_nodes[node] == "Zombie":
            #canvas.draw_image(ZOMBIEICON,(206,206),(512,512),(node[0] + 25, node[1]+ 25),(90,90))
            canvas.draw_polygon(coords,1,"Black","Red")
        elif sim_nodes[node] == "Infected":
            canvas.draw_polygon(coords,1,"Black","Orange")
        else:
            pass
            
           # canvas.draw_polygon(coords,1,"Black")
    
                
def initialize():
    for x in range(window_width/size_scale):
        for y in range(window_height/size_scale):
            sim_nodes[(x*size_scale,y*size_scale)] = "Healthy"
    sim_nodes[7*size_scale,10*size_scale] = "Zombie"
    sim_nodes[3*size_scale,8*size_scale] = "Zombie"
    sim_nodes[5*size_scale,3*size_scale] = "Zombie"
    sim_nodes[11*size_scale,12*size_scale] = "Zombie"
    sim_nodes[2*size_scale,14*size_scale] = "Zombie"
    zombies.append((7*size_scale,10*size_scale))
    zombies.append((3*size_scale,8*size_scale))
    zombies.append((5*size_scale,3*size_scale))
    zombies.append((11*size_scale,12*size_scale))
    zombies.append((2*size_scale,14*size_scale))
        
def get_adj(z):
    returnli = []
    w1 =  (z[0] == 0)
    w2 = (z[0] == window_width - size_scale) 
    h1 = (z[1] == 0)  
    h2 =  (z[1] == window_height - size_scale)
    
    if w1:
        if h1:
            return [(z[0],z[1] + size_scale), (z[0] + size_scale,z[1] + size_scale),
               (z[0] + size_scale,z[1])]    
            
        elif h2:
            return [(z[0] + size_scale,z[1] ),
                (z[0],z[1] - size_scale), (z[0] + size_scale,z[1] - size_scale)]
        else:
            return [(z[0],z[1] + size_scale), (z[0] + size_scale,z[1] + size_scale),
               (z[0] + size_scale,z[1]),
               (z[0],z[1] - size_scale), (z[0] + size_scale,z[1] - size_scale)]
    elif w2:
        if h1:
            return [(z[0]- size_scale, z[1] + size_scale), (z[0],z[1] + size_scale),
               (z[0]- size_scale,z[1])]
        elif h2:
            return [(z[0]- size_scale,z[1]),
               (z[0]- size_scale,z[1] - size_scale), (z[0],z[1] - size_scale)]
        else:
            return [(z[0]- size_scale, z[1] + size_scale), (z[0],z[1] + size_scale),
               (z[0]- size_scale,z[1]),
               (z[0]- size_scale,z[1] - size_scale), (z[0],z[1] - size_scale)]
    elif h1:
        return [(z[0]- size_scale, z[1] + size_scale), (z[0],z[1] + size_scale), (z[0] + size_scale,z[1] + size_scale),
               (z[0]- size_scale,z[1]), (z[0] + size_scale,z[1])]
        
    elif h2:
        return [(z[0]- size_scale,z[1]), (z[0] + size_scale,z[1]),
               (z[0]- size_scale,z[1] - size_scale), (z[0],z[1] - size_scale), (z[0] + size_scale,z[1] - size_scale)]
        
    else:
        return [(z[0]- size_scale, z[1] + size_scale), (z[0],z[1] + size_scale), (z[0] + size_scale,z[1] + size_scale),
               (z[0]- size_scale,z[1]), (z[0] + size_scale,z[1]),
               (z[0]- size_scale,z[1] - size_scale), (z[0],z[1] - size_scale), (z[0] + size_scale,z[1] - size_scale)]
            
        

def start_simulating():
    timer.start()
    #overture.play()
    
def stop_simulating():
    timer.stop()
    #overture.pause
    
def resetSim():
    global sim_nodes, zombies, infected, kill,infect
    
    sim_nodes = {}
    zombies = []
    infected = []
    kill = []
    infect = []
    
    timer.stop()
    initialize()
    
def timer_handler():
    global timesteps
    global infected
    global zombies
    global kill
    global sim_nodes
    global infect
    global paintCopy
    global copySimNodes
    global deadzombies
    global livingpeople
    
    graphHPop.append((timesteps,livingpeople))
    graphZPop.append((timesteps,len(zombies)))
    graphIPop.append((timesteps,len(infected)))
    
    if (livingpeople == 10):
        timer.stop()
        print [graphHPop,graphIPop,graphZPop]

    
    copySimNodes = dict(sim_nodes)

    for z in zombies: # need to fix this for corner spaces, suggestion: define a prodecure that checks z (location of zombie) and doesnt add some of these three as a result
        randkill = random.randrange(0,10000)/10000.0
        if (randkill > 1.0 - PROB_KILLZOMBIE): # do infected people kill zombies?
            zombies.remove(z)
            copySimNodes[z] = "Empty"
            deadzombies += 1
            continue
        
        adj = get_adj(z)       
        for n in adj:
            randinf = random.randrange(0,10000)/10000.0
            if n not in infect:            
                if (randinf > 1.0 - PROB_INFECTION) and copySimNodes[n] == "Healthy":            
                    infect.append(n) # at the end of the round change n to infected 
                                
    
    for i in infected:
        rand = random.randrange(0,10000)/10000.0
        if (rand > 1.0 - PROB_CONV): 
            infected.remove(i)
            copySimNodes[i] = "Zombie"
            zombies.append(i)
    
    for i in infect:
        infect.remove(i)
        copySimNodes[i] = "Infected"
        infected.append(i)
        livingpeople -= 1
        
        
    sim_nodes = dict(copySimNodes)
    timesteps += 1
    

    
    #determines whether they are going to go from healthy to infected, or zombie to dead    

def pinf_handler(text_input):
    global PROB_INFECTION
    PROB_INFECTION = float(text_input)
    
def zdeath_handler(text_input):
    global PROB_KILLZOMBIE
    PROB_KILLZOMBIE = float(text_input)  

def conv_handler(text_input):
    global PROB_CONV
    PROB_CONV = float(text_input)

def el():
    frame.add_label("")
    
#generate random zombies and terrain + initialize sim_nodes dict
initialize()
#frame
frame = simplegui.create_frame("Lucas Langer and Robert Belfer Simulation for Linear Algebra and ", window_width, window_height)
frame.set_draw_handler(draw)

#buttons and labels
frame.add_label("Brought to you by:")
frame.add_label("Robert Belfer and Lucas Langer")
el()
frame.add_button("Start Simulating", start_simulating)
frame.add_button("Stop Simulating", stop_simulating)
frame.add_button("Reset To Default", resetSim)
el()
pof = frame.add_input('Probability of Infection', pinf_handler,50)
pof.set_text(str(PROB_INFECTION))
rzd = frame.add_input('Probability that Zombies Die', zdeath_handler,50)
rzd.set_text(str(PROB_KILLZOMBIE))

piz = frame.add_input('Probability that Infectious Turns to Zombie', conv_handler,50)
piz.set_text(str(PROB_CONV))

frame.add_label('Hours Passed:')
timelabel = frame.add_label('0')
frame.add_label('Dead Zombies:')
zombieDeath = frame.add_label('0')
frame.add_label('Zombies Alive:')
livezombies = frame.add_label('1')
frame.add_label('Healthy People:')
numpeople = frame.add_label(str((window_width/size_scale)**2))
frame.add_label('Infected People:')
infpeople = frame.add_label(str(0))


timer = simplegui.create_timer(40, timer_handler)

resetSim()
frame.start()
