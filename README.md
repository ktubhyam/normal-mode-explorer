# Normal Mode Explorer

Visualize and decompose molecular vibrations into individual normal modes. See how each mode contributes to the total vibrational motion.

## Features

- Decompose molecular vibrations into individual normal modes
- Animate each mode independently or combined
- Symmetry labels and selection rules (IR/Raman active)
- Side-by-side comparison of different modes
- Energy distribution visualization

## Tech Stack

- **Framework:** Next.js 15 + TypeScript
- **3D:** Three.js + React Three Fiber
- **Styling:** Tailwind CSS 4
- **Data:** QM9S normal mode data

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## How It Works

Normal modes are the fundamental vibrational patterns of a molecule. Each mode is characterized by:
- A **frequency** (in cm⁻¹) — how fast the atoms vibrate
- A **displacement vector** — which direction each atom moves
- **Symmetry labels** — which point group irreducible representation it belongs to
- **Selection rules** — whether it's IR-active, Raman-active, or silent

This tool lets you explore each mode visually and understand how molecular symmetry determines what spectroscopy can observe.

## License

MIT
