''' Functions to generate agent information,
This information is then placed in a list of lists for the simulation torefer back to later.

The general setup of a particular agent row is
[agent_id, param_1, wake_frequencys, agent_type]
'''


from random import randrange
import random
import numpy as np





''' Generating Agents that will Trade '''
def generate_agent_info(num_agents,agent_info, min_freq, max_freq, linear=False):
    wake_freqs=[int(i) for i in np.linspace(min_freq,max_freq,num_agents)] if linear else [int(i) for i in np.logspace(min_freq, max_freq, base=2, num=num_agents)]
    for agent in range(num_agents):
        agent_info.append([agent,0,wake_freqs[agent],'Random']) #Agent_id, 0 - not required for this agent type, Wake_Frequency, Agent_type
    return agent_info


def generate_agent_info_trend(num_agents,agent_info, min_freq, max_freq, linear=False):
    wake_freqs=[int(i) for i in np.linspace(min_freq,max_freq,num_agents)] if linear else [int(i) for i in np.logspace(min_freq, max_freq, base=2, num=num_agents)]
    trend_period=[int(i) for i in np.linspace(min_freq,max_freq,num_agents)]
    previous_agent_length=len(agent_info)
    for agent in range(num_agents):
        agent_info.append([agent+previous_agent_length,trend_period[agent],wake_freqs[agent],'Trend']) #Agent_id, trend_period_length, Wake_Frequency, Agent_type
    return agent_info


def generate_agent_info_mean(num_agents,agent_info, min_freq, max_freq, linear=False):
    wake_freqs=[int(i) for i in np.linspace(min_freq,max_freq,num_agents)] if linear else [int(i) for i in np.logspace(min_freq, max_freq, base=2, num=num_agents)]
    trend_period=[int(i) for i in np.linspace(min_freq,max_freq,num_agents)]
    previous_agent_length=len(agent_info)
    for agent in range(num_agents):
        agent_info.append([agent+previous_agent_length,trend_period[agent],wake_freqs[agent],'Mean']) #Agent_id, mean_period_length, Wake_Frequency, Agent_type
    return agent_info

def generate_agent_info_spike(num_agents,agent_info, spike_times=[], spike_size=0.5):
    previous_agent_length=len(agent_info)
    for agent in range(num_agents):
        agent_info.append([agent+previous_agent_length,spike_size,spike_times,'Spike']) #Agent_id, Starting_Balance, Wake_Frequency
    return agent_info
