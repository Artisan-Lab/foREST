import threading
import time

class Timer(threading.Thread):
    '''
    一个简单的计时器
    '''
    def __init__(self, seconds):
        self.runTime = seconds
        threading.Thread.__init__(self)
    def run(self):
        time.sleep(self.runTime)
class CountDownTimer(Timer):
    '''
    倒计时器~~~
    '''
    def run(self):
        counter = self.runTime
        for sec in range(self.runTime):
            time.sleep(1.0)
            counter -= 1
        print('请求超时')
class CountDownExec(CountDownTimer):
    '''
    倒计时后对api请求的处理
    '''
    def __init__(self, seconds, action):
        self.action = action
        CountDownTimer.__init__(self, seconds)
    def run(self):
        CountDownTimer.run(self)
        self.action()
# def myAction():
#     print('action')
#
# if __name__ == '__main__':
#     t = CountDownExec(3, myAction())
#     t.start()







