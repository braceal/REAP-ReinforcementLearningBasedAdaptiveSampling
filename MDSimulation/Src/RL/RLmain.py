# python 2.7 MSMbuilder 2.8
def rlmain(i):
	
	from scipy import io as sio
	import RLSim as rl
	import numpy as np 

	# inital state
	S_0 = [0] # inactive

	N = len(S_0) # number of parallel runs 
	nstepmax = 40
	print('Simulation length: ', nstepmax*0.005)
	W_0 = [[0.25, 0.25], [0.25, 0.25]] # initial geuss of weights for + - in x and y directions
	Ws = [] # series of weights
	newPoints_all=[]
	Ws.append(W_0)
	print('Weight', W_0)
	# run simulation
	my_sim = rl.mockSimulation()
	my_sim.tp = sio.mmread('../tProb.mtx')
	my_sim.x = np.load('../Gens_aloopRMSD.npy')
	my_sim.y = np.load('../Gens_y_KE.npy')
	my_sim.mapping = np.load('../map_Macro2micro.npy')


	#### first round
	trj1 = my_sim.run(S_0, nstepmax = nstepmax) # 1 x 1 x n_frames
	trj1 = my_sim.PreAll(trj1) # 1 x 1 x n_frames
	trjs = trj1[0] # 1 x n_frames
	trj1_Sp = my_sim.PreSamp_MC(trjs, N = 10) # pre analysis # 1 x n_samples
	trj1_Sp_theta = np.array(my_sim.map(trj1_Sp)) # [trjx, trjy]
	newPoints = my_sim.findStarting(trj1_Sp_theta, trj1_Sp, W_0, starting_n = N , method = 'RL') # needs 2 x something
	trjs_theta = trj1_Sp_theta
	trjs_Sp_theta = trj1_Sp_theta
	bad = False


	for round in range(100):
		my_sim.updateStat(trjs_theta) # based on all trajectories

		W_1 = my_sim.updateW(trjs_Sp_theta, W_0) # important
		W_0 = W_1
		Ws.append(W_0)
		print('Weight', W_0)
		if np.any(np.isnan(W_0)):
			bad=True
			print(bad)
			break
	
		oldTrjs = trjs
		trj1 = my_sim.run(newPoints, nstepmax = 5)
		trj1 = my_sim.PreAll(trj1)[0] # 2 x all points of this round
		com_trjs = np.concatenate((trjs, trj1))
	
		trjs = np.array(com_trjs)
		trjs_theta = np.array(my_sim.map(trjs))
	
		trjs_Sp = my_sim.PreSamp_MC(trjs, N = 10)
		trjs_Sp_theta = np.array(my_sim.map(trjs_Sp))
		newPoints = my_sim.findStarting(trjs_Sp_theta, trjs_Sp, W_1, starting_n = N , method = 'RL')
		newPoints_all.append(newPoints)


#my_sim.pltPoints(trjs_theta, trjs_Sp_theta, newPoints, round, weights=Ws)

	my_sim.pltPoints(trjs_theta[0], trjs_theta[1])
	print(newPoints_all)
	if not bad:
		np.save('w'+str(i), Ws)
		np.save('trjs_theta'+str(i), trjs_theta)


