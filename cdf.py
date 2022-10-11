import numpy as np
import matplotlib.pyplot as plt

def read_list(f):
    lines = []
    with open(f) as file:
        for line in file: 
            line = line.strip() #or some other preprocessing
            lines.append(abs(float(line))) #storing everything in memory!
    print(lines)
    return lines

if __name__ == '__main__':
    intervals = read_list("xrpl_slippage.txt")
    inter = np.asarray(intervals)
    # print(inter)

    count, bins_count = np.histogram(inter, bins=200)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)


    intervals2 = read_list("uniswap_slippage.txt")
    inter2 = np.asarray(intervals2)
    # print(inter)
    
    count2, bins_count2 = np.histogram(inter2, bins=200)
    pdf2 = count2 / sum(count2)
    cdf2 = np.cumsum(pdf2)


    size = 14
    fig, ax = plt.subplots(figsize=(6,3.5))
    ax.plot(bins_count[1:], cdf, color='b',linewidth=3,label="XRPL AMM")
    ax.plot(bins_count2[1:], cdf2, color='r', linewidth=3,label="Uniswap V2")
    ax.set_ylabel('Cumulative Probability', fontsize = size)
    ax.set_xlabel('absolute value of slippage', fontsize = size)
    ax.tick_params(axis='both', which='major', labelsize=size)
    ax.grid(True)
    plt.legend(loc="lower right")
    fig.tight_layout()

    plt.show()