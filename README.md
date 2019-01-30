

# README

### Launching processes in parallel

This is a simple collection of bash/python scripts that allow you to run up to k processes in parallel, typically on a cluster. At the end of execution, the exitcodes of the processes are reported to you.

A typical use case is to run grid search, or process a whole set of files, and so on.

To avoid swamping the OS/RAM/IO only k processes are run in parallel.

### Requirements

* Unix environment
* Python >= 3.5 

### Getting started

```bash
$python deploy.py
```

This will run 15 jobs, executing a very simple bash script with a grid search of parameters.

#### Running your own code

* Create a config.json (see demo.ipynb for simple way to do this)

  * This should specify at least
    * script path
    * script name
    * batch size : how many processes to execute in parallel

* Change deploy.py for the parameters you want to pass, if any

* On a slurm cluster

  * Edit job.sh with your account credentials

  * ```bash
    $sbatch job.sh
    ```


