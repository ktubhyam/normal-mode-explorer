"use client";

import dynamic from "next/dynamic";
import { useEffect } from "react";
import { useExplorerStore } from "@/lib/store";
import { useKeyboard } from "@/hooks/useKeyboard";
import { Header } from "@/components/Header";
import { ModeList } from "@/components/panels/ModeList";
import { SelectionRules } from "@/components/panels/SelectionRules";
import { AnimationControls } from "@/components/panels/AnimationControls";
import { SymmetryInfo } from "@/components/panels/SymmetryInfo";
import { SpectrumChart } from "@/components/panels/SpectrumChart";
import { BoltzmannPanel } from "@/components/panels/BoltzmannPanel";
import { DisplacementTable } from "@/components/panels/DisplacementTable";
import { Sonification } from "@/components/panels/Sonification";
import { EnergyChart } from "@/components/panels/EnergyChart";
import type { MoleculeData, MoleculeManifestEntry } from "@/lib/types";

// Three.js needs client-only rendering
const ComparisonView = dynamic(
  () =>
    import("@/components/scene/ComparisonView").then((m) => ({
      default: m.ComparisonView,
    })),
  { ssr: false },
);

function DataLoader() {
  const moleculeId = useExplorerStore((s) => s.moleculeId);
  const setMolecule = useExplorerStore((s) => s.setMolecule);
  const setManifest = useExplorerStore((s) => s.setManifest);
  const setLoading = useExplorerStore((s) => s.setLoading);

  // Load manifest on mount
  useEffect(() => {
    fetch("/molecules/index.json")
      .then((r) => r.json())
      .then((data: MoleculeManifestEntry[]) => setManifest(data))
      .catch(console.error);
  }, [setManifest]);

  // Load molecule when ID changes
  useEffect(() => {
    setLoading(true);
    fetch(`/molecules/${moleculeId}.json`)
      .then((r) => r.json())
      .then((data: MoleculeData) => {
        setMolecule(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load molecule:", err);
        setLoading(false);
      });
  }, [moleculeId, setMolecule, setLoading]);

  return null;
}

export default function Page() {
  useKeyboard();

  return (
    <div className="h-screen flex flex-col">
      <DataLoader />
      <Header />

      <div className="flex-1 flex min-h-0">
        {/* Left: 3D viewer(s) — ~55% */}
        <div className="flex-1 flex flex-col min-h-0 min-w-0">
          <div className="flex-1 min-h-0">
            <ComparisonView />
          </div>
        </div>

        {/* Right: Analysis panels — scrollable dashboard */}
        <aside className="w-[420px] border-l border-border bg-surface/30 overflow-y-auto shrink-0">
          <div className="p-2 space-y-2">
            {/* Row 1: Mode list + Animation controls side by side */}
            <div className="grid grid-cols-2 gap-2">
              <ModeList />
              <div className="space-y-2">
                <AnimationControls />
                <Sonification />
              </div>
            </div>

            {/* Row 2: Spectrum chart (full width) */}
            <SpectrumChart />

            {/* Row 3: Energy chart + Selection rules */}
            <div className="grid grid-cols-2 gap-2">
              <EnergyChart />
              <SelectionRules />
            </div>

            {/* Row 4: Boltzmann + Symmetry */}
            <div className="grid grid-cols-2 gap-2">
              <BoltzmannPanel />
              <SymmetryInfo />
            </div>

            {/* Row 5: Displacement table (full width) */}
            <DisplacementTable />
          </div>

          {/* Keyboard hints */}
          <div className="px-3 py-2 border-t border-border">
            <div className="text-[9px] font-mono text-foreground/20 space-y-0.5">
              <div>Space — play/pause</div>
              <div>↑↓ — cycle mode A</div>
              <div>←→ — cycle mode B</div>
              <div>B — toggle compare</div>
              <div>Esc — close compare</div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
