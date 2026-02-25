#!/usr/bin/env python3
"""Generate molecule JSON files for Normal Mode Explorer."""

import json
import math
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public", "molecules")

MASSES = {
    "H": 1.008, "B": 10.811, "C": 12.011, "N": 14.007,
    "O": 15.999, "F": 18.998, "P": 30.974, "S": 32.065, "Cl": 35.453,
}


def make_atom(el: str, x: float, y: float, z: float) -> dict:
    return {"element": el, "x": round(x, 6), "y": round(y, 6), "z": round(z, 6), "mass": MASSES[el]}


def make_bond(a1: int, a2: int, order: int = 1) -> dict:
    return {"atom1": a1, "atom2": a2, "order": order}


def normalize_displacements(disps: list[list[float]]) -> list[list[float]]:
    max_mag = max(math.sqrt(sum(c**2 for c in d)) for d in disps) or 1.0
    return [[round(c / max_mag, 6) for c in d] for d in disps]


def make_mode(idx: int, freq: float, ir: float, raman: float,
              disps: list[list[float]], sym: str = "") -> dict:
    return {
        "index": idx,
        "frequency": freq,
        "ir_intensity": ir,
        "raman_activity": raman,
        "symmetry": sym,
        "displacements": normalize_displacements(disps),
    }


def lorentzian_spectrum(modes: list[dict], wn_start=500, wn_end=4000, wn_step=10, gamma=10.0) -> dict:
    wavenumbers = list(range(wn_start, wn_end + 1, wn_step))
    ir_spec = []
    raman_spec = []
    for w in wavenumbers:
        ir_val = sum(m["ir_intensity"] * gamma**2 / ((w - m["frequency"])**2 + gamma**2) for m in modes)
        raman_val = sum(m["raman_activity"] * gamma**2 / ((w - m["frequency"])**2 + gamma**2) for m in modes)
        ir_spec.append(round(ir_val, 10))
        raman_spec.append(round(raman_val, 10))
    return {"wavenumbers": wavenumbers, "ir": ir_spec, "raman": raman_spec}


def build_molecule(mol_id: str, name: str, formula: str, smiles: str,
                   atoms: list[dict], bonds: list[dict], modes: list[dict]) -> dict:
    return {
        "name": mol_id,
        "formula": formula,
        "smiles": smiles,
        "atomCount": len(atoms),
        "atoms": atoms,
        "bonds": bonds,
        "modes": modes,
        "spectrum": lorentzian_spectrum(modes),
    }


# ============================================================
# Molecule definitions
# ============================================================

Z = [0.0, 0.0, 0.0]


def carbon_dioxide():
    """CO2 - linear, D_inf_h"""
    d = 1.16
    atoms = [make_atom("C", 0, 0, 0), make_atom("O", -d, 0, 0), make_atom("O", d, 0, 0)]
    bonds = [make_bond(0, 1, 2), make_bond(0, 2, 2)]
    modes = [
        make_mode(0, 667.0, 0.0, 0.0, [[0, 0.5, 0], [0, -0.7, 0], [0, 0.7, 0]], "Pi_u bend"),
        make_mode(1, 667.0, 0.0, 0.0, [[0, 0, 0.5], [0, 0, -0.7], [0, 0, 0.7]], "Pi_u bend"),
        make_mode(2, 1388.0, 0.0, 7.0, [[0, 0, 0], [-0.7, 0, 0], [0.7, 0, 0]], "Sigma_g sym stretch"),
        make_mode(3, 2349.0, 100.0, 0.0, [[-0.5, 0, 0], [0.7, 0, 0], [0.7, 0, 0]], "Sigma_u asym stretch"),
    ]
    # CO2 bends are IR active (degenerate pair), sym stretch is Raman only, asym is IR only
    modes[0]["ir_intensity"] = 20.0
    modes[1]["ir_intensity"] = 20.0
    return build_molecule("carbon_dioxide", "Carbon Dioxide", "CO2", "O=C=O", atoms, bonds, modes)


def hydrogen_fluoride():
    """HF - diatomic"""
    d = 0.917
    atoms = [make_atom("H", 0, 0, 0), make_atom("F", d, 0, 0)]
    bonds = [make_bond(0, 1, 1)]
    modes = [make_mode(0, 4138.0, 45.0, 3.0, [[-0.95, 0, 0], [0.05, 0, 0]], "Sigma stretch")]
    return build_molecule("hydrogen_fluoride", "Hydrogen Fluoride", "HF", "[H]F", atoms, bonds, modes)


