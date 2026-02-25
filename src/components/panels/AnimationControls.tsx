"use client";

import { useExplorerStore } from "@/lib/store";
import { TerminalPanel } from "../ui/TerminalPanel";

export function AnimationControls() {
  const isPlaying = useExplorerStore((s) => s.isPlaying);
  const speed = useExplorerStore((s) => s.speed);
  const amplitude = useExplorerStore((s) => s.amplitude);
  const togglePlaying = useExplorerStore((s) => s.togglePlaying);
  const setSpeed = useExplorerStore((s) => s.setSpeed);
  const setAmplitude = useExplorerStore((s) => s.setAmplitude);

  return (
    <TerminalPanel title="Animation">
      <div className="p-3 space-y-3">
        {/* Play/Pause */}
        <button
          onClick={togglePlaying}
          className="w-full flex items-center justify-center gap-2 py-1.5 rounded bg-surface-2 border border-border hover:border-border-bright transition-colors text-xs font-mono text-foreground/70 hover:text-foreground"
        >
          {isPlaying ? (
            <>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <rect x="6" y="4" width="4" height="16" rx="1" />
                <rect x="14" y="4" width="4" height="16" rx="1" />
              </svg>
              Pause
            </>
          ) : (
            <>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5,3 19,12 5,21" />
              </svg>
              Play
            </>
          )}
          <span className="text-foreground/25 text-[10px]">[Space]</span>
        </button>

        {/* Speed */}
        <div className="space-y-1">
          <div className="flex items-center justify-between text-[10px] font-mono">
            <span className="text-foreground/40">Speed</span>
            <span className="text-foreground/60">{speed.toFixed(1)}×</span>
          </div>
          <input
            type="range"
            min={0.1}
            max={3}
            step={0.1}
            value={speed}
            onChange={(e) => setSpeed(parseFloat(e.target.value))}
          />
        </div>

        {/* Amplitude */}
        <div className="space-y-1">
          <div className="flex items-center justify-between text-[10px] font-mono">
            <span className="text-foreground/40">Amplitude</span>
            <span className="text-foreground/60">{amplitude.toFixed(1)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={2}
            step={0.1}
            value={amplitude}
            onChange={(e) => setAmplitude(parseFloat(e.target.value))}
          />
        </div>
      </div>
    </TerminalPanel>
  );
}
