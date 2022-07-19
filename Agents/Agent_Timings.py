from Agents.Agent_Generation import generate_wake_times_quick
from tqdm import tqdm

#### GET ALL WAKE TIMES OF RANDOM AGENTS ####
def generating_agent_wake_times(agent_info, sim_time,rng):
	agents=[str(row[0]) for row in agent_info]
	all_wake_times = dict.fromkeys(agents, [])
	print("Generating wake times...")
	for agent in tqdm(agent_info):
	    agent_id, wake_times = generate_wake_times_quick(agent_id=agent[0], trade_freq=agent[-2], sim_time=sim_time,rng=rng)
	    all_wake_times[str(agent_id)]=wake_times
	return all_wake_times


#### This is used to create a dictionary that specifies which agent to wake at each time step ####
'''Function to convert a list of agent wake-times to a list of times that specify which agents wake-up '''
def combine_agent_wake_times(all_wake_times):
	wake_up_instances= {}
	print("Combining wake times...")
	for k,v in tqdm(all_wake_times.items()):
	    for x in v:
	        wake_up_instances.setdefault(x,[]).append(int(k))
	return wake_up_instances


