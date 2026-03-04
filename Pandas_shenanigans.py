import time

import pandas as pd

def sect_duels_data(duel_dict,members_info_list):

    members_info = pd.DataFrame([[x[0], x[1], x[2]] for x in members_info_list],
                                columns=["rid", "pseudo", "BR"])

    def decode_dict(d):
        return {
            k:
                v
            for k, v in d.items()
        }
    if 'appearance' in duel_dict.keys():
        a='appearance'
    else:
        a='enemy_appearances'
    enemy_data = [{
        "op_rid": k,
        "op_BR": v["combat_capacity"],
        "op_pseudo": v["name"]
    } for k, v in duel_dict[a].items()]
    names_uuid = pd.DataFrame(enemy_data)
    # print(names_uuid)

    duel_info = (pd.DataFrame(decode_dict(d) for d in duel_dict['battles'])
                 .merge(names_uuid, on="op_rid",how='left')
                 .merge(members_info,on="rid",how='left'))
    duel_info.drop(columns=["playback_id","time","duel_id","ori_battle_id","gang_rid"], inplace=True)
    duel_info.replace({"result": {True: 1, False: 0, None: 0},
                       "enemy_record": {True: 1, None: 0}},
                      inplace=True)

    duel_info.to_excel(excel_writer="duel_info"+str(time.strftime("%W",time.localtime()))+".xlsx", index=False)
    return duel_info





if __name__ == "__main__":
    duel_info = sect_duels_data(duel_dict, list_members)
    duel_info.to_excel(excel_writer="pandas_shenanigans_test.xlsx", index=False)
    print(duel_info)