import { create } from "zustand";
import type { MoleculeData, MoleculeManifestEntry } from "./types";

interface ExplorerStore {
  // Manifest
  manifest: MoleculeManifestEntry[];
  setManifest: (entries: MoleculeManifestEntry[]) => void;

  // Current molecule
  moleculeId: string;
  molecule: MoleculeData | null;
  loading: boolean;
  setMoleculeId: (id: string) => void;
  setMolecule: (data: MoleculeData | null) => void;
  setLoading: (loading: boolean) => void;

  // Dual mode selection
  modeA: number;
  modeB: number | null;
  setModeA: (index: number) => void;
  setModeB: (index: number | null) => void;

  // Superposition: set of mode indices to combine
  superpositionModes: Set<number>;
  toggleSuperpositionMode: (index: number) => void;
  clearSuperposition: () => void;
  superpositionEnabled: boolean;
  setSuperpositionEnabled: (enabled: boolean) => void;

  // Animation controls
  isPlaying: boolean;
  speed: number;
  amplitude: number;
  phase: number;
  togglePlaying: () => void;
  setSpeed: (speed: number) => void;
  setAmplitude: (amplitude: number) => void;
  setPhase: (phase: number) => void;

  // Visual toggles
  showArrows: boolean;
  showTrails: boolean;
  showSymmetryElements: boolean;
  showLabels: boolean;
  showGrid: boolean;
  toggleArrows: () => void;
  toggleTrails: () => void;
  toggleSymmetryElements: () => void;
  toggleLabels: () => void;
  toggleGrid: () => void;

  // Fullscreen
  isFullscreen: boolean;
  setFullscreen: (fs: boolean) => void;

  // Temperature (Kelvin) for Boltzmann distribution
  temperature: number;
  setTemperature: (temp: number) => void;

  // Spectrum display
  spectrumType: "ir" | "raman";
  setSpectrumType: (type: "ir" | "raman") => void;

  // Sonification
  isSoundOn: boolean;
  toggleSound: () => void;
}

export const useExplorerStore = create<ExplorerStore>((set) => ({
  manifest: [],
  setManifest: (entries) => set({ manifest: entries }),

  moleculeId: "water",
  molecule: null,
  loading: false,
  setMoleculeId: (id) =>
    set({
      moleculeId: id,
      modeA: 0,
      modeB: null,
      superpositionModes: new Set(),
      superpositionEnabled: false,
    }),
  setMolecule: (data) => set({ molecule: data }),
  setLoading: (loading) => set({ loading }),

  modeA: 0,
  modeB: null,
  setModeA: (index) => set({ modeA: index }),
  setModeB: (index) => set({ modeB: index }),

  superpositionModes: new Set(),
  toggleSuperpositionMode: (index) =>
    set((s) => {
      const next = new Set(s.superpositionModes);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return { superpositionModes: next };
    }),
  clearSuperposition: () => set({ superpositionModes: new Set() }),
  superpositionEnabled: false,
  setSuperpositionEnabled: (enabled) => set({ superpositionEnabled: enabled }),

  isPlaying: true,
  speed: 1.0,
  amplitude: 0.5,
  phase: 0,
  togglePlaying: () => set((s) => ({ isPlaying: !s.isPlaying })),
  setSpeed: (speed) => set({ speed }),
  setAmplitude: (amplitude) => set({ amplitude }),
  setPhase: (phase) => set({ phase }),

  showArrows: true,
  showTrails: false,
  showSymmetryElements: false,
  showLabels: true,
  showGrid: true,
  toggleArrows: () => set((s) => ({ showArrows: !s.showArrows })),
  toggleTrails: () => set((s) => ({ showTrails: !s.showTrails })),
  toggleSymmetryElements: () =>
    set((s) => ({ showSymmetryElements: !s.showSymmetryElements })),
  toggleLabels: () => set((s) => ({ showLabels: !s.showLabels })),
  toggleGrid: () => set((s) => ({ showGrid: !s.showGrid })),

  isFullscreen: false,
  setFullscreen: (fs) => set({ isFullscreen: fs }),

  temperature: 300,
  setTemperature: (temp) => set({ temperature: temp }),

  spectrumType: "ir",
  setSpectrumType: (type) => set({ spectrumType: type }),

  isSoundOn: false,
  toggleSound: () => set((s) => ({ isSoundOn: !s.isSoundOn })),
}));