def hydrogen_chloride():
    """HCl - diatomic"""
    d = 1.275
    atoms = [make_atom("H", 0, 0, 0), make_atom("Cl", d, 0, 0)]
    bonds = [make_bond(0, 1, 1)]
    modes = [make_mode(0, 2886.0, 35.0, 4.0, [[-0.97, 0, 0], [0.03, 0, 0]], "Sigma stretch")]
    return build_molecule("hydrogen_chloride", "Hydrogen Chloride", "HCl", "[H]Cl", atoms, bonds, modes)


def sulfur_dioxide():
    """SO2 - bent, C2v"""
    d = 1.43
    angle = math.radians(119.0 / 2)
    atoms = [
        make_atom("S", 0, 0, 0),
        make_atom("O", -d * math.sin(angle), d * math.cos(angle), 0),
        make_atom("O", d * math.sin(angle), d * math.cos(angle), 0),
    ]
    bonds = [make_bond(0, 1, 2), make_bond(0, 2, 2)]
    modes = [
        make_mode(0, 518.0, 3.0, 1.5, [[0, -0.3, 0], [0.7, 0.5, 0], [-0.7, 0.5, 0]], "A1 bend"),
        make_mode(1, 1151.0, 8.0, 5.0, [[0, 0.3, 0], [0, -0.7, 0], [0, -0.7, 0]], "A1 sym stretch"),
        make_mode(2, 1362.0, 25.0, 0.5, [[0, 0, 0], [-0.7, 0.3, 0], [0.7, 0.3, 0]], "B1 asym stretch"),
    ]
    return build_molecule("sulfur_dioxide", "Sulfur Dioxide", "SO2", "O=S=O", atoms, bonds, modes)


def hydrogen_sulfide():
    """H2S - bent, C2v"""
    d = 1.336
    angle = math.radians(92.1 / 2)
    atoms = [
        make_atom("S", 0, 0, 0),
        make_atom("H", -d * math.sin(angle), d * math.cos(angle), 0),
        make_atom("H", d * math.sin(angle), d * math.cos(angle), 0),
    ]
    bonds = [make_bond(0, 1, 1), make_bond(0, 2, 1)]
    modes = [
        make_mode(0, 1183.0, 5.0, 3.0, [[0, -0.05, 0], [0.7, 0.5, 0], [-0.7, 0.5, 0]], "A1 bend"),
        make_mode(1, 2615.0, 2.0, 7.0, [[0, 0.06, 0], [0, -0.7, 0], [0, -0.7, 0]], "A1 sym stretch"),
        make_mode(2, 2626.0, 8.0, 1.0, [[0, 0, 0], [0.3, -0.7, 0], [-0.3, -0.7, 0]], "B2 asym stretch"),
    ]
    return build_molecule("hydrogen_sulfide", "Hydrogen Sulfide", "H2S", "S", atoms, bonds, modes)


def phosphine():
    """PH3 - pyramidal, C3v"""
    d = 1.42
    angle = math.radians(93.3)
    h_z = d * math.cos(angle)
    h_r = d * math.sin(angle)
    atoms = [
        make_atom("P", 0, 0, 0),
        make_atom("H", h_r, 0, h_z),
        make_atom("H", -h_r * 0.5, h_r * 0.866, h_z),
        make_atom("H", -h_r * 0.5, -h_r * 0.866, h_z),
    ]
    bonds = [make_bond(0, 1, 1), make_bond(0, 2, 1), make_bond(0, 3, 1)]
    modes = [
        make_mode(0, 992.0, 10.0, 2.0, [
            [0, 0, -0.1], [0.5, 0, 0.4], [-0.25, 0.43, 0.4], [-0.25, -0.43, 0.4]
        ], "A1 bend"),
        make_mode(1, 1118.0, 15.0, 0.5, [
            [0, 0, 0], [0.3, 0, -0.5], [-0.6, 0.35, 0.25], [0.3, -0.35, 0.25]
        ], "E bend"),
        make_mode(2, 1118.0, 15.0, 0.5, [
            [0, 0, 0], [0, 0.5, 0], [0.43, -0.25, 0], [-0.43, -0.25, 0]
        ], "E bend"),
        make_mode(3, 2323.0, 3.0, 8.0, [
            [0, 0, 0.1], [-0.4, 0, -0.5], [0.2, -0.35, -0.5], [0.2, 0.35, -0.5]
        ], "A1 sym stretch"),
        make_mode(4, 2328.0, 6.0, 2.0, [
            [0, 0, 0], [-0.7, 0, 0.35], [0.35, -0.6, 0.35], [0.35, 0.6, -0.7]
        ], "E asym stretch"),
        make_mode(5, 2328.0, 6.0, 2.0, [
            [0, 0, 0], [0, -0.7, 0], [0.6, 0.35, 0], [-0.6, 0.35, 0]
        ], "E asym stretch"),
    ]
    return build_molecule("phosphine", "Phosphine", "PH3", "P", atoms, bonds, modes)


