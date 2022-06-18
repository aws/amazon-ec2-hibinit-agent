sources:
	python3 setup.py sdist --formats=gztar
	mv dist/*.gz .
	rm -rf dist

clean:
	rm *.gz
	rm -rf ec2_hibinit_agent.egg-info 
