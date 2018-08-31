"""
Strelka Test Execution
"""
import logging
from sbg import cwl
from tools.strelka import strelka_app
from tests.config import TEST_PROJECT, PROFILE

logging.basicConfig(level=logging.WARNING)


def test_strelka(
        normal_bam_name: str = 'NA12892_demo20.bam',
        tumor_bam_name: str = 'NA12891_demo20.bam',
        reference_name: str = 'demo20.fa'
):
    """

    :param normal_bam_name:
    :param tumor_bam_name:
    :param reference_name:
    :return:
    """
    session = cwl.Session(profile=PROFILE)
    app = strelka_app
    log = logging.getLogger('Strelka Test Run')
    log.warning(" Strelka 2.9.7 Test Run Started")
    try:
        normal_bam = list(
            session.api.files.query(
                project=TEST_PROJECT,
                names=[normal_bam_name]
            )
        )

        log.warning(" Normal Bam file is here!")
    except IndexError:
        raise Exception('Missing normal_bam file') from None

    try:
        tumor_bam = list(
            session.api.files.query(
                project=TEST_PROJECT,
                names=[tumor_bam_name]
            )
        )

        log.warning(" Tumor Bam file is here!")
    except IndexError:
        raise Exception('Missing tumor_bam file') from None

    try:
        reference = list(
            session.api.files.query(
                project=TEST_PROJECT,
                names=[reference_name]
            )
        )

        log.warning(" Reference file is here!")
    except IndexError:
        raise Exception('Missing reference file') from None

    session.run(
        TEST_PROJECT,
        app,
        dict(
            reference_fasta=reference[0],
            normal_bam=normal_bam[0],
            tumor_bam=tumor_bam[0]
        )
    )

    log.warning(" Demo Task is running on the CGC platform!")


if __name__ == "__main__":
    test_strelka()
