import scipy.interpolate

#x1 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
#y2 = [4, 7, 11, 16, 22, 29, 38, 49, 63, 80]


def interpolate(list_x, list_y, x):
    flag=0              # out of bounds flag: 0=not out of bounds; 1=Error: out of bounds
    y=0
    if x<min(list_x) or x>max(list_x):
        flag=1
        return (flag, y)
    y_interp = scipy.interpolate.interp1d(list_x, list_y)
    y=y_interp(x)
    return (flag, y)

#print(interpolate(x1, y2, 3))
#print(interpolate(x1, y2, 5.235152))
#print(interpolate(x1, y2, 19))
#print(interpolate(x1, y2, 80))
#(a,b)=interpolate(x1, y2, 19)
#print(b)