"use client";

import { useRef, useEffect } from "react";
import { useExplorerStore } from "@/lib/store";
import { MOLECULE_SYMMETRY } from "@/lib/constants";
import { TerminalPanel } from "../ui/TerminalPanel";

export function ModeList() {
  const molecule = useExplorerStore((s) => s.molecule);
  const modeA = useExplorerStore((s) => s.modeA);
  const modeB = useExplorerStore((s) => s.modeB);
  const setModeA = useExplorerStore((s) => s.setModeA);
  const setModeB = useExplorerStore((s) => s.setModeB);

  const listRef = useRef<HTMLDivElement>(null);
  const activeRef = useRef<HTMLButtonElement>(null);

  // Auto-scroll to selected mode A
  useEffect(() => {
    if (activeRef.current && listRef.current) {
      activeRef.current.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }, [modeA]);

  if (!molecule) return null;

  const symmetryData = MOLECULE_SYMMETRY[molecule.name.toLowerCase().replace(/\s+/g, "_")];

  const handleClick = (index: number, e: React.MouseEvent) => {
    if (e.shiftKey || e.metaKey) {
      // Shift/Cmd+click assigns to B
      setModeB(modeB === index ? null : index);
    } else {
      setModeA(index);
    }
  };

  return (
    <TerminalPanel title="Normal Modes">
      <div className="px-1 py-1">
        <div className="text-[9px] font-mono text-foreground/30 px-2 py-1 flex justify-between">
          <span>Click = A · Shift+Click = B</span>
          {modeB !== null && (
            <button
              onClick={() => setModeB(null)}
              className="text-accent/60 hover:text-accent"
            >
              Clear B
            </button>
          )}
        </div>
      </div>
      <div ref={listRef} className="max-h-[280px] overflow-y-auto px-1 pb-1">
        {molecule.modes.map((mode, i) => {
          const isA = i === modeA;
          const isB = i === modeB;
          const symLabel = symmetryData?.modeLabels[i] || mode.symmetry || "";
          const irActive = mode.ir_intensity > 0.1;
          const ramanActive = mode.raman_activity > 0.1;

          return (
            <button
              key={i}
              ref={isA ? activeRef : null}
              onClick={(e) => handleClick(i, e)}
              className={`w-full flex items-center gap-2 px-2 py-1.5 rounded text-left transition-colors text-xs font-mono ${
                isA
                  ? "bg-cyan/10 text-cyan"
                  : isB
                    ? "bg-accent/10 text-accent"
                    : "text-foreground/60 hover:bg-surface-2 hover:text-foreground/80"
              }`}
            >
              {/* Mode index */}
              <span className="w-4 text-right text-foreground/30 text-[10px]">
                {i + 1}
              </span>

              {/* Frequency */}
              <span className="flex-1">{mode.frequency.toFixed(0)} cm⁻¹</span>

              {/* Symmetry label */}
              {symLabel && (
                <span className="text-[10px] text-foreground/40">{symLabel}</span>
              )}

              {/* IR/Raman badges */}
              <div className="flex gap-0.5">
                {irActive && (
                  <span className="text-[8px] px-1 py-px rounded bg-ir/15 text-ir">
                    IR
                  </span>
                )}
                {ramanActive && (
                  <span className="text-[8px] px-1 py-px rounded bg-raman/15 text-raman">
                    R
                  </span>
                )}
              </div>

              {/* A/B indicator */}
              {isA && (
                <span className="text-[9px] font-bold text-cyan">A</span>
              )}
              {isB && (
                <span className="text-[9px] font-bold text-accent">B</span>
              )}
            </button>
          );
        })}
      </div>
    </TerminalPanel>
  );
}
