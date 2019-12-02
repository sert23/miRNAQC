from miRQC.settings import SPECIES_FILE



def load_species(ifile):
    with open(ifile) as i:
        species_list=[]
        for line in i:
            a = line.replace('\n', '').split(',')

            if a[7] == 'true':
                a[7] = True
            else:
                a[7] = False

            if a[8] == 'true':
                a[8] = True
            else:
                a[8] = False

            to_keep = [a[0], ]
            species_list.append(a)

    return species_list


tt_list = load_species(SPECIES_FILE)
print(tt_list)

