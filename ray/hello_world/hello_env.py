import os

# subprocess vars
env_vars = ['SBP_A', 'SBP_B', 'SBP_C']
envd = {key: os.getenv(key) for key in env_vars}

# process id
pid = os.getpid()

# print statement
print("hello world!\nmy id is {}".format(pid))
for key in envd:
    print("{}: {}".format(key, envd[key]))
