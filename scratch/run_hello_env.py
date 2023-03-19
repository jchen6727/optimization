from runmpi import runMPI, ray

NR = 4
ray.init()

envs = [{'SBP_A': "A{}".format(a), 'SBP_B': "B{}".format(b), 'SBP_C': "C{}".format(c)}
        for a, b, c in zip(range(NR), range(NR), range(NR))]

runners = []
for _ in range(NR):
    runner = runMPI.remote(np=4, script="hello_env.py")
    runners.append(runner)

commands = ray.get([runner.get_command.remote() for runner in runners])
for command in commands:
    print(' '.join(command))

envs = ray.get([runner.add_env.remote(env) for runner, env in zip(runners, envs)])

results = ray.get([runner.run.remote() for runner in runners])
for result_ in results:
    result = result_[0]
    print(result)