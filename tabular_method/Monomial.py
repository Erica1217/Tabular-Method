
# 패트릭매소드에서 PI들의 곱을 표현하는 클래스
class Monomial:

    def __init__(self, pi):
        self.PIs = set(pi)

    def add_pi(self, pi):
        self.PIs.add(pi)
