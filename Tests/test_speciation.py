import TestConfigs

from Packages.Analysis.ComputeSpeciation import computeSpeciation


def test_speciation():
    assert computeSpeciation(TestConfigs.testXyzFile_1) == 0
