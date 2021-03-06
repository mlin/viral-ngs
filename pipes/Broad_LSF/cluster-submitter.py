#!/usr/bin/env python3
import os, sys, re
from snakemake.utils import read_job_properties

LOGDIR = sys.argv[-2]
jobscript = sys.argv[-1]
mo = re.match(r'(\S+)/snakejob\.\S+\.(\d+)\.sh', jobscript)
assert mo
sm_tmpdir, sm_jobid = mo.groups()
props = read_job_properties(jobscript)

# set up job name, project name
jobname = "{rule}-{jobid}".format(rule=props["rule"], jobid=sm_jobid)
if props["params"].get("logid"):
    jobname = "{rule}-{id}".format(rule=props["rule"], id=props["params"]["logid"])
cmdline = "bsub -P {proj_name} -J {jobname} ".format(
    proj_name='viral_ngs', jobname=jobname)

# log file output
if "-N" not in props["params"].get("LSF",""):
    cmdline += "-oo {logdir}/LSF-{jobname}.txt ".format(
        logdir=LOGDIR, jobname=jobname)

# rule-specific LSF parameters (e.g. queue, runtime, memory)
cmdline += props["params"].get("LSF","") + " "

# figure out job dependencies
dependencies = sys.argv[1:-2]
if dependencies:
    cmdline += "-w '{}' ".format(" && ".join(dependencies))

# the actual job
cmdline += jobscript

# the success file
cmdline += " %s/%s.jobfinished" % (sm_tmpdir, sm_jobid)

# the part that strips bsub's output to just the job id
cmdline += " | tail -1 | cut -f 2 -d \< | cut -f 1 -d \>"

# call the command
os.system(cmdline)
