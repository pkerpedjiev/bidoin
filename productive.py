
def is_productive(program_class, program_name):
    '''
    Check if this program is in the list of productive programs.
    '''
    productive_class = ['terminal', 'texmaker', 'freemind', 'evince', 'inkscape', 'tk', 'thunar', 'gedit', 'thunderbird', 'eog', 'PyMOL', 'gimp', 'r graphics', 'emacs', 'pidgin']
    productive_name = ['Stack Overflow', 'matplotlib','Matplotlib', 'oxfordjournals', 'Python', 'NumPy', 'git', 'Git', 'OpenCL', 'PyMOL', 'Adobe Reader', 'Bio.', 'bio.', 'pylint', 'SciPy', 'scipy', 'genome', 'genomic', 'latex', 'LaTeX', 'pymol', 'autoconf', 'patch', 'fastq', 'texmaker', 'citeulike', 'thunar', 'xfce', 'calc', 'journal', 'tbi', 'lyx', 'pkerpedjiev', 'coordinate', 'rna', 'phaistos', 'acs', 'univis', 'profiling', 'cython', 'web of knowledge', 'scopus', 'mayavi','libreoffice', 'springerlink', 'pubmed', 'ncbi.nlm', 'Staufen1', 'rcsb protein', 'ribozyme', 'rcsb pdb', 'ubuntu', 'vimoutliner', 'syntaxhighlighter', 'css', 'atomic resolution', 'arxiv.org', 'tandfonline', 'mak research', 'view-source', 'burrows-wheeler', 'd3', 'monte carlo', 'glmol', 'webgl', 'pkerp', 'genetics.org', 'pssm', 'sozi', 'vtk', 'r graphics', 'trello', 'amino acid', 'sciencemag', 'ggplot', 'r_x11', 'markdown', 'networkx', 'regexp', 'sympy', 'gdb', 'sra', 'primers', 'cutadapt', 'ernwin', 'GEO Accession', 'qstat', 'awk', 'Least Squares', 'partition', 'boltzmann', 'shell command', 'inkscape', 'duolingo', 'alignment', 'bayes', 'linux', 'annoe', 'spherical data', 'read_mapping', 'gromacs', 'charmm', 'peptide', 'fwspidr', 'MMTSB', 'force-directed', 'Frellsen', 'Fruchterman', 'jar3d', '1gid', 'il_', 'current_plot', 'tristetraprolin', 'makefile', 'Untitled0', 'backtest', 'response to reviews', 'emptypipes', 'Google Fonts', 'bootstrap', 'k-d tree', 'quadtree', '3D-Printing', 'kink turn', 'aminor_probabilities', 'rosetta_benchmark', 'kl-divergence', 'organized_plots', 'work_targets', 'benchmarks','predicted_secondary_structure', 'proposal distribution', 'toodledoo', 'angle_stats_clustering_and_divergence', 'spherical coordinate', 'toodledo', 'Scientific poster design', 'linkedin' ]

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
