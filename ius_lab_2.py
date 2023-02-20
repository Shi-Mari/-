import matplotlib.pyplot as plt 
import math 

class Param():
    def __init__(self, h):
        self.h = h
        self.i = 0
        self.T = [0]
    def Time(self):
        self.i += 1
        self.T.append(self.h*self.i)
class Limiter(Param):
    def __init__(self, h, maxREG, maxV):
        super().__init__(h)
        self.v = 0
        self.maxREG = maxREG
        self.maxV = maxV
    def LimReg(self, REG):
        if abs(REG[self.i]) > self.maxREG:
            REG[self.i] = math.copysign(self.maxREG, REG[self.i])
    def LimV(self, REG):
        self.v = (REG[self.i] - REG[self.i-1])/self.h
        if abs(self.v) > self.maxV:
            REG[self.i] = REG[self.i-1] + math.copysign(self.maxV, self.v)*self.h
class Reg(Param):
    def __init__(self, h, kp, ki, kd, maxREG, maxV):
        super().__init__(h)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.reg_i = 0
        self.limiter = Limiter(self.h, maxREG, maxV)
        self.REG = [0]
        self.ERR = [inp(0)]
        self.U = [inp(0)]
    def Pid(self, X1):
        self.ERR.append(self.U[self.i] - X1)
        if (abs(self.REG[i-1]) < self.limiter.maxREG) & (abs(self.limiter.v) < self.limiter.maxV):
            self.reg_i += self.ki*self.h*self.ERR[self.i] 
        self.reg_d = self.kd*(self.ERR[self.i]-self.ERR[self.i-1])/self.h
        self.REG.append(self.kp*self.ERR[self.i] + self.reg_i + self.reg_d)
        self.limiter.LimReg(self.REG)
        self.limiter.LimV(self.REG)
class ObjControl(Param):
    def __init__(self, h):
        super().__init__(h)
        self.x2 = 0	
        self.X1 = [0]
    def Roots(self, REG):
        self.x2 += self.h*(REG + 0.15*math.sin(0.04*self.T[self.i]) - 0.1*self.x2 - 2*self.X1[self.i-1])/0.03 
        self.X1.append(self.X1[self.i-1] + self.h*self.x2) 

inp = lambda t: 1
		
reg = Reg(0.01, 0.1, 5, 0.25, 20, 5)
obj = ObjControl(0.01)

for i in range(1, 200, 1):
  reg.Time()
  reg.limiter.Time()
  obj.Time()  
  reg.U.append(inp(reg.T[i]))
  reg.Pid(obj.X1[i-1])
  obj.Roots(reg.REG[i])


plt.plot(reg.T, obj.X1, 'm', label = 'Вых. сигнал')
plt.plot(reg.T, reg.U, 'blueviolet', label = 'Вх. сигнал')
plt.plot(reg.T, reg.ERR, 'deepskyblue', label = 'Ошибка')
plt.plot(reg.T, reg.REG, 'royalblue', label = 'Упр. сигнал')
plt.legend(loc=4)

plt.figure()

inp = lambda t: math.sin(t)
		
reg = Reg(0.01, 0.1, 5, 0.25, 20, 5)
obj = ObjControl(0.01)

for i in range(1, 2000, 1):
  reg.Time()
  reg.limiter.Time()
  obj.Time()  
  reg.U.append(inp(reg.T[i]))
  reg.Pid(obj.X1[i-1])
  obj.Roots(reg.REG[i])


plt.plot(reg.T, obj.X1, 'm', label = 'Вых. сигнал')
plt.plot(reg.T, reg.U, 'blueviolet', label = 'Вх. сигнал')
plt.plot(reg.T, reg.ERR, 'deepskyblue', label = 'Ошибка')
plt.plot(reg.T, reg.REG, 'royalblue', label = 'Упр. сигнал')
plt.legend(loc=4)

plt.show()
