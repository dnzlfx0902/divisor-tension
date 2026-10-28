import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import divisor_tension as m


class Resolver(unittest.TestCase):
    def test_divisor_simetrico(self):
        vout, i = m.resolver(10.0, 1000.0, 1000.0)
        self.assertAlmostEqual(vout, 5.0)
        self.assertAlmostEqual(i, 0.005)

    def test_rechaza_negativos(self):
        for args in ((0, 1, 1), (1, 0, 1), (1, 1, -2)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                m.resolver(*args)


class Serie(unittest.TestCase):
    def test_e24_nunca_arriba(self):
        for r in (470, 1000, 2200, 47000):
            with self.subTest(r=r):
                self.assertLessEqual(m.valores_e24(r), r)

    def test_propuesta_cercana(self):
        r1, r2 = m.proponer(12.0, 3.3)
        vout, _ = m.resolver(12.0, r1, r2)
        self.assertLess(abs(vout - 3.3), 0.35)

    def test_objetivo_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            m.proponer(5.0, 5.0)


if __name__ == "__main__":
    unittest.main()
