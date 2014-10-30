"Tools in the blast+ suite."
import tools
import os

VERSION='2.2.29'
URL_BASE = ''.join([
    'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/',
    VERSION,
    '/ncbi-blast-',
    VERSION,
    '+'
    ])

def get_url() :
    uname = os.uname()
    if uname[0] == 'Darwin' :
        osStr = 'universal-macosx'
    elif uname[0] == 'Linux' :
        if uname[4].endswith('64') :
            osStr = 'x64-linux'
        else :
            osStr = 'ia32-linux'
    else :
        raise NotImplementedError('OS {} not implemented'.format(uname[0]))
    return '{}-{}.tar.gz'.format(URL_BASE, osStr)

class BlastTools(tools.Tool) :
    subtoolName = None

    """
    Base class for tools in the blast+ suite.
       Subclasses must define class member subtoolName.

    Previous note said that this was an 'Abstract' base class.  If we want
    that, we have to make the class abstract though...
    """
    def __init__(self, install_methods = None) :
        assert(self.subtoolName is not None)
        if install_methods == None :
            target_rel_path = 'ncbi-blast-{}+/bin/{}'.format(VERSION,
                    self.subtoolName)
            url = get_url()
            install_methods = [tools.DownloadPackage(url, target_rel_path)]
        tools.Tool.__init__(self, install_methods = install_methods)

    def version(self) :
        return VERSION

    def execute(self, options={}, option_string="", post_cmd=""):
        """
        options may be specified as key-value pairs of the form (flag: value)
            Leading dashes, ('-' or '--'), should be included in the key
            For flags without value arguments, value should equal the empty str
            (order does not matter for bwa execution)
        option_string spefifies options in a preformatted string.
            An alternative to options, but may be use in conjuction as well.
        post_cmd is appended to the end of the command.  It is intended to be
            used as a pipe ("| <other shell command>").  Note that while it can
            be used to store output ("> output.sai"), it is preferable to use
            flags for this when available (-out output.sai")
        """

        assert(self.subtoolName is not None)
        option_str = '{} {}'.format(' '.join([ "{} {}".format(k, v) for k, v in
                                                options.items() ]),
                                    option_string
                                    )
        cmd = "{self.exec_path} {option_str} {post_cmd}".format(**locals())
        log.debug("Calling blast subtool {} with: {}".format(self.subtoolName,
            cmd))
        return os.system(cmd)

class BlastnTool(BlastTools) :
    subtoolName = 'blastn'





"""
# RUN BLASTN ANALYSIS
for sample in
do
for directory in
do
for temp in /broad/hptmp/andersen
do
for db in metag_v3.ncRNA.mRNA.mitRNA.consensus
do
i=1
j=1
for a in $temp/$sample.prinseq.1.split.*
do
bsub -R "rusage[mem=2]" -W 4:00 -o $directory/_logs/$sample.log.bsub.txt -P sabeti_meta -J $sample.$((j++)).bn "blastn -db /idi/sabeti-scratch/kandersen/references/blast/$db -word_size 16 -evalue 1e-6 -outfmt 6 -num_descriptions 2 -num_alignments 2 -query $a -out $temp/$sample.1.$db.$((i++)).txt"
done
done
done
done
done
for sample in
do
for directory in
do
for temp in /broad/hptmp/andersen
do
for db in metag_v3.ncRNA.mRNA.mitRNA.consensus
do
i=1
j=1
for b in $temp/$sample.prinseq.2.split.*
do
bsub -R "rusage[mem=$memory]" -W 4:00 -o $directory/_logs/$sample.log.bsub.txt -P sabeti_meta -J $sample.$((j++)).bn "blastn -db /idi/sabeti-scratch/kandersen/references/blast/$db -word_size 16 -evalue 1e-6 -outfmt 6 -num_descriptions 2 -num_alignments 2 -query $b -out $temp/$sample.2.$db.$((i++)).txt"
done
done
done
done
"""
