import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
import os
current = os.getcwd()
# file_dir = current +'\\Hopfield_dataset\\'
file_dir = current +'\\'
def readFile(flag):
    if flag == "Basic":
        train_file_name = file_dir+'Basic_Training.txt'
        test_file_name = file_dir+'Basic_Testing.txt'
    elif flag == "Bonus":
        train_file_name = file_dir+'Bonus_Training.txt'
        test_file_name = file_dir+'Bonus_Testing.txt'
    # with open(file_dir+'Basic_Training.txt','r') as trainfile:

    with open(train_file_name,'r') as trainfile:
        # tmp = np.zeros((9,12),0)
        stringIO = ''
        Tmp_pattern = []
        Tmp_train = []
        train_Pattern = []
        train_Picture = []
        for line in trainfile.readlines():
            if len(line) <= 1:
                # c = StringIO(stringIO)
                # print(np.loadtxt(c))
                np_tmp = np.array(Tmp_pattern)
                np_train = np.array(Tmp_train)
                # print(len(np_tmp))
                # print(np_tmp.shape)
                train_Pattern.append(np_tmp)
                train_Picture.append(np_train)
                Tmp_pattern= []
                Tmp_train= []
            else:
                tmp = []
                ptmp = []
                # print(len(line))
                for char in line:
                    if char == ' ':
                        tmp.append(np.array([-1]))
                        ptmp.append(np.array(0))
                    elif char == '\n':
                        continue
                    else:
                        tmp.append(np.array([1]))
                        ptmp.append(np.array(1))
                Tmp_pattern.extend(tmp)
                Tmp_train.append(ptmp)
            # print(Tmp_pattern)
            # input()
    # print("Pattern: ",len(np.array(train_Pattern)))
    # print("Pattern[0]: ",np.array(train_Pattern).shape)

    # with open(file_dir+'Basic_Testing.txt','r') as testfile:
    with open(test_file_name,'r') as testfile:
        # tmp = np.zeros((9,12),0)
        stringIO = ''
        Tmp_pattern = []
        test_Pattern = []
        for line in testfile.readlines():
            if len(line) <= 1:
                # c = StringIO(stringIO)
                # print(np.loadtxt(c))
                np_tmp = np.array(Tmp_pattern)
                # print(len(np_tmp))
                # print(np_tmp.shape)
                test_Pattern.append(np_tmp)
                Tmp_pattern= []
            else:
                tmp = []
                # print(len(line))
                for char in line:
                    if char == ' ':
                        tmp.append(np.array([-1]))
                    elif char == '\n':
                        continue
                    else:
                        tmp.append(np.array([1]))
                Tmp_pattern.extend(tmp)
            # print(Tmp_pattern)
            # input()
                 #(3,12,9)
    draw_picture(np.array(train_Picture),flag+'_origin')
    # draw_picture(np.array(train_Picture),'Basic_origin')
                    #(3,108,1)              #(3,108,1)
    return np.array(train_Pattern),np.array(test_Pattern)
def addNoise(data,rate):
    print("addNoise")
    # with open(file_dir+'Basic_Training.txt','r') as trainfile:
    new_pattern = data.copy()
    print(len(data))
    for idx in range(len(new_pattern)):
        rand = random.uniform(0, 1)
        # print("rand: ",round(rand,2))
        # print("origin: ",new_pattern[idx])
        if round(rand,2) < float(rate):
            new_pattern[idx] *= -1
            # print("after:",new_pattern[idx])
    return new_pattern

def transport(input):
    weight_sum = np.zeros((len(input[0]),len(input[0])))
    # print(weight_sum.shape)
    for data in input:
        # print("data:",data.shape)
        # print("data:",(data*data.T).shape)
        weight_sum += data*data.T
        # print(weight_sum)
    # print("weight_sum.shape",weight_sum.shape)
    return weight_sum
def getTheta(weight):
    theta = np.sum(weight,axis=1)
    # for data in weight:
    #     total = 0
    #     for d in data:
    #         total+=d
    #         print(d)
        # print("total:",total)
        # print("theta shape:",theta.shape)
        # print("theta:",theta[0])
        # input()
    # print(theta)
    return theta
def Hopfield_energy_function(weights,inputs,thetas):
    # print("inputs:",inputs.shape)
    # print("inputs:",inputs[0:5])
    # print("thetas:",np.array([thetas]).shape)
    # print("weights:",weights.shape)
    # print("np.sum(inputs*thetas): ",np.sum(inputs*thetas))
    # print("(inputs.T*weights*inputs)/2",np.dot(np.dot(inputs.T,weights),inputs)/2)
    # print("(inputs.T*weights*inputs)/2: ",np.sum(np.sum(inputs.T*weights)*inputs)/2)
    # value = np.dot(np.dot(inputs.T, weights), inputs) / 2 * (-1)
    E = np.sum(np.sum(inputs.T*weights)*inputs)/2*(-1) + np.sum(inputs*thetas)
    # E = -0.5 * inputs @ @ s + np.sum(s * self.threshold)
    # print("E:",E)
    return E
