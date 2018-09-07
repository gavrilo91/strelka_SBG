## Strelka2 Small Variant Caller Wrapped using `sbg-cwl`

This project demonstrate wrapping style using open-source python library sbg-cwl.


## Table of content
*  [Strelka2](#Strelka2)
*  [Input requirements](#input-requirements)
    *  [Sequencing Data](#sequencing-data)
    *  [Alignment Files](#alignment-files)
    * [VCF Files](#vcf-files)
* [Outputs](#outputs)
    * [Variant prediction](#variant-prediction)
 
## Strelka2

Strelka2 is a fast and accurate small variant caller optimized for analysis of germline variation in small cohorts and somatic variation in tumor/normal sample pairs. The germline caller employs an efficient tiered haplotype model to improve accuracy and provide read-backed phasing, adaptively selecting between assembly and a faster alignment-based haplotyping approach at each variant locus. The germline caller also analyzes input sequencing data using a mixture-model indel error estimation method to improve robustness to indel noise. The somatic calling model improves on the original Strelka method for liquid and late-stage tumor analysis by accounting for possible tumor cell contamination in the normal sample. A final empirical variant re-scoring step using random forest models trained on various call quality features has been added to both callers to further improve precision.

Strelka accepts input read mappings from BAM or CRAM files, and optionally candidate and/or forced-call alleles from VCF. It reports all small variant predictions in VCF 4.1 format. Germline variant reporting uses the gVCF conventions to represent both variant and reference call confidence. For best somatic indel performance, Strelka is designed to be run with the Manta structural variant and indel caller, which provides additional indel candidates up to a given maxiumum indel size (49 by default). By design, Manta and Strelka run together with default settings provide complete coverage over all indel sizes (in additional to SVs and SNVs).


## Input requirements

### Sequencing Data

The input sequencing reads are expected to come from a paired-end sequencing assay.
Any input other than paired-end reads are ignored by default except to double-check
for putative somatic variant evidence in the normal sample during somatic variant analysis.
Read lengths above ~400 bases are not tested.

### Alignment Files

All input sequencing reads should be mapped by an external tool and provided as input in
BAM or CRAM format.

The following limitations apply to the input BAM/CRAM alignment records:

* Alignments cannot contain the "=" character in the SEQ field.
* RG (read group) tags are ignored -- each alignment file must represent one
  sample.
* Alignments with basecall quality values greater than 70 will trigger a runtime error (these
  are not supported on the assumption that the high basecall quality indicates an offset error)

### VCF Files

Input VCFs files are accepted for a number of roles as described below. All input VCF records are checked for
compatibility with the given reference genome, in additional to role-specific checks described below. If any
VCF record's REF field is not compatible with the reference genome a runtime error will be triggered.
"Compatible with the reference genome" means that each VCF record's REF base either matches the corresponding
reference genome base or the VCF record's REF base is 'N' or the reference genome base is any ambiguous IUPAC base code
(all ambiguous base codes are converted to 'N' while importing the reference).

## Outputs

### Variant prediction

Primary variant inferences are provided as a series of VCF 4.1 files.