

class Minterm:

    MAX_COUNT=4 # static

    # def __init__(self):
    #     self.numbers=[]
    #     self.binary = ''
    #     self.num1=0
    #
    # def __init__(self, numbers):
    #     self.__init__(numbers, self.getBinary(), self.getNum1())
    #
    # def __init__(self, numbers, binary):
    #     self.__init__(numbers, binary, self.getNum1())

    def __init__(self, numbers):
        self.numbers = numbers
        self.binary = self.getBinary()
        self.num1 = self.getNum1()

    # 01-0 형태로 반환
    def getBinary(self):
        if len(self.numbers)==0:
            return ''
        if len(self.numbers)==1:
            b = str(format(int(self.numbers[0]),'b'))
            self.binary = (Minterm.MAX_COUNT-len(b))*'0' + b
            return self.binary
        binArr = []
        for i in range(len(self.numbers)):
            t = format(int(self.numbers[i]),'b')
            t = (Minterm.MAX_COUNT-len(t))*'0'+t
            binArr.append(t)

        result=''
        for i in range(0, Minterm.MAX_COUNT):
            t = binArr[0][i]
            isSame = True
            for j in range(1,len(binArr)):
                if t != binArr[j][i]:
                    isSame=False
                    break

            if isSame:
                result = result+t
            else:
                result = result+'-'
        return result

    # # of 1s
    def getNum1(self):
        if self.getBinary() != '':
            self.num1 = self.binary.count('1')
        return self.num1

    #  minterm 가능하면 추가
    def combineNum(self, number):
        self.numbers.append(number)
        self.binary = self.getBinary()
        self.num1 = self.getNum1()

    def __str__(self):
        return str(self.numbers) +" " + self.binary


if __name__ == '__main__':
    d = [0,4,8,12]
    print(Minterm(d))
