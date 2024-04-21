'''index = 0
for b in B_angle:
    if x[b[0]][b[1]] == 0:
        index = B.index(b)
        B.remove(b)
        break
print(index)'''
''' B_new = B
if index != 0 and index != len(B):
    B_new = B[:index][::-1] + [B[-1]] + B[index:len(B)-1]

if B_new == [[1, 1], [1, 2], [2, 0], [2, 2], [0, 2]]:
    B_new = [[2, 0], [1, 0], [1, 1], [0, 1], [0, 2]]

print(x)
print(B)
print(B_new)'''

''' a_vals = []
  b_vals = []
  for i, j in B:
      u_vals = [0] * a.shape[0]
      v_vals = [0] * b.shape[0]
      u_vals[i] = 1
      v_vals[j] = 1
      a_vals.append(u_vals + v_vals)
      b_vals.append(c[i, j])
  u_vals = [0] * (a.shape[0] + b.shape[0])
  u_vals[0] = 1
  a_vals.append(u_vals)
  b_vals.append(0)

  sol = np.linalg.solve(a_vals, b_vals)
  u = sol[:len(a)]
  v = sol[len(b):]'''

'''
    B_super = [B[-1]] + B + [B[0]]
    for i in range(len(B_super) -2):
        if is_angle_component(B_super[i], B_super[i+1], B_super[i+2]):
            B_angle.append(B_super[i+1])
            '''
