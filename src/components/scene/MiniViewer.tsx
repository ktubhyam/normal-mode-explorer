"use client";

import { useRef, useEffect } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { Atoms } from "./Atoms";
import { Bonds } from "./Bonds";
import { MOLECULE_SYMMETRY } from "@/lib/constants";
import type { MoleculeData } from "@/lib/types";

function CameraFit({ molecule }: { molecule: MoleculeData }) {
  const { camera } = useThree();
  const prevMolRef = useRef<string>("");

  useEffect(() => {
    if (molecule.name === prevMolRef.current) return;
    prevMolRef.current = molecule.name;

    const points = molecule.atoms.map((a) => new THREE.Vector3(a.x, a.y, a.z));
    const box = new THREE.Box3().setFromPoints(points);
    const sphere = new THREE.Sphere();
    box.getBoundingSphere(sphere);

    const radius = Math.max(sphere.radius, 1.5);
    const dist = radius * 3.2;

    camera.position.set(dist * 0.6, dist * 0.4, dist);
    camera.lookAt(sphere.center);
    camera.updateProjectionMatrix();
  }, [molecule, camera]);

  return null;
}

interface Props {
  molecule: MoleculeData;
  modeIndex: number;
  label: "A" | "B";
  accentColor: string;
}

export function MiniViewer({ molecule, modeIndex, label, accentColor }: Props) {
  const mode = molecule.modes[modeIndex];
  if (!mode) return null;

  const symmetryData = MOLECULE_SYMMETRY[molecule.name.toLowerCase().replace(/\s+/g, "_")];
  const symmetryLabel = symmetryData?.modeLabels[modeIndex] || mode.symmetry || "—";
  const pointGroup = symmetryData?.pointGroup || molecule.pointGroup || "";

  const irActive = mode.ir_intensity > 0.1;
  const ramanActive = mode.raman_activity > 0.1;
  const activityStr = irActive && ramanActive
    ? "IR + Raman"
    : irActive
      ? "IR"
      : ramanActive
        ? "Raman"
        : "Silent";

  return (
    <div className="flex-1 flex flex-col min-h-0">
      {/* Mode header */}
      <div
        className="flex items-center justify-between px-3 py-2 border-b"
        style={{ borderColor: `${accentColor}33` }}
      >
        <div className="flex items-center gap-2">
          <span
            className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded"
            style={{ background: `${accentColor}22`, color: accentColor }}
          >
            {label}
          </span>
          <span className="text-sm font-mono text-foreground">
            ν = {mode.frequency.toFixed(0)} cm⁻¹
          </span>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-mono">
          {symmetryLabel !== "—" && (
            <span className="text-foreground/60">{symmetryLabel}</span>
          )}
          {pointGroup && (
            <span className="text-foreground/40">{pointGroup}</span>
          )}
          <span
            className="px-1.5 py-0.5 rounded"
            style={{ background: `${accentColor}15`, color: `${accentColor}cc` }}
          >
            {activityStr}
          </span>
        </div>
      </div>

      {/* 3D Canvas */}
      <div className="flex-1 min-h-0">
        <Canvas
          camera={{ position: [0, 0, 6], fov: 50, near: 0.1, far: 100 }}
          gl={{ antialias: true, alpha: true }}
        >
          <color attach="background" args={["#050505"]} />
          <ambientLight intensity={0.6} />
          <directionalLight position={[5, 5, 5]} intensity={0.8} />
          <directionalLight position={[-3, -3, 2]} intensity={0.3} />

          <CameraFit molecule={molecule} />
          <Atoms molecule={molecule} modeIndex={modeIndex} />
          <Bonds molecule={molecule} modeIndex={modeIndex} />

          <OrbitControls enableDamping dampingFactor={0.1} minDistance={2} maxDistance={20} />
        </Canvas>
      </div>
    </div>
  );
}