def boron_trifluoride():
    """BF3 - trigonal planar, D3h"""
    d = 1.313
    atoms = [
        make_atom("B", 0, 0, 0),
        make_atom("F", d, 0, 0),
        make_atom("F", -d * 0.5, d * 0.866, 0),
        make_atom("F", -d * 0.5, -d * 0.866, 0),
    ]
    bonds = [make_bond(0, 1, 1), make_bond(0, 2, 1), make_bond(0, 3, 1)]
    modes = [
        make_mode(0, 480.0, 0.0, 2.0, [
            [0, 0, 0.3], [0, 0, -0.6], [0, 0, -0.6], [0, 0, -0.6]
        ], "A2'' oop"),
        make_mode(1, 691.0, 15.0, 0.0, [
            [0.2, 0, 0], [-0.6, 0, 0], [0.3, -0.5, 0], [0.3, 0.5, 0]
        ], "E' asym stretch"),
        make_mode(2, 691.0, 15.0, 0.0, [
            [0, 0.2, 0], [0, 0, 0], [0.5, -0.3, 0], [-0.5, -0.3, 0]
        ], "E' asym stretch"),
        make_mode(3, 888.0, 0.0, 5.0, [
            [0, 0, 0], [-0.6, 0, 0], [0.3, -0.5, 0], [0.3, 0.5, 0]
        ], "A1' sym stretch"),
        make_mode(4, 1453.0, 60.0, 0.0, [
            [-0.15, 0, 0], [0.6, 0, 0], [-0.3, 0.5, 0], [-0.3, -0.5, 0]
        ], "E' bend"),
        make_mode(5, 1453.0, 60.0, 0.0, [
            [0, -0.15, 0], [0, 0.6, 0], [-0.5, -0.3, 0], [0.5, -0.3, 0]
        ], "E' bend"),
    ]
    return build_molecule("boron_trifluoride", "Boron Trifluoride", "BF3", "FB(F)F", atoms, bonds, modes)


def carbon_tetrachloride():
    """CCl4 - tetrahedral, Td"""
    d = 1.766
    s = d / math.sqrt(3)
    atoms = [
        make_atom("C", 0, 0, 0),
        make_atom("Cl", s, s, s),
        make_atom("Cl", s, -s, -s),
        make_atom("Cl", -s, s, -s),
        make_atom("Cl", -s, -s, s),
    ]
    bonds = [make_bond(0, 1, 1), make_bond(0, 2, 1), make_bond(0, 3, 1), make_bond(0, 4, 1)]
    modes = [
        # A1 sym stretch (Raman only)
        make_mode(0, 459.0, 0.0, 10.0, [
            Z, [0.3, 0.3, 0.3], [0.3, -0.3, -0.3], [-0.3, 0.3, -0.3], [-0.3, -0.3, 0.3]
        ], "A1 sym stretch"),
        # E bend (Raman only, 2-fold degenerate)
        make_mode(1, 218.0, 0.0, 2.0, [
            Z, [0.3, 0.3, -0.6], [0.3, -0.3, 0.6], [-0.3, 0.3, 0.6], [-0.3, -0.3, -0.6]
        ], "E bend"),
        make_mode(2, 218.0, 0.0, 2.0, [
            Z, [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, -0.5, 0], [-0.5, 0.5, 0]
        ], "E bend"),
        # T2 asym stretch (IR active, 3-fold degenerate)
        make_mode(3, 776.0, 80.0, 1.0, [
            [0.2, 0, 0], [-0.5, 0.3, 0.3], [-0.5, -0.3, -0.3], [0.5, 0.3, -0.3], [0.5, -0.3, 0.3]
        ], "T2 asym stretch"),
        make_mode(4, 776.0, 80.0, 1.0, [
            [0, 0.2, 0], [0.3, -0.5, 0.3], [-0.3, -0.5, -0.3], [0.3, 0.5, -0.3], [-0.3, 0.5, 0.3]
        ], "T2 asym stretch"),
        make_mode(5, 776.0, 80.0, 1.0, [
            [0, 0, 0.2], [0.3, 0.3, -0.5], [-0.3, -0.3, -0.5], [-0.3, 0.3, 0.5], [0.3, -0.3, 0.5]
        ], "T2 asym stretch"),
        # T2 bend (IR active, 3-fold degenerate)
        make_mode(6, 314.0, 10.0, 0.5, [
            [0, 0.1, 0.1], [0, -0.3, 0.3], [0, 0.3, -0.3], [0, 0.3, -0.3], [0, -0.3, 0.3]
        ], "T2 bend"),
        make_mode(7, 314.0, 10.0, 0.5, [
            [0.1, 0, 0.1], [-0.3, 0, 0.3], [0.3, 0, -0.3], [0.3, 0, -0.3], [-0.3, 0, 0.3]
        ], "T2 bend"),
        make_mode(8, 314.0, 10.0, 0.5, [
            [0.1, 0.1, 0], [0.3, -0.3, 0], [-0.3, 0.3, 0], [-0.3, 0.3, 0], [0.3, -0.3, 0]
        ], "T2 bend"),
    ]
    return build_molecule("carbon_tetrachloride", "Carbon Tetrachloride", "CCl4", "ClC(Cl)(Cl)Cl", atoms, bonds, modes)


