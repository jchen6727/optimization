"""
ray with mpiexec through subprocess (mpiexec -n <# processors> nrniv -python -mpi <python script>
"""

import ray
import subprocess

ray.init()
@ray.remote
class runMPI(object):
    def __init__(self, np=1, script="hello_world.py"):
        self.np = np
        self.command = "mpiexec -n {} nrniv -python -mpi {}".format(np, script).split()
        self.pid = None

    def get_command(self):
        return self.command

    def run(self):
        self.proc = subprocess.run(self.command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        return self.stdout, self.stderr

"""
test = runMPI()
print(test.run())
"""

if __name__ == "__main__":

    hellos = []
    for _ in range(4):
        hello = runMPI.remote(np = 2, script = "hello_world.py")
        hellos.append(hello)

    commands = ray.get([hello.get_command.remote() for hello in hellos])
    for command in commands:
        print(' '.join(command))
    results = ray.get([hello.run.remote() for hello in hellos])
    for result_ in results:
        result = result_[0]
        print(result)
