from synth import Synth

if __name__ == "__main__":
    t_att = 0.1
    t_dec = 0.1
    sus_lvl = 0.7
    t_rel = 0.1
    curve = "expo"
    bs = 4096
    sr = 48000
    k = 6
    tb_size = 4096
    type = "sine"
    syn = Synth(
        t_att=t_att,
        t_dec=t_dec,
        sus_lvl=sus_lvl,
        t_rel=t_rel,
        curve=curve,
        bs=bs,
        sr=sr,
        type=type,
        k=k,
        tb_size=tb_size,
    )
    syn.switch_on()
