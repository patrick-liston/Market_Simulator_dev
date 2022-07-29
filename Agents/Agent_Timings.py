''' This set of functions is used to generate the "wake" times for agent.
These are the times at which an agent is checked - and makes a decision of if/how they will trade.
'''

from tqdm import tqdm


''' Generates a list of wake times for an agents.

	@param agent_id: Agent to calculate wake times for.
	@param trade_freq: Specified tradinf frequency - use this to get wake intervals (using chisquare distribution) 
	@param sim_time: Time simulation will run for - maximum time allowed 
	@praram rng: Random seed - So we can reproduce results

	@Return wake_times: List of all times the agent should be "woken" during the simulation
'''
def generate_wake_times_quick(agent_id, trade_freq, sim_time,rng):
    wake_times=[]; current_time=0
    while current_time<=sim_time:
        wake_interval=int(rng.chisquare(trade_freq))
        if wake_interval>0:
            wake_times.append(current_time+wake_interval)
            current_time+=wake_interval
    return  wake_times



''' Generates a list of lists containing wake times for ALL agents.

	@param agent_info: List of information about ALL agents within the simulation
	@param sim_time: Time simulation will run for - maximum time allowed 
	@praram rng: Random seed - So we can reproduce results

	@Return all_wake_times: List of lists containing all times ALL agents should be "woken" during the simulation
'''

def generating_agent_wake_times(agent_info, sim_time,rng):
	agents=[str(row[0]) for row in agent_info]
	all_wake_times = dict.fromkeys(agents, [])
	print("Generating wake times...")
	for agent in tqdm(agent_info):
	    wake_times = generate_wake_times_quick(agent_id=agent[0], trade_freq=agent[-2], sim_time=sim_time,rng=rng)
	    all_wake_times[str(agent[0])]=wake_times
	return all_wake_times




#### This is used to create a dictionary that specifies which agent to wake at each time step ####
'''Function to convert a list of agent wake-times to a list of times that specify which agents wake-up '''
'''Used to generate a dictionary that contains a list of times, and a list of agents that should be woken at those times
		@param wake_times: List of all wake times for each agent - i.e[ [2,4,5], [1,4]]


		@Return  wake_up_instances: Dictionary of relevant times, and list of agents to wake. i.e {1 :[2], 2:[1], 4:[1,2], 5:[1]}
		
	This is then used to incrfement the simulator and call the correct agent.
'''
def combine_agent_wake_times(all_wake_times):
	wake_up_instances= {}
	print("Combining wake times...")
	for k,v in tqdm(all_wake_times.items()):
	    for x in v:
	        wake_up_instances.setdefault(x,[]).append(int(k))
	return wake_up_instances


