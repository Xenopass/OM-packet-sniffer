#tools for the overmortal app

# ================== FLEXIBLE SHAPE DEFINITION ==================
import pandas as pd
from time import time

NoneType = type(None)

EXPECTED_DUEL_SHAPE = {
    'opponent_info': dict,
    'members_data': dict,
    'appearance': dict,
    'left_alive': int,
    'left_duel_chance': int,
    'enemy_left_alive': int,
    'enemy_left_duel_chance': int,
    'me_info': dict,
    'opponent_score': int,
    'me_score': int,
    'user_duel_chance': int,
    'dueled_opponents': list,
    'extra_enemy_factor': float,
}

EXPECTED_SECT_SHAPE = {
    'rid': (bytes, str),
    'hp': int,
    'hp_max': int,
    'exp': int,
    'name': (bytes, str),
    'icon': int,
    'info': (bytes, str),
    'owner': (bytes, str),
    'gang_hp': int,
    'gang_hp_max': int,
    'level': int,
    'gang_pos': dict,
    'apply_level': int,
    'announcement': (bytes, str),
    'apply_capacity_new': int,
    'pass_red_env': int,
    'range': float,
    'range_max': float,
    'expand_speed': int,
    'name_editor': (bytes, str),
    'announce_editor': (bytes, str),
    'rule_editor': (bytes, str),
    'set_recruit_info_user': (bytes, str),
    'recruit_info': (bytes, str),
    'members': dict,
    'appliers': (dict, NoneType),
    'under_attack': bool,
    'inc_gang_exp': int,
    'dec_gang_hp': int,
    'dec_gang_hp_max': int,
    'gang_hp_recover_speed': int,
    'next_expand_time': int,
    'combat_capacity': int,
    'server_name': (bytes, str),
    'server_id': (bytes, str),
    'world': int,
    'welcome_word': int,
    'newest_photo': int,
    'rest_photo_count': int,
    'photo_share_cd': dict,
    'gang_star': int,
    'from_invited': (NoneType,),  # optional
}

def find_sects(list_objects):
    
    NoneType = type(None)


    EXPECTED_SECT_SHAPE = {
        'rid': (bytes, str),
        'hp': int,
        'hp_max': int,
        'exp': int,
        'name': (bytes, str),
        'icon': int,
        'info': (bytes, str),
        'owner': (bytes, str),
        'gang_hp': int,
        'gang_hp_max': int,
        'level': int,
        'gang_pos': dict,
        'apply_level': int,
        'announcement': (bytes, str),
        'apply_capacity_new': int,
        'pass_red_env': int,
        'range': float,
        'range_max': float,
        'expand_speed': int,
        'name_editor': (bytes, str),
        'announce_editor': (bytes, str),
        'rule_editor': (bytes, str),
        'set_recruit_info_user': (bytes, str),
        'recruit_info': (bytes, str),
        'members': dict,
        'appliers': (dict, NoneType),
        'under_attack': bool,
        'inc_gang_exp': int,
        'dec_gang_hp': int,
        'dec_gang_hp_max': int,
        'gang_hp_recover_speed': int,
        'next_expand_time': int,
        'combat_capacity': int,
        'server_name': (bytes, str),
        'server_id': (bytes, str),
        'world': int,
        'welcome_word': int,
        'newest_photo': int,
        'rest_photo_count': int,
        'photo_share_cd': dict,
        'gang_star': int,
        'from_invited': (NoneType,),  # optional
    }
    
    matches = find_all_matching_dicts(list_objects, EXPECTED_SECT_SHAPE)
    unique_matches = deduplicate_by_name(matches)

    print(f"Found {len(matches)} matching SECT dict(s)")
    print(f"After deduplication: {len(unique_matches)} unique SECT dict(s)")
    return unique_matches

