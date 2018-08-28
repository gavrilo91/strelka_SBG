"""
Documentation
"""
TOOL_DOC = "Strelka calls germline and somatic small variants from mapped " \
           "sequencing reads. It is optimized for rapid clinical analysis of " \
           "germline variation in small cohorts and somatic variation in " \
           "tumor/normal sample pairs. Strelka's germline caller employs a haplotype " \
           "model to improve call quality and provide short-range read-backed phasing " \
           "in addition to a probabilistic variant calling model using indel error " \
           "rates adaptively estimated from each input sample's sequencing data. " \
           "Both germline and somatic callers include a final empirical variant " \
           "rescoring step using a random forest model to reflect numerous features " \
           "indicative of call reliability which may not be represented in the " \
           "core variant calling probability model."
