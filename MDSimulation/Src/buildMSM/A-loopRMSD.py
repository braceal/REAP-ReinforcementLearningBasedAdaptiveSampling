import glob
import numpy as np
import mdtraj as md

topFile = 'csrc_inactive.pdb'
top = md.load(topFile).topology

# aloop
aloop_select = 'resid 144 to 164'
aloop_atomIndex = top.select(aloop_select)

# ref aloop
aloop_ref = md.load(topFile).atom_slice(aloop_atomIndex)

#############
for file in glob.glob('*/*.lh5'):
	print(file)
	t = md.load(file)

	# aloop RMSD
	t2 = t.atom_slice(aloop_atomIndex)
	r = md.rmsd(t2, aloop_ref)
	np.save(file.replace('.lh5','_aloopRMSD.npy'), r)
    
    
#########
import glob
import numpy as np
import mdtraj as md

file = 'MSM_traj_csrc_100microsecs.pdb'
refFile = 'csrc_inactive.pdb'

trj = md.load(file)
top = trj.topology

# aloop
aloop_select = 'resid 144 to 164'
aloop_atomIndex = top.select(aloop_select)

# ref aloop
aloop_ref = md.load(refFile).atom_slice(aloop_atomIndex)

t2 = t.atom_slice(aloop_atomIndex)
r = md.rmsd(t2, aloop_ref)

np.save('MSM_traj_csrc_100microsecs__aloopRMSD.npy', r)