def nitrous_oxide():
    """N2O - linear, asymmetric"""
    # N=N=O arrangement
    d_nn = 1.128
    d_no = 1.184
    atoms = [
        make_atom("N", 0, 0, 0),
        make_atom("N", d_nn, 0, 0),
        make_atom("O", d_nn + d_no, 0, 0),
    ]
    bonds = [make_bond(0, 1, 2), make_bond(1, 2, 2)]
    modes = [
        make_mode(0, 589.0, 15.0, 0.5, [[0, 0.5, 0], [0, -0.7, 0], [0, 0.3, 0]], "Pi bend"),
        make_mode(1, 589.0, 15.0, 0.5, [[0, 0, 0.5], [0, 0, -0.7], [0, 0, 0.3]], "Pi bend"),
        make_mode(2, 1285.0, 6.0, 4.0, [[-0.5, 0, 0], [0.1, 0, 0], [0.7, 0, 0]], "Sym stretch"),
        make_mode(3, 2224.0, 100.0, 0.3, [[0.5, 0, 0], [-0.7, 0, 0], [0.3, 0, 0]], "Asym stretch"),
    ]
    return build_molecule("nitrous_oxide", "Nitrous Oxide", "N2O", "[N-]=[N+]=O", atoms, bonds, modes)


def formic_acid():
    """HCOOH"""
    atoms = [
        make_atom("C", 0, 0, 0),
        make_atom("O", 1.20, 0, 0),         # C=O
        make_atom("O", -0.36, 1.08, 0),      # C-OH
        make_atom("H", -0.55, -0.77, 0),     # C-H
        make_atom("H", -0.36 + 0.87, 1.08 + 0.50, 0),  # O-H
    ]
    bonds = [
        make_bond(0, 1, 2), make_bond(0, 2, 1), make_bond(0, 3, 1), make_bond(2, 4, 1),
    ]
    modes = [
        make_mode(0, 625.0, 12.0, 0.5, [
            [0.1, 0.1, 0], [-0.3, -0.2, 0], [0.1, -0.2, 0], [0.1, 0.3, 0], [-0.3, 0.8, 0]
        ], "OCO bend"),
        make_mode(1, 1033.0, 20.0, 1.0, [
            [0.1, 0, 0], [0.05, 0, 0], [-0.5, 0, 0], [0.05, 0, 0], [0.8, -0.4, 0]
        ], "C-O stretch"),
        make_mode(2, 1105.0, 30.0, 0.5, [
            [0, 0.1, 0], [0, -0.1, 0], [0, -0.1, 0], [0, -0.8, 0], [0, 0.3, 0]
        ], "CH bend"),
        make_mode(3, 1229.0, 25.0, 0.8, [
            [-0.1, 0, 0], [0.2, 0, 0], [-0.3, 0, 0], [0.1, 0, 0], [0.5, -0.7, 0]
        ], "C-O-H bend"),
        make_mode(4, 1387.0, 5.0, 1.5, [
            [0.2, 0, 0], [-0.5, 0, 0], [0.3, 0, 0], [-0.1, 0, 0], [0.1, 0, 0]
        ], "sym C-O stretch"),
        make_mode(5, 1770.0, 80.0, 3.0, [
            [0.2, 0, 0], [-0.7, 0, 0], [0.1, 0, 0], [-0.05, 0, 0], [0.05, 0, 0]
        ], "C=O stretch"),
        make_mode(6, 2943.0, 10.0, 5.0, [
            [0.05, 0.03, 0], [0, 0, 0], [0, 0, 0], [-0.7, -0.7, 0], [0, 0, 0]
        ], "C-H stretch"),
        make_mode(7, 3570.0, 50.0, 2.0, [
            [0, 0, 0], [0, 0, 0], [0.02, 0, 0], [0, 0, 0], [0.5, -0.85, 0]
        ], "O-H stretch"),
        make_mode(8, 1036.0, 5.0, 0.2, [
            [0, 0, 0.3], [0, 0, -0.2], [0, 0, -0.2], [0, 0, -0.8], [0, 0, 0.3]
        ], "CH oop bend"),
    ]
    return build_molecule("formic_acid", "Formic Acid", "CH2O2", "OC=O", atoms, bonds, modes)


