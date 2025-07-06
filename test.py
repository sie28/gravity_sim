# import matplotlib as mpl
# print(mpl.rcParams['animation.ffmpeg_path'])


# from matplotlib.animation import FFMpegWriter

# Writer = FFMpegWriter(fps=30, codec='libx264')
# ani.save('test.mp4', writer=Writer)

import subprocess
result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
print(result.stdout)