def asy_recall(input,weight,theta):
    new_value = -100
    new_vector = []
    #Iteration = 20
    # print(len(theta))
    compute = input.copy()
    result = input.copy()
    #(weights,inputs,thetas)
    E = Hopfield_energy_function(weight,input,theta)
    for i in range(20):
        print("i:",i)
        new_vector = []
        for idx in range(len(theta)):
            # print("idx:",idx)
            # print("before:",compute[idx][0])
            value = np.sign(np.dot(weight[idx],compute))[0]
            # value = np.sign(np.dot(weight[idx],compute)[0]-theta[idx])

            # print("value: ",value)
            compute[idx][0] = value
            # print("after:",compute[idx][0])

            # print("input: ",input)
            # print("compute: ",compute)
            # compute = input
            # print("weight: ",weight[idx])
            # print(input)
            # print("--: ",np.dot(weight[idx],compute)-theta[idx])

            # if np.dot(weight[idx],compute) > theta[idx]:
            #     new_value = 1
            #     compute[idx] = new_value
            # elif np.dot(weight[idx],compute) == theta[idx]:
            #     new_value = input[idx]
            # elif np.dot(weight[idx],compute) < theta[idx]:
            #     new_value = -1
            # compute[idx] = new_value

            # print("input: ",input)
            # print("compute: ",compute)

        E_new = Hopfield_energy_function(weight,compute, theta)
        # print("compute: ",compute[0:6])
        # print("input: ",input[0:6])
        print("E: ",E)
        print("E_new: ",E_new)
        if E == E_new:
            # print("if:",(compute == result).all())
            return compute
        else:
            #(A==B).all()
            # print("else:",(compute == result).all())
            E = E_new
            result = compute.copy()
        # if np.array_equal(compute, result):
        #     return compute
        # else:
        #     result = compute
    return compute

def draw_picture (picture,file_name):
    print("draw_picture")
    print(len(picture))
    for i in range(len(picture)):
        sns.set()
        ax = sns.heatmap(picture[i])
        if len(picture) == 1:
            plt.savefig(file_dir + file_name + ".png")
        else:
            plt.savefig(file_dir+file_name+str(i)+".png")
        # plt.show()
        # input()
        plt.clf()
def small_test():
    I = np.eye(4, dtype=int)
    X = np.array([[[1], [-1], [-1], [-1]], [[-1], [1], [1], [-1]], [[-1], [1], [1], [1]]])
    print("X:", X.shape)
    P = 4
    N = 3
    return X,P,N,I

def RecallPicture(flag,isNoise,assign_patern, weight, theta):
    print("RecallPicture")
    test = assign_patern
    answer = asy_recall(test, weight, theta)
    remebers = []
    if flag == 'Basic':
        remeber = np.reshape(answer, (12, 9))
        # print(remeber.shape)
        remebers.append(remeber)
        return remebers
    elif flag == 'Bonus':
        remeber = np.reshape(answer, (10, 10))
        # print(remeber.shape)
        remebers.append(remeber)
        return remebers
def getGUI(flag,isNoise,assign_idx,rate):
    # (str(data[0]), isNoise_signal, int(data[1]), noise_rate)
    print("rate:",rate)
    X, Y = readFile(flag)
    P = len(X[0])
    N = X.shape[0]
    print("P:",P)
    print("N:", N)
    weight_sum = transport(X)
    I = np.eye(P, dtype=int)
    weight = weight_sum / P - (N / P)*I
    theta = []
    # print(weight.shape)
    assign_pattern = Y[assign_idx]

    theta = getTheta(weight)
    if isNoise == True:
        noise_pattern = addNoise(assign_pattern,rate)
        print("noise_pattern: ",noise_pattern.shape)
        result = RecallPicture(flag,isNoise, noise_pattern, weight, theta)
        print("result: ",result[0].shape)
        if flag == 'Basic':
            npattern = np.reshape(noise_pattern, (12, 9))
        else:
            npattern = np.reshape(noise_pattern, (10, 10))
        draw_picture([npattern], flag + "_" + "noise" + str(rate) + "_" + str(assign_idx))
        draw_picture(result, flag + "_" + "noise" + str(rate) + "_recall" + str(assign_idx))
    else:
        result = RecallPicture(flag,isNoise, assign_pattern, weight, theta)
        draw_picture(result, flag + "_recall" + str(assign_idx))

# if __name__ == '__main__':
#     # X, P, N, I = small_test()
#     flag = 'Basic'
#     X,Y = readFile(flag)
#     P = len(X[0])
#     N = X.shape[0]
#     # print("P:",P)
#     print("N:",N)
#     # print("X:",X.shape)
#     # print("Y:",Y.shape)
#     weight_sum = transport(X)
#     I = np.eye(P, dtype=int)
#     # print((I*N)/P)
#     weight = weight_sum/P - (I*N)/P
#     # print(weight)
#     theta = []
#     # print(weight.shape)
#     theta = getTheta(weight)
#
#     remebers = []
#     # for i in range(len(Y)):
#     #     test = Y[i]
#     #     print("test: ",test.shape)
#     #     answer = asy_recall(test,weight,theta)
#     #     # remeber = np.reshape(answer, (12, 9))
#     #     remeber = np.reshape(answer, (10,10))
#     #     print(remeber.shape)
#     #     remebers.append(remeber)
#     # remebers = np.array(remebers)
#     '''small test'''
#
#     # draw_picture(remebers, 'Bonus_recall')
#     draw_picture(remebers, 'Basic_noise_recall' )
#     # draw_picture(remebers, 'Basic_recall_' )
