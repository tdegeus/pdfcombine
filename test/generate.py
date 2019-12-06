import matplotlib.pyplot as plt

for i in range(1, 4):
    fig, ax = plt.subplots()
    ax.plot([0, 2], [0, 2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.savefig('fig{0:d}.pdf'.format(i))
    plt.close()
