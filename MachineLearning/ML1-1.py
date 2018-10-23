#!/usr/bin/python

ex1_1 = list(filter(lambda x: x%2==0, range(11)))
ex1_1 = [x for x in range(11) if x%2 == 0]
ex1_1 = list(range(0,11,2))
ex1_1 = list(range(11)[::2])

ex1_2 = [x for x in range(101) if x%15==0]
ex1_2 = [x*15 for x in range(int(100/15)+1)]

ex1_3 = list(range(15,0,-2))
ex1_3 = [x for x in range(15,0,-1) if x%2 == 1]
ex1_3 = [x for x in range(15,0,-2)]
ex1_3 = list(filter(lambda x: x%2==1, range(15,0,-1)))
ex1_3 = list(filter(lambda x: x%2==1, range(1,16)))[::-1]
ex1_3 = [x for x in range(16) if x%2 == 1][::-1]
ex1_3 = [x for x in range(1,16,2)][::-1]

ex1_4 = ["xx"]*5
ex1_4 = list(map(lambda x: "xx", range(5)))

ex1_5 = ["string"+str(x) for x in range(5,15)]
ex1_5 = list(map(lambda x: "string"+str(x), range(5,15)))
ex1_5 = list(map(lambda x: "string"+str(5+x), range(10)))

ex1_6 = ["1", 2, 3.0, 4]

ex1_7 = [x for x in range(100) if str(x).find("3")!=-1]
ex1_7 = list(filter(lambda x: str(x).find('3')!=-1, range(100)))
ex1_7 = [x*10+3 for x in range(3)] + [30+x for x in range(10)] + [x*10+3 for x in range(4,10)]