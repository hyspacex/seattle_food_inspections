'''
Tests for the visualization.py file
'''
# Now you can import your module

# Import the cleaning_functions
from .. import visualization as vz

def test_folium():
    test_map = vz.make_folium_map(True)
    assert str(type(test_map)) == "<class 'folium.folium.Map'>"

def test_altair():
    t_info = vz.make_altair_map('income')
    assert str(type(t_info)) == "<class 'altair.vegalite.v3.api.HConcatChart'>"