def acetic_acid():
    """CH3COOH"""
    atoms = [
        make_atom("C", 0, 0, 0),              # 0: CH3
        make_atom("C", 1.52, 0, 0),            # 1: C(=O)OH
        make_atom("O", 1.52 + 1.20, 0, 0),     # 2: =O
        make_atom("O", 1.52 - 0.36, 1.08, 0),  # 3: -OH
        make_atom("H", -0.36, -0.51, 0.89),    # 4: H
        make_atom("H", -0.36, -0.51, -0.89),   # 5: H
        make_atom("H", -0.36, 1.02, 0),         # 6: H
        make_atom("H", 1.52 - 0.36 + 0.87, 1.08 + 0.50, 0),  # 7: OH
    ]
    bonds = [
        make_bond(0, 1, 1), make_bond(1, 2, 2), make_bond(1, 3, 1),
        make_bond(0, 4, 1), make_bond(0, 5, 1), make_bond(0, 6, 1),
        make_bond(3, 7, 1),
    ]
    n = 8
    modes = []
    freqs = [
        (0, 432.0, 3.0, 0.3, "CCO bend"),
        (1, 581.0, 8.0, 0.5, "OCO bend"),
        (2, 642.0, 15.0, 0.2, "C=O oop"),
        (3, 847.0, 5.0, 0.8, "C-C stretch"),
        (4, 989.0, 12.0, 0.4, "CH3 rock"),
        (5, 1048.0, 25.0, 1.0, "C-O stretch"),
        (6, 1178.0, 20.0, 0.6, "C-O-H bend"),
        (7, 1258.0, 35.0, 0.5, "CH3 rock"),
        (8, 1382.0, 8.0, 1.5, "sym CH3 bend"),
        (9, 1430.0, 5.0, 0.8, "asym CH3 bend"),
        (10, 1430.0, 5.0, 0.8, "asym CH3 bend"),
        (11, 1788.0, 80.0, 4.0, "C=O stretch"),
        (12, 2944.0, 3.0, 3.0, "sym CH3 stretch"),
        (13, 2996.0, 5.0, 2.0, "asym CH3 stretch"),
        (14, 2996.0, 5.0, 2.0, "asym CH3 stretch"),
        (15, 3051.0, 2.0, 1.5, "asym CH3 stretch"),
        (16, 3583.0, 45.0, 2.5, "O-H stretch"),
        (17, 534.0, 2.0, 0.1, "torsion"),
    ]
    import random
    random.seed(42)
    for idx, freq, ir, raman, sym in freqs:
        disps = []
        for _ in range(n):
            disps.append([round(random.gauss(0, 0.3), 3) for _ in range(3)])
        # Make the highest-frequency atom move most
        if "CH3 stretch" in sym:
            for i in [4, 5, 6]:
                disps[i] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        elif "O-H" in sym:
            disps[7] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        elif "C=O" in sym:
            disps[2] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        modes.append(make_mode(idx, freq, ir, raman, disps, sym))
    return build_molecule("acetic_acid", "Acetic Acid", "C2H4O2", "CC(=O)O", atoms, bonds, modes)


