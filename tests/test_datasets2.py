import unittest
import os
import site   # so that AI4Water directory is in path
site.addsitedir(os.path.dirname(os.path.dirname(__file__)) )

import pandas as pd

from ai4water.datasets import WeatherJena, SWECanada, MtropicsLaos

# wj = WeatherJena()
# df = wj.fetch()
#
# assert df.shape[0] >= 919551
# assert df.shape[1] >= 21

# swe = SWECanada()
#
# stns = swe.stations()
#
# d = swe.fetch(1)
#
# d = swe.fetch(10, st='20110101')
#
# d = swe.fetch(0.001, st='20110101')
#
# d = swe.fetch('ALE-05AE810', st='20110101')
#
# d = swe.fetch(stns[0:10], st='20110101')

laos = MtropicsLaos()

class TestMtropicsLaos(unittest.TestCase):

    def test_pcp(self):
        pcp = laos.fetch_pcp()
        assert isinstance(pcp.index, pd.DatetimeIndex)
        assert pcp.shape == (1665361, 1)
        assert pcp.index.freqstr == '6T'

    def test_weather_station_data(self):
        w = laos.fetch_weather_station_data()
        assert isinstance(w.index, pd.DatetimeIndex)
        assert w.index.freq == 'H'
        assert w.shape == (166536, 4)
        assert int(w.isna().sum().sum()) == 82114

    def test_fetch_hydro(self):
        wl, spm = laos.fetch_hydro()
        assert wl.shape ==  (454699, 1)
        assert isinstance(wl.index, pd.DatetimeIndex)
        assert spm.shape == (6428, 1)
        assert isinstance(spm.index, pd.DatetimeIndex)

    def test_fetch_ecoli(self):
        ecoli = laos.fetch_ecoli()
        assert ecoli.shape == (409, 1)
        assert int(ecoli.isna().sum()) == 42
        assert isinstance(ecoli.index, pd.DatetimeIndex)
        ecoli_all = laos.fetch_ecoli(features='all')
        assert ecoli_all.shape == (409, 3)
        assert int(ecoli_all.isna().sum().sum()) == 162
        assert isinstance(ecoli_all.index, pd.DatetimeIndex)

    def test_fetch_physio_chem(self):
        phy_chem = laos.fetch_physiochem('T_deg')
        assert phy_chem.shape == (411, 1)
        assert int(phy_chem.isna().sum()) == 63
        assert isinstance(phy_chem.index, pd.DatetimeIndex)
        phy_chem_all = laos.fetch_physiochem(features='all')
        assert phy_chem_all.shape == (411, 8)
        assert int(phy_chem_all.isna().sum().sum()) == 640
        assert isinstance(phy_chem_all.index, pd.DatetimeIndex)

    def test_rain_gauges(self):
        rg = laos.fetch_rain_gauges()
        assert isinstance(rg.index, pd.DatetimeIndex)
        assert rg.index.freq == 'D'
        assert rg.shape == (6939, 7)
        assert int(rg.isna().sum().sum()) == 34510

    def test_fetch(self):
        df = laos.make_regression(st="20110525 10:00:00", en="20190910")
        assert isinstance(df.index, pd.DatetimeIndex)
        assert int(df.isna().sum().sum()) == 10553086
        assert df.shape[-1] == 16
        return

if __name__=="__main__":
    unittest.main()
