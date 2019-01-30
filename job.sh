#!/bin/bash
#SBATCH --time=8:00:00
#SBATCH --mem=255G
#SBATCH --account=YOURACCOUNT
#SBATCH --cpus-per-task=24
#SBATCH --mail-user=YOUREMAIL
#SBATCH --mail-type=ALL
module load python
python3 deploy.py
