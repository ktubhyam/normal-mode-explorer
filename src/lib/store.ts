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

  // Animation controls
  isPlaying: boolean;
  speed: number;
  amplitude: number;
  togglePlaying: () => void;
  setSpeed: (speed: number) => void;
  setAmplitude: (amplitude: number) => void;
}

export const useExplorerStore = create<ExplorerStore>((set) => ({
  manifest: [],
  setManifest: (entries) => set({ manifest: entries }),

  moleculeId: "water",
  molecule: null,
  loading: false,
  setMoleculeId: (id) => set({ moleculeId: id, modeA: 0, modeB: null }),
  setMolecule: (data) => set({ molecule: data }),
  setLoading: (loading) => set({ loading }),

  modeA: 0,
  modeB: null,
  setModeA: (index) => set({ modeA: index }),
  setModeB: (index) => set({ modeB: index }),

  isPlaying: true,
  speed: 1.0,
  amplitude: 0.5,
  togglePlaying: () => set((s) => ({ isPlaying: !s.isPlaying })),
  setSpeed: (speed) => set({ speed }),
  setAmplitude: (amplitude) => set({ amplitude }),
}));
