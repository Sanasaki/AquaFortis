from Classes.SpeciationLine import Speciation


def main(**argv):
    someSpeciation = Speciation.fromStr("4 {HNO3: 16, H2O: 76, H3NO4: 4}")
    print(someSpeciation)

if __name__ == "__main__":
    main()