def dimethyl_ether():
    """CH3OCH3"""
    d_co = 1.41
    angle = math.radians(111.7 / 2)
    atoms = [
        make_atom("O", 0, 0, 0),
        make_atom("C", -d_co * math.sin(angle), d_co * math.cos(angle), 0),
        make_atom("C", d_co * math.sin(angle), d_co * math.cos(angle), 0),
    ]
    c1 = (atoms[1]["x"], atoms[1]["y"])
    c2 = (atoms[2]["x"], atoms[2]["y"])
    d_ch = 1.09
    # Add H atoms to each carbon
    for ci, (cx, cy) in enumerate([c1, c2], 1):
        sign = -1 if ci == 1 else 1
        atoms.append(make_atom("H", cx, cy + d_ch, 0))
        atoms.append(make_atom("H", cx + sign * d_ch * 0.87, cy - d_ch * 0.5, d_ch * 0.5))
        atoms.append(make_atom("H", cx + sign * d_ch * 0.87, cy - d_ch * 0.5, -d_ch * 0.5))
    bonds = [
        make_bond(0, 1, 1), make_bond(0, 2, 1),
        make_bond(1, 3, 1), make_bond(1, 4, 1), make_bond(1, 5, 1),
        make_bond(2, 6, 1), make_bond(2, 7, 1), make_bond(2, 8, 1),
    ]
    n = 9
    import random
    random.seed(43)
    mode_data = [
        (0, 242.0, 0.5, 0.1, "torsion"),
        (1, 418.0, 1.0, 0.3, "COC bend"),
        (2, 924.0, 3.0, 0.5, "CH3 rock"),
        (3, 924.0, 3.0, 0.5, "CH3 rock"),
        (4, 1102.0, 25.0, 0.8, "C-O-C asym stretch"),
        (5, 1150.0, 5.0, 3.0, "C-O-C sym stretch"),
        (6, 1179.0, 8.0, 0.4, "CH3 rock"),
        (7, 1179.0, 8.0, 0.4, "CH3 rock"),
        (8, 1244.0, 12.0, 0.3, "CH3 twist"),
        (9, 1452.0, 3.0, 1.0, "CH3 bend"),
        (10, 1452.0, 3.0, 1.0, "CH3 bend"),
        (11, 1464.0, 5.0, 0.8, "CH3 bend"),
        (12, 1464.0, 5.0, 0.8, "CH3 bend"),
        (13, 1469.0, 2.0, 1.2, "CH3 sym bend"),
        (14, 1469.0, 2.0, 1.2, "CH3 sym bend"),
        (15, 2817.0, 10.0, 5.0, "CH3 sym stretch"),
        (16, 2817.0, 10.0, 5.0, "CH3 sym stretch"),
        (17, 2925.0, 3.0, 2.0, "CH3 asym stretch"),
        (18, 2925.0, 3.0, 2.0, "CH3 asym stretch"),
        (19, 2996.0, 5.0, 1.5, "CH3 asym stretch"),
        (20, 2996.0, 5.0, 1.5, "CH3 asym stretch"),
    ]
    modes = []
    for idx, freq, ir, raman, sym in mode_data:
        disps = [[round(random.gauss(0, 0.3), 3) for _ in range(3)] for _ in range(n)]
        modes.append(make_mode(idx, freq, ir, raman, disps, sym))
    return build_molecule("dimethyl_ether", "Dimethyl Ether", "C2H6O", "COC", atoms, bonds, modes)


def methylamine():
    """CH3NH2"""
    d_cn = 1.471
    d_ch = 1.09
    d_nh = 1.01
    atoms = [
        make_atom("C", 0, 0, 0),
        make_atom("N", d_cn, 0, 0),
        make_atom("H", -0.36, 0.51, 0.89),
        make_atom("H", -0.36, 0.51, -0.89),
        make_atom("H", -0.36, -1.02, 0),
        make_atom("H", d_cn + d_nh * 0.39, d_nh * 0.45, d_nh * 0.80),
        make_atom("H", d_cn + d_nh * 0.39, d_nh * 0.45, -d_nh * 0.80),
    ]
    bonds = [
        make_bond(0, 1, 1),
        make_bond(0, 2, 1), make_bond(0, 3, 1), make_bond(0, 4, 1),
        make_bond(1, 5, 1), make_bond(1, 6, 1),
    ]
    n = 7
    import random
    random.seed(44)
    mode_data = [
        (0, 268.0, 1.0, 0.1, "torsion"),
        (1, 780.0, 8.0, 0.5, "NH2 wag"),
        (2, 1044.0, 5.0, 1.0, "C-N stretch"),
        (3, 1130.0, 3.0, 0.3, "CH3 rock"),
        (4, 1130.0, 3.0, 0.3, "CH3 rock"),
        (5, 1195.0, 2.0, 0.5, "NH2 twist"),
        (6, 1419.0, 5.0, 0.8, "CH3 bend"),
        (7, 1419.0, 5.0, 0.8, "CH3 bend"),
        (8, 1474.0, 3.0, 1.2, "CH3 sym bend"),
        (9, 1623.0, 20.0, 1.5, "NH2 scissor"),
        (10, 2820.0, 8.0, 5.0, "CH3 sym stretch"),
        (11, 2961.0, 3.0, 2.0, "CH3 asym stretch"),
        (12, 2961.0, 3.0, 2.0, "CH3 asym stretch"),
        (13, 3361.0, 1.0, 3.0, "NH2 sym stretch"),
        (14, 3427.0, 2.0, 1.5, "NH2 asym stretch"),
    ]
    modes = []
    for idx, freq, ir, raman, sym in mode_data:
        disps = [[round(random.gauss(0, 0.3), 3) for _ in range(3)] for _ in range(n)]
        if "NH2" in sym and "stretch" in sym:
            disps[5] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
            disps[6] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        elif "CH3" in sym and "stretch" in sym:
            for i in [2, 3, 4]:
                disps[i] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        modes.append(make_mode(idx, freq, ir, raman, disps, sym))
    return build_molecule("methylamine", "Methylamine", "CH5N", "CN", atoms, bonds, modes)


