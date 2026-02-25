"use client";

import { useExplorerStore } from "@/lib/store";
import { MiniViewer } from "./MiniViewer";

export function ComparisonView() {
  const molecule = useExplorerStore((s) => s.molecule);
  const modeA = useExplorerStore((s) => s.modeA);
  const modeB = useExplorerStore((s) => s.modeB);
  const loading = useExplorerStore((s) => s.loading);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex items-center gap-2 bg-surface/80 backdrop-blur-sm rounded-lg px-4 py-2.5 border border-border">
          <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
          <span className="text-foreground/50 font-mono text-sm">Loading molecule...</span>
        </div>
      </div>
    );
  }

  if (!molecule) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <span className="text-foreground/30 font-mono text-sm">Select a molecule</span>
      </div>
    );
  }

  const isDual = modeB !== null;

  return (
    <div className="flex-1 flex min-h-0 gap-px bg-border">
      <div className={`flex flex-col min-h-0 bg-background ${isDual ? "w-1/2" : "w-full"}`}>
        <MiniViewer
          molecule={molecule}
          modeIndex={modeA}
          label="A"
          accentColor="#00D8FF"
        />
      </div>
      {isDual && modeB !== null && (
        <div className="flex flex-col min-h-0 w-1/2 bg-background">
          <MiniViewer
            molecule={molecule}
            modeIndex={modeB}
            label="B"
            accentColor="#C9A04A"
          />
        </div>
      )}
    </div>
  );
}
