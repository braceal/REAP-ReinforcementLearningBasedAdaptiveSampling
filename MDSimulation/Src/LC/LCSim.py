# ipython2 SLmain.py

class mockSimulation:
        ## public
        def __init__(self):
                self.theta_mean = [0, 0]
                self.theta_std = [0, 0]
                self.r = 1#number of rounds
                self.s = 1# length of simulations
                self.N = 1# number of parallel simulations
                self.tp = None
                self.mapping = None
                self.x = None
                self.y = None
                
        def run_multipleSim(self):
                return True
        def runNxtRound(self):
                return True
                
        
        ## private
        def PreAll(self, trj):
                """
                Pre-Sampling:
                        choose states with minimum counts or newly discovered states
                output:
                        trj with shape of [[Xs][Ys]]
                """
                import numpy as np
                comb_trj = np.concatenate(trj)
                return trj

                
        def map(self, trj_Ps):
                """

                output:
                      n_ec x n_frames
                """
                # map coordinate space to reaction coorinates space
                import numpy as np
                trj_x = []
                trj_y = []
                x = self.x
                y = self.y
                map = self.mapping
                for MacroFrame in trj_Ps:
                    microFrame = map[int(MacroFrame)]
                    trj_x.append(x[microFrame])
                    trj_y.append(y[microFrame])

                return [trj_x, trj_y]

        def PreSamp_MC(self, trj, N = 20):
                """
                Pre-Sampling for Monte Carlo simulations:
                        choose states with minimum counts or newly discovered states
                        
                output:
                        trj with shape of 
                """
                import numpy as np
                cl_trjs = trj             
                unique, counts = np.unique(cl_trjs, return_counts=True)
                leastPop = counts.argsort()[:N]
                init_cl = [int(unique[i]) for i in leastPop]
                return init_cl

        
        def run(self, inits, nstepmax = 10):
                """
                Parameters
                ----------
                initi : 
                        initial state (singe state)
                msm :
                        reference MSM
                s :
                        lenght (number of steps) of each simulation	
                
                output :
                        final trajectory
                """
                import numpy as np
                import msmbuilder as msmb
		
                #msm = self.msm
                tp = self.tp
                N = len(inits)
                trjs = np.empty([N, nstepmax])
                for n in range(N):
                        init = np.int(inits[n])
                        trj = msmb.msm_analysis.sample(tp, init, nstepmax)
                        #trj = msm.sample_discrete(state=init, n_steps=nstepmax, random_state=None)
                        trjs[n] = trj
                return trjs
                

        def pltPoints(self, x, y):
            import matplotlib.pyplot as plt
            import numpy as np

            figName = 'fig.png'

            fig = plt.figure()
            ax = fig.add_subplot(111)
            
            
            #ax.scatter(x , y, color='darkorange', s=10, alpha=0.2)
            ax.scatter(x + np.random.normal(0, 0.06/4, len(x)), y+np.random.normal(0, 0.06, len(y)), color='darkorange', s=10, alpha=0.2)
            plt.xlabel('RMSD of A-loop (nm)')
            plt.ylabel(r'$d_E 310-R409 - d_K295 - E310$')
            #plt.ylabel(r'$d_E_310_-_R_409  - d_K_295_-_E_310 (nm)$')
            plt.ylim([-2, 2])
            plt.xlim([0, 1])
#            plt.show()
            fig.savefig('fig.png', dpi=1000, bbox_inches='tight')

            return 
       
        def findStarting(self, trj_Ps_theta, trj_Ps, W_1, starting_n=10 , method = 'LC'):
                """
                trj_Ps_theta: 
                         size n_theta x n_frames
                trj_Ps:
                """
		# As you have already done least count in finding Sp, then just pick to Sps as least counts
                import numpy as np               
                n_coord = 1                     
		newPoints_index = range(starting_n) 
                newPoints = [trj_Ps[int(i)] for i in newPoints_index]
                return newPoints

        def findStarting_RL(self, trj_Ps_theta, trj_Ps, W_1, starting_n=10 , method = 'RL'):
                """
                trj_Ps_theta: 
                         size n_theta x n_frames
                trj_Ps:
                """
                # get new starting points (in theta domain) using new reward function based on updated weigths (W_1)
                import numpy as np               
                theta_mean = []
                theta_std = []
                for theta in range(len(W_1)):
                        theta_mean.append(np.mean(trj_Ps_theta[theta]))
                        theta_std.append(np.std(trj_Ps_theta[theta]))
                        
                ranks = {}
                trj_Ps_theta = np.array(trj_Ps_theta)
                for state_index in range(len(trj_Ps_theta[0])):
                        state_theta = trj_Ps_theta[:,state_index]
                        
                        r = self.reward_state( state_theta, theta_mean, theta_std, W_1)
                        
                        ranks[state_index] = r

                newPoints_index0 = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[0:starting_n] 
                newPoints_index = np.array(newPoints_index0)[:,0]   
                
                #n_coord = len(trj_Ps)
                n_coord = 1                     
                #newPoints = []
                newPoints = [trj_Ps[int(i)] for i in newPoints_index]
                #for coord in range(n_coord):
                #          newPoints.append([trj_Ps[coord][int(i)] for i in newPoints_index])                                   
                return newPoints