def urea():
    """CO(NH2)2"""
    atoms = [
        make_atom("C", 0, 0, 0),
        make_atom("O", 0, 1.22, 0),
        make_atom("N", -1.14, -0.64, 0),
        make_atom("N", 1.14, -0.64, 0),
        make_atom("H", -1.14 - 0.42, -0.64 - 0.90, 0),
        make_atom("H", -1.14 - 0.91, -0.64 + 0.42, 0),
        make_atom("H", 1.14 + 0.42, -0.64 - 0.90, 0),
        make_atom("H", 1.14 + 0.91, -0.64 + 0.42, 0),
    ]
    bonds = [
        make_bond(0, 1, 2), make_bond(0, 2, 1), make_bond(0, 3, 1),
        make_bond(2, 4, 1), make_bond(2, 5, 1),
        make_bond(3, 6, 1), make_bond(3, 7, 1),
    ]
    n = 8
    import random
    random.seed(45)
    mode_data = [
        (0, 450.0, 5.0, 0.5, "NCN bend"),
        (1, 547.0, 10.0, 0.3, "C=O oop"),
        (2, 786.0, 3.0, 0.8, "NCN sym stretch"),
        (3, 1006.0, 8.0, 0.4, "NH2 rock"),
        (4, 1006.0, 8.0, 0.4, "NH2 rock"),
        (5, 1150.0, 20.0, 1.0, "C-N stretch"),
        (6, 1395.0, 30.0, 1.5, "NCN asym stretch"),
        (7, 1464.0, 5.0, 0.8, "NH2 twist"),
        (8, 1464.0, 5.0, 0.8, "NH2 twist"),
        (9, 1598.0, 15.0, 2.0, "NH2 scissor"),
        (10, 1598.0, 15.0, 2.0, "NH2 scissor"),
        (11, 1686.0, 85.0, 3.5, "C=O stretch"),
        (12, 3350.0, 5.0, 5.0, "NH2 sym stretch"),
        (13, 3350.0, 5.0, 5.0, "NH2 sym stretch"),
        (14, 3440.0, 15.0, 2.0, "NH2 asym stretch"),
        (15, 3440.0, 15.0, 2.0, "NH2 asym stretch"),
        (16, 380.0, 1.0, 0.1, "torsion"),
        (17, 1060.0, 4.0, 0.3, "NH2 wag"),
    ]
    modes = []
    for idx, freq, ir, raman, sym in mode_data:
        disps = [[round(random.gauss(0, 0.3), 3) for _ in range(3)] for _ in range(n)]
        if "C=O" in sym and "stretch" in sym.lower():
            disps[1] = [0, round(random.gauss(0, 0.8), 3), 0]
        elif "NH2" in sym and "stretch" in sym:
            for i in [4, 5, 6, 7]:
                disps[i] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        modes.append(make_mode(idx, freq, ir, raman, disps, sym))
    return build_molecule("urea", "Urea", "CH4N2O", "NC(=O)N", atoms, bonds, modes)


