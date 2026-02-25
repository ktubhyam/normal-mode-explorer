"use client";

import dynamic from "next/dynamic";
import { useEffect } from "react";
import { useExplorerStore } from "@/lib/store";
import { useKeyboard } from "@/hooks/useKeyboard";
import { Header } from "@/components/Header";
import { MobileModeStrip } from "@/components/MobileModeStrip";
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

  useEffect(() => {
    fetch("/molecules/index.json")
      .then((r) => r.json())
      .then((data: MoleculeManifestEntry[]) => setManifest(data))
      .catch(console.error);
  }, [setManifest]);

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
      <MobileModeStrip />

      {/* Mobile: vertical scroll | Desktop: side-by-side */}
      <div className="flex-1 flex flex-col lg:flex-row min-h-0 overflow-y-auto lg:overflow-hidden">
        {/* 3D viewer — centered on mobile with top padding to push it down */}
        <div className="pt-4 lg:pt-0 h-[50vh] lg:h-auto lg:flex-1 flex flex-col min-w-0 shrink-0">
          <div className="flex-1 min-h-0">
            <ComparisonView />
          </div>
        </div>

        {/* Analysis panels — full width on mobile, fixed sidebar on desktop */}
        <aside className="w-full lg:w-[420px] border-t lg:border-t-0 lg:border-l border-border bg-surface/30 lg:overflow-y-auto shrink-0">
          <div className="p-2 space-y-2">
            {/* Mode list + Animation controls */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <ModeList />
              <div className="space-y-2">
                <AnimationControls />
                <Sonification />
              </div>
            </div>

            {/* Spectrum chart */}
            <SpectrumChart />

            {/* Energy chart + Selection rules */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <EnergyChart />
              <SelectionRules />
            </div>

            {/* Boltzmann + Symmetry */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <BoltzmannPanel />
              <SymmetryInfo />
            </div>

            {/* Displacement table */}
            <DisplacementTable />
          </div>

          {/* Keyboard hints — hidden on touch devices */}
          <div className="hidden lg:block px-3 py-2 border-t border-border">
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
