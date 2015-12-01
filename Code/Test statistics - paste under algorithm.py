#--------------------return the timing of the results--------------------------------------------#
averages = []
for i in range(0,100):
    times = []
    for j in range(0,100):
        start = timeit.default_timer()
        algorithm();
        end = timeit.default_timer() - start
        if i is not 0:
            times.append(end)

    #print max(times), min(times), numpy.mean(times)
    averages.append(numpy.mean(times))

#--------------------------display results in histogram------------------------------------------#
'''
Creating a histogram, edited from http://matplotlib.org/1.5.0/examples/animation/histogram.html 
'''
"""
This example shows how to use a path patch to draw a bunch of
rectangles for an animated histogram
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

fig, ax = plt.subplots()

# histogram our data with numpy
data = averages
n, bins = numpy.histogram(data, 100)

# get the corners of the rectangles for the histogram
left = numpy.array(bins[:-1])
right = numpy.array(bins[1:])
bottom = numpy.zeros(len(left))
top = bottom + n
nrects = len(left)

# here comes the tricky part -- we have to set up the vertex and path
# codes arrays using moveto, lineto and closepoly

# for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
# CLOSEPOLY; the vert for the closepoly is ignored but we still need
# it to keep the codes aligned with the vertices
nverts = nrects*(1 + 3 + 1)
verts = numpy.zeros((nverts, 2))
codes = numpy.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

barpath = path.Path(verts, codes)
patch = patches.PathPatch(
    barpath, facecolor='red', edgecolor='purple', alpha=0.5)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())


def animate(i):
    # simulate new data coming in
    data = averages
    n, bins = numpy.histogram(data, 100)
    top = bottom + n
    verts[1::5, 1] = top
    verts[2::5, 1] = top
    return [patch, ]

ani = animation.FuncAnimation(fig, animate, 1, repeat=False, blit=True)
plt.show()


#   ****
#   ****
#   ****
#   ****
#   ****
#   ****
#   ****
#   ****
#   ****

# ----------------- part to do the displaying of the results ------------------ #








# part to display the return results.
