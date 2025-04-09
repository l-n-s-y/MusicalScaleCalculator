# given a tonic note, list the scales of every mode it is a part of

import sys,re


modes = {
    "ionian": "w-w-h-w-w-w-h",
    "dorian": "w-h-w-w-w-h-w",
    "phrygian": "h-w-w-w-h-w-w",
    "lydian": "w-w-w-h-w-w-h",
    "mixolydian": "w-w-h-w-w-h-w",
    "aeolian": "w-h-w-w-h-w-w",
    "locrian": "h-w-w-h-w-w-w",
}

minor_scales = {
    "natural": "w-h-w-w-h-w-w",
    "harmonic": "w-h-w-w-h-+-h", # '+' means tone-and-a-half
    "melodic_asc": "w-h-w-w-w-w-h", # ascending
    "melodic_des": "w-h-w-w-h-w-w", # descending
}


tests = {
    "ionian": ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#', 'A'],
    "dorian": ['A', 'B', 'C', 'D', 'E', 'F#', 'G', 'A'],
    "phrygian": ['A', 'Bb', 'C', 'D', 'E', 'F', 'G', 'A'],
    "lydian": ['A', 'B', 'C#', 'D#', 'E', 'F#', 'G#', 'A'],
    "mixolydian": ['A', 'B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
    "aeolian": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A'],
    "locrian": ['A', 'Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],

    "natural":['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    "harmonic":['A', 'B', 'C', 'D', 'E', 'F', 'G#'],
    "melodic_asc":['A', 'B', 'C', 'D', 'E', 'F#', 'G#'],
    "melodic_des":['A', 'B', 'C', 'D', 'E', 'F', 'G'],
}


def dbg_print(*args):
    if "--dbgout" in sys.argv:
        print(args)


chromatic_staff = [
    #"C",["C#","Db"],"D",["D#","Eb"],"E",["E#","Fb"],"F",["F#","Gb"],"G",["G#","Ab"],"A",["A#","Bb"],"B",["B#","Cb"]
    "C","D","E","F","G","A","B"
    ]

def mod_increment(mod,inc):
    dbg_print(mod,inc)
    new_mod = ""
    if inc == 1: # whole tone
        if "b" in mod:
            new_mod = mod[:-1] # delete flat (and convenientally raise to natural if only 1)
            dbg_print(new_mod,mod)

        elif "#" in mod or "x" in mod:
            new_mod = mod
            if mod[-1] == "#":
                new_mod = mod[:-1]+"x"
            else:
                new_mod += "#"
        else:
            dbg_print("empty positive")
            new_mod = "#"

    elif inc == 2: # tone-and-a-half
        if "b" in mod:
            new_mod = mod[:-2]
            if len(new_mod) == 0:
                new_mod = "#"
            
        elif "#" in mod or "x" in mod:
            new_mod = "x"+mod

        else:
            new_mod = "x"

    elif inc < 0: # semi-tone
        if "b" in mod:
            new_mod = mod+"b"

        elif "#" in mod or "x" in mod:
            if mod[-1] == "#":
                new_mod = mod[:-1]
            else:
                new_mod = mod[:-1]+"#"
                #new_mod[-1] = "#"
        else:
            dbg_print("empty negative")
            new_mod = "b"
    else:
        return mod

    return new_mod

def calc_mod(n,mod,ref,inc):
    new_mod = ""


    mod_n = 0
    if len(mod):
        mod_n = 1 if ("#" in mod) else 2

    """if mod_n == 0: # natural
        
    elif mod_n == 1: # sharp
        pass
    elif mod_n == 2: # flat
        pass"""

    mod_count = 0
    dbg_print("X ",ref, inc)
    if "B" in ref or "E" in ref: # weirdos
        if inc == "h": # B -> C, B# -> C#
            #return mod
            mod_count = 0
        elif inc == "+":
            mod_count = 2
        else:
            dbg_print("whole")
            mod_count = 1
    else:
        if inc == "h":
            mod_count = -1
        elif inc == "+": # coincidentally the same as B/E whole
            mod_count = 1
        else:
            #return mod 
            mod_count = 0
        
    new_mod = mod_increment(mod,mod_count)

    return new_mod

def generate_scale(tonic, mod, mode): # mod is # or b ig, idk
    
    scale = []

    scale.append(tonic)

    # find in chromatic_staff
    chrom_idx = 0
    for i in range(len(chromatic_staff)):
        n = chromatic_staff[i]
        if n == tonic.replace(mod,""):
            chrom_idx = i

    current = tonic
    curr_mod = mod

    trans_dict = modes if (mode in modes.keys()) else minor_scales
    for c in trans_dict[mode].split("-"):
    #for c in modes[mode].split("-"):
        chrom_idx+=1
        note = chromatic_staff[chrom_idx%len(chromatic_staff)]
        
        new_mod = calc_mod(note,curr_mod,current,c)

        current = note+(new_mod if new_mod else "")
        curr_mod = new_mod

        scale.append(current)

    """if type(scale[0]) == list:
        if is_sharp_key:
            scale = [scale[0][0]]
        else:
            scale = [scale[0][1]]"""

    """curr_idx = 0
    t = tonic
    if sharp_or_flat != 0: 
        t = t[0]
    for i in range(len(chromatic_staff)):
        if c == t: curr_idx = i

    curr_note = chromatic_staff[curr_idx]
    next_note = ""
    for c in pattern.split("-"):
        if c == "w":
            if curr_note == "B" or curr_note == "E":
                next_note = chromatic_staff[curr_idx+1] + "#"


        elif c == "h":

        degree = chromatic_staff[curr_idx%len(chromatic_staff)]
        if type(degree) == list:
            scale.append(degree[0] if is_sharp_key else degree[1])
        else:
            scale.append(degree)"""

    return scale

def is_valid_tonic(t):
    regex = "[A-G]{1}[b,#,x]*"
    matcha = re.search(regex,t)
    if not matcha:
        return False

    if matcha.start() == 0 and matcha.end() == len(t):
        return True

    return False   


def main():
    if len(sys.argv) != 2 and "--debug" not in sys.argv:
        print(f"USAGE: python3 {sys.argv[0]} TONIC")
        exit()

    tonic = sys.argv[1]
    if not is_valid_tonic(tonic):
        print("ERROR: malformed input")
        exit()

    mod = tonic[1:]

    for m in modes:
        scale = generate_scale(tonic,mod,m)
        if "--debug" not in sys.argv:
            print(m," : ",scale)
            continue

        if scale == tests[m]:
            print(m," : ",scale," [O] Passed.")
        else:
            print(m,scale,f"[ CORRECT: {tests[m]} ]"," [X] Failed.")


    for s in minor_scales:
        scale = generate_scale(tonic,mod,s)

        if "--debug" not in sys.argv:
            print(s," : ",scale)
            continue

        if scale == tests[s]:
            print(s," : ",scale," [O] Passed.")
        else:
            print(s,scale,f"[ CORRECT: {tests[m]} ]"," [X] Failed.")


if __name__ == "__main__":
    main()
