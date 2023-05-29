def decode_subj_file(file_name,directory):
    f = open(directory+file_name, "r", encoding="utf-8")
    subjects = []
    groups = []
    for line in f:
        if line[0] == '"':
            subjects.append(line.strip().strip('"'))
            groups.append([])
        elif line[0].isdigit():
            a = line.replace('-',' ').split()
            b = []
            for i in range(0,len(a),3):
                b.append([
                    int(a[i])-1,
                    int(a[i+1].partition(':')[0]),
                    int(a[i+2].partition(':')[0])
                    ])
            groups[-1].append(b)
    return subjects, groups
