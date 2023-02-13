from runmpi import runMPI, ray

tut1s = []
for _ in range(4):
    tut1 = runMPI.remote(np=4, script="tut1.py")
    tut1s.append(tut1)

commands = ray.get([tut1.get_command.remote() for tut1 in tut1s])
for command in commands:
    print(' '.join(command))
results = ray.get([tut1.run.remote() for tut1 in tut1s])
for result_ in results:
    result = result_[0]
    print(result)