def find_duels(list_objects):
    
    EXPECTED_DUEL_SHAPE = {
        'opponent_info': dict,
        'members_data': dict,
        'appearance': dict,
        'left_alive': int,
        'left_duel_chance': int,
        'enemy_left_alive': int,
        'enemy_left_duel_chance': int,
        'me_info': dict,
        'opponent_score': int,
        'me_score': int,
        'user_duel_chance': int,
        'dueled_opponents': list,
        'extra_enemy_factor': float,
    }
    
    matches = find_all_matching_dicts(list_objects, EXPECTED_DUEL_SHAPE)
    unique_matches = deduplicate_by_name(matches)

    print(f"Found {len(matches)} matching DUEL dict(s)")
    print(f"After deduplication: {len(unique_matches)} unique DUEL dict(s)")
    return unique_matches
# ================== SHAPE MATCHING ==================

def matches_shape(d, shape):
    if not isinstance(d, dict):
        return False

    for key, expected_type in shape.items():
        if key not in d:
            if isinstance(expected_type, tuple) and NoneType in expected_type:
                continue
            return False

        value = d[key]

        if isinstance(expected_type, tuple):
            if not isinstance(value, expected_type):
                return False
        else:
            if not isinstance(value, expected_type):
                return False

    return True


# ================== RECURSIVE LIST SEARCH ==================

def find_all_matching_dicts(obj, shape):
    results = []

    if isinstance(obj, list):

        for item in obj:
            if isinstance(item, dict):
                if matches_shape(item, shape):
                    results.append(item)

            elif isinstance(item, list):
                results.extend(find_all_matching_dicts(item, shape))

    return results


# ================== DEDUPLICATION BY 'name' ==================

def deduplicate_by_name(dicts):
    seen = set()
    unique = []

    for d in dicts:
        name = d.get('name')
        if name not in seen:
            seen.add(name)
            unique.append(d)

    return unique

def save_list_csv( data:list, name:str):
    
    df = pd.DataFrame(data,columns=["BR","Pseudo", "Power"])
    # print(df)
    filename = "players" + name + ".csv"
    df.to_csv(
    filename,
    index=False,
    encoding="utf-8-sig"
    )
 
def decode_bytes(x):
    return x.decode("utf-8", errors="replace") if isinstance(x, bytes) else str(x)

def print_list(data):
    for i in data:
        print(f' type : {type(i).__name__} \t content')


def find_and_fuse_duel_dicts(obj):
    seen = set()
    fused = {}
    
    def find_all_battles_dicts(obj):
        results = []

        if isinstance(obj, list):
            i=0
            for item in obj:

                if isinstance(item, list):
                    results.extend(find_all_battles_dicts(item))
                    
                elif isinstance(item, str):
                    if (item == "gang_duel_op"):
                        # print("__________found sect_duel related OBJ__________")
                        # print(obj[i+1])
                        if isinstance(obj[i+1],dict):
                            results.append(obj[i+1])
                i+=1
        return results
    
    def signature(d):
        return frozenset((k, len(v)) for k, v in d.items() if hasattr(v, "__len__"))
    
    dicts = find_all_battles_dicts(obj)
    
    for d in dicts:
        sig = signature(d)
        if sig in seen:
            continue
        seen.add(sig)
        for k, v in d.items():
            fused.setdefault(k, v)

    return fused


def get_sect_members(sect):
    members_list = sect.get('members')
    current_time= time()
    def is_active(member : dict, time_now=current_time):
        last_time_online = member.get('state')
        if last_time_online == "online":
            return True
        else:
            last_time_online = (time_now - last_time_online)/3600

            if last_time_online < 72:
                return True
        # print(member.get('name'), " : ", last_time_online)
        return False

    member_UID_name_BR = [[UID, members_list.get(UID).get('name'), members_list.get(UID).get('max_combat_capacity')] for UID in members_list.keys() if is_active(members_list.get(UID))]

    return member_UID_name_BR

def normalize_utf8(obj):
    """
    Recursively walk dicts/lists/tuples and:
    - decode bytes to str if valid UTF-8
    - otherwise keep bytes untouched
    """
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return obj

    elif isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = normalize_utf8(k)
            new_val = normalize_utf8(v)
            new_dict[new_key] = new_val
        return new_dict

    elif isinstance(obj, list):
        return [normalize_utf8(v) for v in obj]

    elif isinstance(obj, tuple):
        return tuple(normalize_utf8(v) for v in obj)

    else:
        return obj