def glycine():
    """NH2CH2COOH - simplest amino acid"""
    atoms = [
        make_atom("N", -1.47, 0, 0),           # 0
        make_atom("C", 0, 0, 0),                # 1: alpha C
        make_atom("C", 1.52, 0, 0),             # 2: carboxyl C
        make_atom("O", 1.52 + 1.03, 0.73, 0),   # 3: =O
        make_atom("O", 1.52 + 0.36, -1.08, 0),  # 4: -OH
        make_atom("H", 1.52 + 0.36 + 0.87, -1.08 - 0.50, 0),  # 5: OH H
        make_atom("H", 0, 0.89, 0.63),          # 6: Ca H
        make_atom("H", 0, -0.89, 0.63),         # 7: Ca H
        make_atom("H", -1.47 - 0.41, 0.81, 0.34),  # 8: NH H
        make_atom("H", -1.47 - 0.41, -0.81, 0.34), # 9: NH H
    ]
    bonds = [
        make_bond(0, 1, 1), make_bond(1, 2, 1),
        make_bond(2, 3, 2), make_bond(2, 4, 1), make_bond(4, 5, 1),
        make_bond(1, 6, 1), make_bond(1, 7, 1),
        make_bond(0, 8, 1), make_bond(0, 9, 1),
    ]
    n = 10
    import random
    random.seed(46)
    mode_data = [
        (0, 250.0, 2.0, 0.1, "skeletal bend"),
        (1, 335.0, 3.0, 0.15, "NH2 torsion"),
        (2, 504.0, 8.0, 0.5, "OCO bend"),
        (3, 577.0, 5.0, 0.3, "rocking"),
        (4, 696.0, 12.0, 0.2, "oop bend"),
        (5, 801.0, 6.0, 1.0, "C-C stretch"),
        (6, 883.0, 3.0, 0.5, "CH2 rock"),
        (7, 918.0, 4.0, 0.4, "NH2 wag"),
        (8, 1033.0, 15.0, 1.2, "C-O stretch"),
        (9, 1101.0, 25.0, 0.6, "C-N stretch"),
        (10, 1148.0, 10.0, 0.8, "CH2 wag"),
        (11, 1255.0, 20.0, 1.5, "C-O-H bend"),
        (12, 1340.0, 12.0, 1.0, "CH2 twist"),
        (13, 1371.0, 8.0, 0.9, "C-O stretch"),
        (14, 1429.0, 5.0, 0.5, "CH2 scissor"),
        (15, 1600.0, 15.0, 1.0, "NH2 scissor"),
        (16, 1763.0, 75.0, 5.0, "C=O stretch"),
        (17, 2910.0, 8.0, 4.0, "CH2 sym stretch"),
        (18, 2969.0, 5.0, 3.0, "CH2 asym stretch"),
        (19, 3359.0, 2.0, 5.0, "NH2 sym stretch"),
        (20, 3425.0, 1.0, 3.5, "NH2 asym stretch"),
        (21, 3568.0, 50.0, 2.5, "O-H stretch"),
        (22, 640.0, 10.0, 0.1, "oop wag"),
        (23, 420.0, 4.0, 0.2, "skeletal twist"),
    ]
    modes = []
    for idx, freq, ir, raman, sym in mode_data:
        disps = [[round(random.gauss(0, 0.3), 3) for _ in range(3)] for _ in range(n)]
        if "C=O" in sym:
            disps[3] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        elif "O-H" in sym:
            disps[5] = [round(random.gauss(0, 0.9), 3) for _ in range(3)]
        elif "CH2" in sym and "stretch" in sym:
            disps[6] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
            disps[7] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        elif "NH2" in sym and "stretch" in sym:
            disps[8] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
            disps[9] = [round(random.gauss(0, 0.8), 3) for _ in range(3)]
        modes.append(make_mode(idx, freq, ir, raman, disps, sym))
    return build_molecule("glycine", "Glycine", "C2H5NO2", "NCC(=O)O", atoms, bonds, modes)


# ============================================================
# Main
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generators = [
        carbon_dioxide, hydrogen_fluoride, hydrogen_chloride,
        sulfur_dioxide, hydrogen_sulfide, phosphine,
        boron_trifluoride, carbon_tetrachloride, nitrous_oxide,
        formic_acid, acetic_acid, dimethyl_ether,
        methylamine, urea, glycine,
    ]

    for gen in generators:
        mol = gen()
        filepath = os.path.join(OUTPUT_DIR, f"{mol['name']}.json")
        with open(filepath, "w") as f:
            json.dump(mol, f, indent=2)
        print(f"Generated {mol['name']}.json ({mol['atomCount']} atoms, {len(mol['modes'])} modes)")

    # Update index.json
    index_path = os.path.join(OUTPUT_DIR, "index.json")
    existing = {}
    if os.path.exists(index_path):
        with open(index_path) as f:
            for entry in json.load(f):
                existing[entry["id"]] = entry

    for gen in generators:
        mol = gen()
        existing[mol["name"]] = {
            "id": mol["name"],
            "name": mol["name"].replace("_", " ").title(),
            "formula": mol["formula"],
            "smiles": mol["smiles"],
            "atomCount": mol["atomCount"],
            "modeCount": len(mol["modes"]),
        }

    sorted_entries = sorted(existing.values(), key=lambda e: (e["atomCount"], e["name"]))
    with open(index_path, "w") as f:
        json.dump(sorted_entries, f, indent=2)

    print(f"\nUpdated index.json with {len(sorted_entries)} total molecules")
    for e in sorted_entries:
        print(f"  {e['id']}: {e['formula']} ({e['atomCount']} atoms, {e['modeCount']} modes)")


if __name__ == "__main__":
    main()
