import utils
import copy

# compares two objects removing fields that do not match the sample prototype
# because they are not actually in the prototype
# or because the value type does not match the comparable value type found in the sample prototype
def clean_data(payload, sample, report=None):
    if isinstance(payload, dict) and isinstance(sample, dict):
        cleaned_dict={}
        for key in payload.keys():
            if key not in sample:
                if report != None:
                    report.append("Deleting attribute {} because not in sample prototype".format(key))
            else:
                cleaned=clean_data(payload[key], sample[key], report)
                if cleaned:
                    cleaned_dict[key]=cleaned
                else:
                    if report != None:
                        report.append("Deleting attribute {} because value not clean".format(key))
        return cleaned_dict
    elif isinstance(payload, list) and isinstance(sample, list):
        cleaned_list=[]
        if len(sample):
            for item in payload:
                cleaned=clean_data(item, sample[0], report)
                if cleaned:
                    cleaned_list.append(cleaned)
                else:
                    cleaned_list=[]
                    break
        return cleaned_list
    elif type(payload) is type(sample):
        return payload
    else:
        if report != None:
            report.append("Type of {} does not match expected type of {}".format(type(payload).__name__, type(sample).__name__))
        return None


# TESTS (nose)
def test_no_changes():
    sample_data=utils.read_json_from_file('./sample.json')
    copy_data=copy.deepcopy(sample_data)
    cleaned_data=clean_data(copy_data, sample_data)
    assert cleaned_data == sample_data

def test_extra_key_gets_removed():
    sample_data=utils.read_json_from_file('./sample.json')
    copy_data=copy.deepcopy(sample_data)
    copy_data['xxx']='xxx'
    cleaned_data=clean_data(copy_data, sample_data)
    assert cleaned_data == sample_data

def test_key_value_wrong_type():
    sample_data=utils.read_json_from_file('./sample.json')
    copy_data=copy.deepcopy(sample_data)
    copy_data['id']="123" # change int to string
    cleaned_data=clean_data(copy_data, sample_data)
    assert cleaned_data != sample_data
    assert 'id' not in cleaned_data

def test_list_value_wrong_type():
    sample_data=utils.read_json_from_file('./sample.json')
    copy_data=copy.deepcopy(sample_data)
    copy_data['address_ids']=[1, "30", 100, 50]
    cleaned_data=clean_data(copy_data, sample_data)
    assert cleaned_data != sample_data
    assert 'address_ids' not in cleaned_data
