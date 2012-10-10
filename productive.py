
def is_productive(program_class, program_name):
    '''
    Check if this program is in the list of productive programs.
    '''
    productive_class = ['terminal', 'texmaker', 'freemind', 'evince', 'inkscape', 'tk', 'thunar', 'gedit', 'thunderbird', 'eog', 'PyMOL', 'gimp']
    productive_name = ['Stack Overflow', 'matplotlib','Matplotlib', 'oxfordjournals', 'Python', 'NumPy', 'git', 'Git', 'OpenCL', 'PyMOL', 'Adobe Reader', 'Bio.', 'bio.', 'pylint', 'SciPy', 'scipy', 'genome', 'genomic', 'latex', 'LaTeX', 'pymol', 'autoconf', 'patch', 'fastq', 'texmaker', 'citeulike', 'thunar', 'xfce', 'calc', 'journal', 'tbi', 'lyx', 'pkerpedjiev', 'coordinate', 'rna', 'phaistos', 'acs', 'univis', 'profiling', 'cython', 'web of knowledge', 'scopus', 'mayavi','libreoffice', 'springerlink', 'pubmed', 'ncbi.nlm', 'Staufen1', 'rcsb protein', 'ribozyme', 'rcsb pdb', 'ubuntu', 'vimoutliner', 'syntaxhighlighter', 'css', 'atomic resolution', 'arxiv.org', 'tandfonline', 'mak research', 'view-source', 'burrows-wheeler', 'd3', 'monte carlo', 'glmol', 'webgl', 'pkerp', 'genetics.org', 'pssm', 'sozi']

    #unproductive_name = ['window_focus']
    unproductive_name = []

    for p in unproductive_name:
        if program_name.lower().find(p.lower()) >= 0:
            return False

    for p in productive_class:
        if program_class.lower().find(p.lower()) >= 0:
            return True

    for p in productive_name:
        if program_name.lower().find(p.lower()) >= 0:
            return True

    return False
