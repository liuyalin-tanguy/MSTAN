import random
import numpy as np
import torch
from torch.distributions import Beta
from scipy.stats import beta as SCI_beta


def Loss_proba(alpha, beta, pi, y):
    beta_dist = Beta(alpha, beta)# 添加一个小数，防止生成函数的时候因为0的存在导致出现了问题

    PdfValues = beta_dist.log_prob(y.unsqueeze(-1)).exp()  # (32, 5, 3)

    weighted_pdf_values = (pi * PdfValues).sum(dim=2)  # (32, 5)

    loss = -weighted_pdf_values.log().mean()

    return loss

def GetY_pre(alpha, beta, pi,confidence):
    # alpha * pi / (alpha + beta)
    # y_pre = torch.div(torch.mul(alpha,pi), torch.add(alpha,beta)) #都是一对一的运算，(batch,tau,m)
    # y_pre = y_pre.sum(dim = 2)
    pi = pi.numpy()
    confidence = 0.2
    lower_bound_percentile = (1 - confidence) / 2
    upper_bound_percentile = 1 - lower_bound_percentile

    # 计算置信区间
    lower_bounds = SCI_beta.ppf(lower_bound_percentile, alpha, beta)
    upper_bounds = SCI_beta.ppf(upper_bound_percentile, alpha, beta)
    lower_bounds = np.sum(lower_bounds * pi,axis=2)
    upper_bounds = np.sum(upper_bounds * pi, axis=2)
    return lower_bounds,upper_bounds

def set_seed(seed = 100):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)

def Loss_value(Y_pre,Y):
    diff = torch.abs(Y_pre - Y)
    output = diff.mean()
    return output
