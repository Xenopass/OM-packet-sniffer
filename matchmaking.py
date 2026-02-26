# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 13:17:22 2025

@author: mathi
"""
import time
import numpy as np
import pandas as pd
import os

def matchmaking_from_DF(name_FirstSect, name_SecondSect):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path for output.csv in that folder
    path_sm = os.path.join(script_dir, "players"+name_FirstSect+".csv")
    path_op = os.path.join(script_dir, "players"+name_SecondSect+".csv")
    # Example data
    df1 = pd.read_csv(path_sm)
    df2 = pd.read_csv(path_op)
    df1 = df1.drop_duplicates()
    df2 = df2.drop_duplicates()
    # Sort both sects
    df1 = df1.sort_values("Power").reset_index(drop=True)
    df2 = df2.sort_values("Power").reset_index(drop=True)

    def format_large_numbers(x):

        try:
            x = float(x)
        except (ValueError, TypeError):
            return x  # return original if not numeric

        if x >= 1e12:
            return f"{x / 1e12:.2f}T"
        elif x >= 1e9:
            return f"{x / 1e9:.2f}B"
        elif x>= 1e6:
            return f"{x/1e6:.2f}M"
        else:
            return f"{x:.0f}"



    def condition_dualpath(x):
        return ((2e11 <= x <= 2.9e11) or (5e10 <= x <= 8e10) or (8e11 <= x <= 1e12))

    def matchmaking_balanced(df1, df2, max_per_member=3, max_per_opponent=3):
        # Sort sect members by descending power
        df1_sorted = df1.sort_values("Power", ascending=False).reset_index(drop=True)
        df2_sorted = df2.sort_values("Power", ascending=False).reset_index(drop=True)

        matches = {sm["Pseudo"]: [] for _, sm in df1_sorted.iterrows()}
        opp_count = {o: 0 for o in df2_sorted["Pseudo"]}

        # --- First pass: greedy strongest-to-weakest
        for _, sm in df1_sorted.iterrows():
            s_name, s_power = sm["Pseudo"], sm["Power"]

            available = df2_sorted[df2_sorted["Pseudo"].map(lambda x: opp_count[x] < max_per_opponent)].copy()
            available["vp"] = available["Power"].apply(lambda p: p*1.8 if condition_dualpath(p) else p)

            eligible = available[available["vp"] < s_power].sort_values("vp", ascending=False)

            for _, opp in eligible.head(max_per_member).iterrows():
                o_name, o_power = opp["Pseudo"], opp["Power"]
                matches[s_name].append((o_name, o_power))
                opp_count[o_name] += 1
                if len(matches[s_name]) >= max_per_member:
                    break

        # --- Redistribution: balance all sect members
        max_iterations = len(df1_sorted) * max_per_member * 2
        iterations = 0

        while iterations < max_iterations:
            iterations += 1
            changed = False

            # Sort sect members by fewest matches first
            needy_list = sorted(matches.keys(), key=lambda s: len(matches[s]))
            # Sort donors by most matches first
            donors = sorted(matches.keys(), key=lambda s: len(matches[s]), reverse=True)

            for needy in needy_list:
                if len(matches[needy]) >= max_per_member:
                    continue  # already full

                s_power = df1_sorted.loc[df1_sorted["Pseudo"] == needy, "Power"].iloc[0]

                for donor in donors:
                    if donor == needy:
                        continue
                    if len(matches[donor]) <= 1:
                        continue  # donor must keep at least 1

                    for opp in list(matches[donor]):
                        o_name, o_power = opp
                        # print(opp,"\n")
                        # print(matches[needy],"\n\n")
                        if opp in matches[needy]:
                            continue

                        vp = o_power*1.8 if condition_dualpath(o_power) else o_power

                        if vp < s_power and opp_count[o_name] <= max_per_opponent:
                            # Transfer opponent
                            matches[donor].remove(opp)
                            matches[needy].append(opp)
                            changed = True
                            break

                    if changed or len(matches[needy]) >= max_per_member:
                        break

                if changed:
                    break  # re-sort needy/donors next iteration

            if not changed:
                break  # stop redistribution if no transfers possible

        # --- Convert to DataFrame
        rows = []
        for sm, opps in matches.items():
            for o_name, o_power in opps:
                rows.append((sm, o_name, o_power))

        match_df = pd.DataFrame(rows, columns=["sect_member", "opponent", "opp_power"])
        return match_df

    match_df = matchmaking_balanced(df1, df2)

    match_df["opp_idx"] = match_df.groupby("sect_member").cumcount() + 1

    # Pivot wider: opponent and power side by side
    wide_df = match_df.pivot(index=["sect_member"],
                       columns="opp_idx",
                       values=["opponent", "opp_power"])

    # Flatten MultiIndex columns
    wide_df.columns = [f"{col[0]}_{col[1]}" for col in wide_df.columns]


    wide_df = wide_df.merge(
        df1[["Pseudo", "Power"]],
        left_on="sect_member",
        right_on="Pseudo",
        how="left"
    ).rename(columns={"Power": "SectMemberPower"}).rename(columns={"Pseudo" : "sect_member"})

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    # print(wide_df)

    wide_df = wide_df.reindex(columns=[
        "sect_member", "SectMemberPower",
        "opponent_1", "opp_power_1",
        "opponent_2", "opp_power_2",
        "opponent_3", "opp_power_3"
    ])

    # print(wide_df)
    wide_df["SectMemberPower"]=wide_df["SectMemberPower"].apply(format_large_numbers)
    wide_df["opp_power_1"]=wide_df["opp_power_1"].apply(format_large_numbers)
    wide_df["opp_power_2"]=wide_df["opp_power_2"].apply(format_large_numbers)
    wide_df["opp_power_3"]=wide_df["opp_power_3"].apply(format_large_numbers)
    wide_df.fillna('',inplace=True)
    wide_df.replace("nan", '', regex=True,inplace=True)
    print(wide_df)
    path_match = os.path.join(script_dir, "matchmaking_week_"+str(time.strftime("%W",time.localtime()))+".xlsx")
    wide_df.to_excel(path_match, index=False)
    return(wide_df)

if __name__ == "__main__":
    match_df = matchmaking_from_DF()