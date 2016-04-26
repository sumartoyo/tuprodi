import subprocess

def main():
    if not call('HParse gram wdnet'): return False
    if not call('julia bin/prompts2wlist.jl prompts wlist'): return False
    if not call('HDMan -A -D -T 1 -m -w wlist -n monophones1 -i -l dlog dict lexicon'): return False
    if not call('cat monophones1 |  while read line; do if [ $line != \'sp\' ]; then echo -n "$line\n"; fi; done > monophones0'): return False
    if not call('julia bin/prompts2mlf.jl prompts words.mlf'): return False
    if not call('HLEd -A -D -T 1 -l \'*\' -d dict -i phones0.mlf mkphones0.led words.mlf'): return False
    if not call('HLEd -A -D -T 1 -l \'*\' -d dict -i phones1.mlf mkphones1.led words.mlf'): return False
    if not call('HCopy -A -D -T 1 -C wav_config -S codetrain.scp'): return False
    if not call('HCompV -A -D -T 1 -C config -f 0.01 -m -S train.scp -M hmm0 proto'): return False
    create_hmm0()
    if not call('HERest -A -D -T 1 -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm0/macros -H hmm0/hmmdefs -M hmm1 monophones0'): return False
    if not call('HERest -A -D -T 1 -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm1/macros -H hmm1/hmmdefs -M hmm2 monophones0'): return False
    if not call('HERest -A -D -T 1 -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm2/macros -H hmm2/hmmdefs -M hmm3 monophones0'): return False
    if not call('cp hmm3/* hmm4'): return False
    create_hmm4()
    if not call('HHEd -A -D -T 1 -H hmm4/macros -H hmm4/hmmdefs -M hmm5 sil.hed monophones1'): return False
    if not call('HERest -A -D -T 1 -C config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm5/macros -H hmm5/hmmdefs -M hmm6 monophones1'): return False
    if not call('HERest -A -D -T 1 -C config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm6/macros -H hmm6/hmmdefs -M hmm7 monophones1'): return False
    if not call('HVite -A -D -T 1 -l \'*\' -o SWT -b SENT-END -C config -H hmm7/macros -H hmm7/hmmdefs -i aligned.mlf -m -t 250.0 150.0 1000.0 -y lab -a -I words.mlf -S train.scp dict monophones1 > HVite_log'): return False
    if not call('HERest -A -D -T 1 -C config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm7/macros -H hmm7/hmmdefs -M hmm8 monophones1'): return False
    if not call('HERest -A -D -T 1 -C config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm8/macros -H hmm8/hmmdefs -M hmm9 monophones1'): return False
    if not call('HLEd -A -D -T 1 -n triphones1 -l \'*\' -i wintri.mlf mktri.led aligned.mlf'): return False
    if not call('julia bin/mktrihed.jl monophones1 triphones1 mktri.hed'): return False
    if not call('HHEd -A -D -T 1 -H hmm9/macros -H hmm9/hmmdefs -M hmm10 mktri.hed monophones1'): return False
    if not call('HERest  -A -D -T 1 -C config -I wintri.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm10/macros -H hmm10/hmmdefs -M hmm11 triphones1'): return False
    if not call('HERest  -A -D -T 1 -C config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm11/macros -H hmm11/hmmdefs -M hmm12 triphones1'): return False
    if not call('HDMan -A -D -T 1 -b sp -n fulllist0 -g maketriphones.ded -l flog dict-tri lexicon'): return False
    if not call('julia bin/fixfulllist.jl fulllist0 monophones0 fulllist'): return False
    if not call('cat tree1.hed > tree.hed'): return False
    if not call('julia bin/mkclscript.jl monophones0 tree.hed'): return False
    if not call('HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1'): return False
    if not call('HERest -A -D -T 1 -T 1 -C config -I wintri.mlf  -t 250.0 150.0 3000.0 -S train.scp -H hmm13/macros -H hmm13/hmmdefs -M hmm14 tiedlist'): return False
    if not call('HERest -A -D -T 1 -T 1 -C config -I wintri.mlf  -t 250.0 150.0 3000.0 -S train.scp -H hmm14/macros -H hmm14/hmmdefs -M hmm15 tiedlist'): return False
    print '[SELESAI]'

def call(cmd):
    status = subprocess.call(cmd, shell=True)
    if status == 0:
        return True
    else:
        print '[ERROR] '+cmd
        return False

def create_hmm0():
    phones = [line.rstrip('\n') for line in open('monophones0')]
    proto = [line.rstrip('\n') for line in open('hmm0/proto')]

    hmm = proto[4:]
    hmmdefs = []
    for i, phone in enumerate(phones):
        hmmdefs.append('~h "'+phone+'"')
        hmmdefs.extend(hmm)
    with open('hmm0/hmmdefs', 'w') as f:
        f.write('\n'.join(hmmdefs)+'\n')

    vFloors = [line.rstrip('\n') for line in open('hmm0/vFloors')]
    macros = []
    macros.extend(proto[:3])
    macros.extend(vFloors)
    with open('hmm0/macros', 'w') as f:
        f.write('\n'.join(macros)+'\n')

def create_hmm4():
    hmmdefs = [line.rstrip('\n') for line in open('hmm4/hmmdefs')]
    for i, line in enumerate(hmmdefs):
        if line == '~h "sil"':
            sil = hmmdefs[i+10:i+15]
            sp = ['~h "sp"', '<BEGINHMM>', '<NUMSTATES> 3', '<STATE> 2']
            sp.extend(sil)
            sp.extend(['<TRANSP> 3', ' 0.0 1.0 0.0', ' 0.0 0.9 0.1', ' 0.0 0.0 0.0', '<ENDHMM>'])
            hmmdefs.extend(sp)
            with open('hmm4/hmmdefs', 'w') as f:
                f.write('\n'.join(hmmdefs)+'\n')
            break

if __name__ == '__main__':
    '''sediakan:
    gram
    bin/
    prompts *****speech
    global.ded
    lexicon
    mkphones0.led
    mkphones1.led
    codetrain.scp *****speech
    wav_config
    wav/ *****speech
    proto
    config
    train.scp *****speech
    hmm0-15/
    sil.hed
    mktri.led
    maketriphones.ded
    tree1.hed
    '''
    main()
