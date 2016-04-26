# train

```
python htker.py
```

# test

```
HCopy -A -D -T 1 -C wav_config_test -S codetest.scp
```

```
HVite -H hmm15/macros -H hmm15/hmmdefs -S test.scp -l '*' -i recout.mlf -w wdnet -p 0.0 -s 5.0 dict tiedlist
```

```
HResults -I testref.mlf tiedlist recout.mlf
```
