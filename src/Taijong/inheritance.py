class Person:
  def __init__(self,first,last):
    self.firstname = first
    self.lastname = last
    
  def info(self):
    print(f'{self.firstname} {self.lastname}')

class Member(Person):
  def __init__(self,first,last,member_id,fee):
    super().__init__(first,last)
    self.member_id = member_id
    self.fee = fee

  def info(self):
    super().info()
    print(f'會員編號：{self.member_id}，金額：{self.fee}')
  
  def get_discount(self):
    self.fee = self.fee - 0.1*self.fee
    print(f'折扣後{self.fee}元')

class GoldenMember(Member):
  def get_discount(self):
    self.fee = self.fee - 0.3*self.fee
    print(f'折扣後{self.fee}元')

  def info(self):
    super().info()
    print("您是金卡會員")

class SilverMember(Member):
  def get_discount(self):
    self.fee = self.fee - 0.2*self.fee
    print(f'折扣後{self.fee}元')

  def info(self):
    super().info()
    print("您是銀卡會員")

class NormalMember(Member):
  def info(self):
    super().info()
    print("您是我們的會員")

John = NormalMember('John','Tyler',2322, 5000)
John.get_discount()
John.info()

Tom = SilverMember('Tom', 'Lu', 2324, 5000)
Tom.get_discount()
Tom.info()

Susi = GoldenMember('Susi', 'Lopets', 2324, 5000)
Susi.get_discount()
Susi.info()