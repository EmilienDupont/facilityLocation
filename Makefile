all:
	./SimpleServer.py

test:
	./facility.py

clean:
	-rm gurobi.log *.pyc *.lp
