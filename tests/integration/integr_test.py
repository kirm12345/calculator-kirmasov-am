import subprocess
import sys
import os
   
def test_sum_int():
    res = subprocess.run(["./build/app.exe"], input="2+2", text=True, capture_output=True)
    assert res.returncode == 0
    assert int(res.stdout) == 4
    
def test_mult_int():
    res = subprocess.run(["./build/app.exe"], input="12*5", text=True, capture_output=True)
    assert res.returncode == 0
    assert int(res.stdout) == 60
    
def test_div_float():
    res = subprocess.run(["./build/app.exe","--float"], input="5/2", text=True, capture_output=True)
    assert res.returncode == 0
    assert float(res.stdout) == 2.5
    
def test_div_null():
    res = subprocess.run(["./build/app.exe"], input="5/0", text=True, capture_output=True)
    assert res.returncode != 0 
    
def test_lot_simb():
    res = subprocess.run(["./build/app.exe"], input="10++5", text=True, capture_output=True)
    assert res.returncode != 0 

    
def test_large_num():
    res = subprocess.run(["./build/app.exe"], input="2000000001", text=True, capture_output=True)
    assert res.returncode != 0

    
def test_small_num():
    res = subprocess.run(["./build/app.exe"], input="0-2000000001", text=True, capture_output=True)
    assert res.returncode != 0

def test_lot_braces():
    res = subprocess.run(["./build/app.exe"], input="4*((7-4)", text=True, capture_output=True)
    assert res.returncode != 0
    
def test_wrong_sim():
    res = subprocess.run(["./build/app.exe"], input="seven", text=True, capture_output=True)
    assert res.returncode != 0
    
def test_umin():
    res = subprocess.run(["./build/app.exe"], input="-4", text=True, capture_output=True)
    assert res.returncode != 0
