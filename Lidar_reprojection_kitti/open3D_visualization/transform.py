import numpy as np 
import math
import sys

roll_angle  = float(sys.argv[1])
pitch_angle = float(sys.argv[2])
yaw_angle   = float(sys.argv[3])
x_offset    = float(sys.argv[4])
y_offset    = float(sys.argv[5])
z_offset    = float(sys.argv[6])

roll_mat  = np.zeros((3, 3), dtype=float)
pitch_mat = np.zeros((3, 3), dtype=float)
yaw_mat   = np.zeros((3, 3), dtype=float)

# make the roll matrix
roll_mat[0, 0] =  1
roll_mat[1, 1] =  math.cos(math.radians(roll_angle))
roll_mat[2, 2] =  roll_mat[1, 1]
roll_mat[1, 2] = -math.sin(math.radians(roll_angle))
roll_mat[2, 1] = -roll_mat[1, 2]

# make the pitch matrix
pitch_mat[0, 0] =  math.cos(math.radians(pitch_angle))
pitch_mat[2, 2] =  pitch_mat[0, 0]
pitch_mat[1, 1] =  1
pitch_mat[0, 2] =  math.sin(math.radians(pitch_angle))
pitch_mat[2, 0] = -math.sin(math.radians(pitch_angle))

# make the yaw matrix
yaw_mat[0, 0] =  math.cos(math.radians(yaw_angle))
yaw_mat[1, 1] =  yaw_mat[0, 0]
yaw_mat[0, 1] =  -math.sin(math.radians(yaw_angle))
yaw_mat[1, 0] =  -yaw_mat[0, 1]
yaw_mat[2, 2] = 1

mat_1 = np.dot(roll_mat, pitch_mat)
mat_2 = np.dot(mat_1,    yaw_mat)
translation_mat = np.array([[x_offset], [y_offset], [z_offset]])
mat_transform = np.hstack((mat_2, translation_mat))
mat_transform = np.vstack((mat_transform, [0., 0., 0., 1.]))

original_matrix = np.array([[-1.8658607504059743e-01, 4.1910175179716530e-01, 8.8856027271170102e-01, 3.8663984043110750e-02],
                            [-5.8488917853471156e-01, 6.7930668600681332e-01, -4.4322350476867911e-01, -1.6363076292564346e-01],
                            [-7.8936068145932858e-01, -11.0240862210545110e-01, 1.1837891104025566e-01, -1.9517701413214553e-01],
                            [0., 0., 0., 1.]])

#print(original_matrix)

mat_final = np.dot(mat_transform, original_matrix)
print(mat_final)
