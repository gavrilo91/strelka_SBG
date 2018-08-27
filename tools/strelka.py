from sbg import cwl
from subprocess import check_call


@cwl.to_tool(outputs=dict(),
             docker='images.sbgenomics.com/gavrilo_andric/strelka:1')
def strelka(normal_bam: cwl.File(secondary_files='.bai',
                                 doc='Normal sample BAM or CRAM file. (no default)'),
            tumor_bam: cwl.File(secondary_files='.bai',
                                doc='Tumor sample BAM or CRAM file. [required] (no default)'),
            reference_fasta: cwl.File(secondary_files='.fai',
                                      doc='samtools-indexed reference fasta file [required]'),
            indel_candidates: cwl.File(
                doc='Specify a VCF of candidate indel alleles. These alleles are always '
                    'evaluated but only reported in the output when they are inferred to '
                    'exist in the sample. The VCF must be tabix indexed. All indel alleles'
                    ' must be left-shifted/normalized, any unnormalized alleles will be '
                    'ignored. This option may be specified more than once, multiple input '
                    'VCFs will be merged. (default: None)') = None,
            ):
    """
    Version: 2.9.7

    This script configures Strelka somatic small variant calling.
    You must specify an alignment file (BAM or CRAM) for each sample of a matched tumor-normal pair.

    Configuration will produce a workflow run script which
    can execute the workflow on a single node or through
    sge and resume any interrupted execution.

    :param normal_bam:
    :param tumor_bam:
    :param reference_fasta:
    :param indel_candidates:
    :return:
    """
    strelka_config_path = '/opt/bin/configureStrelkaSomaticWorkflow.py'
    strelka_cmd = [strelka_config_path]
    strelka_cmd += ['--normalBam', normal_bam['path']]
    strelka_cmd += ['--tumorBam', tumor_bam['path']]
    strelka_cmd += ['--referenceFasta', reference_fasta['path']]

    if indel_candidates:
        strelka_cmd += ['--indelCandidates', indel_candidates['path']]

    check_call(strelka_cmd)


if __name__ == '__main__':
    TOOL = strelka()
    TOOL.dump('test.cwl')
