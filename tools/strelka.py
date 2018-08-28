from sbg import cwl
from tools.doc import TOOL_DOC
from subprocess import check_call, check_output


@cwl.to_tool(outputs=dict(stats_log=cwl.File(glob='results/stats/runStats.tsv'),
                          somatic_snvs=cwl.File(glob='results/variants/somatic.snvs.vcf.gz',
                                                secondary_files='.tbi',
                                                doc="All somatic SNVs inferred in the tumor sample"),
                          somatic_snvs_tbi=cwl.File(glob='results/variants/somatic.snvs.vcf.gz.tbi'),
                          somatic_indels=cwl.File(glob='results/variants/somatic.indels.vcf.gz',
                                                  secondary_files='.tbi',
                                                  doc="All somatic Indels inferred in the tumor sample"),
                          somatic_indels_tbi=cwl.File(glob='results/variants/somatic.indels.vcf.gz.tbi')
                          ),
             docker='images.sbgenomics.com/gavrilo_andric/strelka:1',
             label="Strelka 2.9.7")
def strelka(normal_bam: cwl.File(secondary_files='.bai',
                                 doc='Normal sample BAM or CRAM file.'),
            tumor_bam: cwl.File(secondary_files='.bai',
                                doc='Tumor sample BAM or CRAM file.',
                                required=True),
            reference_fasta: cwl.File(secondary_files='.fai',
                                      doc='samtools-indexed reference fasta file [required]'),
            indel_candidates: cwl.File(
                doc='Specify a VCF of candidate indel alleles. These alleles are always '
                    'evaluated but only reported in the output when they are inferred to '
                    'exist in the sample. The VCF must be tabix indexed. All indel alleles'
                    ' must be left-shifted/normalized, any unnormalized alleles will be '
                    'ignored. This option may be specified more than once, multiple input '
                    'VCFs will be merged.',
                default='None') = None,
            forced_gt: cwl.File(doc="Specify a VCF of candidate alleles. "
                                    "These alleles are always evaluated and "
                                    "reported even if they are unlikely to exist in the "
                                    "sample. The VCF must be tabix indexed. All indel "
                                    "alleles must be left-shifted/normalized, any unnormalized "
                                    "allele will trigger a runtime error. This option may "
                                    "be specified more than once, multiple input VCFs will "
                                    "be merged. Note that for any SNVs provided in the VCF, "
                                    "the SNV site will be reported (and for gVCF, excluded "
                                    "from block compression), but the specific SNV "
                                    "alleles are ignored.",
                                default='None') = None,
            exome: cwl.Bool(doc="Set options for exome or other targeted input: note in "
                                "particular that this flag turns off high-depth filters") = False,
            call_regions: cwl.File(doc="Optionally provide a bgzip-compressed/tabix-indexed BED "
                                       "file containing the set of regions to call. No VCF "
                                       "output will be provided outside of these regions. "
                                       "The full genome will still be used to estimate statistics "
                                       "from the input (such as expected depth per chromosome). "
                                       "Only one BED file may be specified.",
                                   default='Call the entire genome') = None,
            scan_size_mb: cwl.Int(doc="Maximum sequence region size (in megabases) scanned by "
                                      "each task during genome variant calling. (default: 12)",
                                  default=12) = 12,
            region: cwl.String(doc="Limit the analysis to one or more genome region(s) for "
                                   "debugging purposes. If this argument is provided multiple"
                                   " times the union of all specified regions will be analyzed. "
                                   "All regions must be non-overlapping to get a meaningful "
                                   "result. Examples: '--region chr20' (whole chromosome), "
                                   "'--region chr2:100-2000 --region chr3:2500-3000' "
                                   "(two regions)'. If this option is specified (one or more times) "
                                   "together with the --callRegions BED file, then all "
                                   "region arguments will be intersected with the "
                                   "callRegions BED track.",
                               default='None') = None
            ):
    """

    :param normal_bam:
    :param tumor_bam:
    :param reference_fasta:
    :param indel_candidates:
    :param forced_gt:
    :param exome:
    :param call_regions:
    :param scan_size_mb:
    :param region:
    :return:
    """
    strelka_config_path = '/opt/bin/configureStrelkaSomaticWorkflow.py'
    strelka_cmd = [strelka_config_path]
    strelka_cmd += ['--normalBam', normal_bam['path']]
    strelka_cmd += ['--tumorBam', tumor_bam['path']]
    strelka_cmd += ['--referenceFasta', reference_fasta['path']]
    strelka_cmd += ['--runDir', '.']

    if indel_candidates:
        strelka_cmd += ['--indelCandidates', indel_candidates['path']]

    if forced_gt:
        strelka_cmd += ['--forcedGT', forced_gt['path']]

    if exome:
        strelka_cmd += ['--exome']

    if call_regions:
        strelka_cmd += ['--callRegions', call_regions['path']]

    strelka_cmd += ['--scanSizeMb', str(scan_size_mb)]
    if region:
        strelka_cmd += ['--region', region]
    check_output(strelka_cmd)
    check_call(['python', 'runWorkflow.py', '-m', 'local', '-j', '8'])


strelka_app = strelka()
strelka_app.doc = TOOL_DOC

if __name__ == '__main__':
    TOOL = strelka()
    TOOL.doc = TOOL_DOC
    TOOL.dump('test.cwl')
