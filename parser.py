import re


def list_to_str(par_list):
    new_str = ""
    for par in par_list:
        new_str += "{} ".format(par)
    return new_str


def parser(par_dict, par_str):
    par_exp = r'--(.*)=\$(.*)'
    new_par_list = []
    par_list = par_str.split(" ")
    for par in par_list:
        match = re.match(par_exp, par, re.M | re.I)
        if match:
            key = match.group(2)
            try:
                value = par_dict.get(key)
            except Exception as e:
                print(e)
                continue
            par = par.replace("$" + key, value)
        new_par_list.append(par)
    return list_to_str(new_par_list)


def main():
    d = {"algo1234": "/var/input/algo/1234", "data1234": "/var/input/data/1234"}
    s = "--input_dir=$algo1234 --batch_size=512 --data_dir=$data1234"
    print(parser(d, s))


if __name__ == "__main__":
    main()
