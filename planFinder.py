def define_all_plans(p, groups, start_hour=8, omitted_subjects=[]):
    Rows = ['8','9','10','11','12','13','14','15','16','17','18','19','20']
    group_clicker = [0 for i in range(len(p))]
    Ready_plans = []
    while True:
        set = []
        #creating a set
        for i in range(len(groups)):
            if p[i] not in omitted_subjects:
                set.append([p[i], groups[i][group_clicker[i]]])
        #checking the set
        for i in range(len(groups)):
            if p[i] not in omitted_subjects:
                for k in range(len(groups[i][group_clicker[i]])):
                    if groups[i][group_clicker[i]][k][1] >= start_hour:
                        for ii in range(len(groups)):
                            if(ii != i and p[ii] not in omitted_subjects):
                                for kk in range(len(groups[ii][group_clicker[ii]])):
                                    if groups[ii][group_clicker[ii]][kk][1] >= start_hour:
                                        if(groups[i][group_clicker[i]][k][0] == groups[ii][group_clicker[ii]][kk][0]):    #day of the week
                                            if (groups[i][group_clicker[i]][k][1] <= groups[ii][group_clicker[ii]][kk][1]):
                                                if (groups[i][group_clicker[i]][k][2] > groups[ii][group_clicker[ii]][kk][1]):
                                                    break   #colision
                                    else:
                                        break
                                else:
                                    continue
                                break
                        else:
                            continue
                        break
                    else:
                        break
                else:
                    continue
                break
        else:        
            plan = [['' for j in range(5+1)] for i in range(int(Rows[0]),int(Rows[-1]))]
            for i in range(len(set)):                                            #subject
                for j in range(len(set[i][1])):                                  #class
                    for k in range(set[i][1][j][1]-8,set[i][1][j][2]-8):
                        plan[k][0] = Rows[k]
                        plan[k][set[i][1][j][0]+1] = set[i][0]
            if plan not in Ready_plans:
                Ready_plans.append(plan)
        # changing the set
        group_clicker[0] += 1
        for i in range(len(group_clicker)):
            if group_clicker[i] >= len(groups[i]):
                if i+1>=len(group_clicker):
                    return Ready_plans

                if p[i+1] not in omitted_subjects:
                    group_clicker[i+1] += 1
                else:
                    group_clicker[i+1] = len(groups[i+1])
                group_clicker[i] = 0
