import os
def get_filepath_list(root_path):
    """
    Get complete filepaths leading to all relevant training data documents in a list
    :param root_path: str
    """
    file_list = []
    for root, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_list.append(os.path.join(root, filename))
    return(file_list)

def create_data_inventory(file_list):
    """
    creates a data inventory according to filepath and filename structure of data
    """
    data_inventory = []
    for x in file_list:
        d = dict()
        spl = x.split('/')
        if spl[2] == 'train_2':
            round = '2'
        if spl[2] == 'train_3':
            round = '3'
        if spl[2] == 'train_4':
            round = '4'
        if spl[3] == 'special_topic_ESTA':
            round = '3_ESTA'
        year = int((spl[-1].split(' -')[1].strip()))
        if int((spl[-1].split(' -')[1].strip())) <1650:
            centuryhalf = '1600-1650'
        if int((spl[-1].split(' -')[1].strip())) in range (1650, 1700):
            centuryhalf = '1650-1700'
        if int((spl[-1].split(' -')[1].strip())) in range(1700, 1750):
            centuryhalf = '1700-1750'
        if int((spl[-1].split(' -')[1].strip())) in range(1750, 1800):
            centuryhalf = '1750-1800'
        if round == '2':
            inv_nr = ((spl[-1].split('_'))[2]).split(' - ')[0]
            scan_nrs = ((spl[-1].split('_'))[3]).split(' - ')[0]
        if round == '3' or round == '3_ESTA':
            inv_nr = ((spl[-1].split('_'))[4]).split(' - ')[0]
            scan_nrs = ((spl[-1].split('_'))[5]).split(' - ')[0]
        if round == '4':
            inv_nr = ((spl[-1].split('_'))[2]).split(' - ')[0]
            scan_nrs = ((spl[-1].split('_'))[3]).split(' - ')[0]
        d['original_filename'] = spl[-1]
        d['round'] = round
        d['inv_nr'] = inv_nr
        d['scan_nrs'] = scan_nrs
        d['year'] = year
        d['century_half'] = centuryhalf
        data_inventory.append(d)
    return(data_inventory)



if __name__ == "__main__":
    root_path = "data/json_per_doc/"
    filepaths=get_filepath_list(root_path)
    data_inv=create_data_inventory(filepaths)
