import numpy as np
import scipy.optimize as spo

rwlay=np.array([[511, 5],[901, 10],[977, 10],[1060, 11],[1143, 13],[1216, 14],[1380, 16],[1448, 18],[1557, 19],[1990, 27],[2063, 27],[2130, 27],[2230, 27],[2373, 31],[2540, 35],[2876, 44],[3442, 62],[3567, 63],[3991, 83],[4092, 84]])
tclay=np.array([[208, 2],[1638, 20],[2453, 34],[3036, 45]])
wlay=np.array([[39, 1],[200, 2],[396, 3],[584, 4],[619, 5],[678, 6],[746, 7],[825, 8],[961, 9],[1086, 9],[1122, 9],[1174, 10],[1220, 11],[1267, 11],[1317, 12],[1322, 12]])

def ratio_of(data):
        return data.T[1]/data.T[0]

lay_ratios=np.concatenate([ratio_of(rwlay), ratio_of(tclay), ratio_of(wlay)])
approaches=np.concatenate([rwlay.T[0], tclay.T[0], wlay.T[0]])

def shrunk_logistic(x, slope, intercept, ceiling):
        return ceiling*1/(1+np.exp(slope*x+intercept))

lay_ratio_fit=spo.curve_fit(shrunk_logistic, approaches, lay_ratios, bounds=([-np.inf, 0, 0], [1, np.inf, 0.033]))
lay_slope, lay_intercept, lay_ceiling=lay_ratio_fit[0]

rwdate=np.array([[511, 19,], [901, 38,], [977, 38,], [1060, 40,], [1143, 46,], [1216, 48,], [1380, 58,], [1448, 63,], [1557, 64,], [1990, 81,], [2063, 81,], [2130, 84,], [2230, 85,], [2373, 91,], [2540, 97,], [2876, 126,], [3442, 165,], [3567, 170,], [3991, 200,], [4092, 202]])
tcdate=np.array([[208, 12], [1638, 79], [2453, 116]])
wdate=np.array([[445, 11,], [593, 12,], [700, 14,], [783, 15,], [858, 19,], [925, 23,], [1000, 32,], [1086, 32,], [1122, 32,], [1174, 35,], [1220, 37,], [1267, 37,], [1317, 39,], [1322, 39,]])

date_ratios=np.concatenate([ratio_of(rwdate), ratio_of(tcdate), ratio_of(wdate)])
approaches=np.concatenate([rwdate.T[0], tcdate.T[0], wdate.T[0]])

date_ratio_fit=spo.curve_fit(shrunk_logistic, approaches, date_ratios, bounds=([-np.inf, 0, 0], [1, np.inf, 0.07]))
date_slope, date_intercept, date_ceiling=date_ratio_fit[0]
