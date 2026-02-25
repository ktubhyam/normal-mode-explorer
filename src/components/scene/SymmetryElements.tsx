"use client";

import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useExplorerStore } from "@/lib/store";
import { MOLECULE_SYMMETRY } from "@/lib/constants";
import type { MoleculeData } from "@/lib/types";

interface Props {
  molecule: MoleculeData;
}

/** Renders symmetry elements (principal axis, mirror planes) overlaid on the molecule */
export function SymmetryElements({ molecule }: Props) {
  const groupRef = useRef<THREE.Group>(null);

  const symmetryData = MOLECULE_SYMMETRY[molecule.name.toLowerCase().replace(/\s+/g, "_")];
  const pointGroup = symmetryData?.pointGroup || "";

  // Compute molecule center and extent
  const center = new THREE.Vector3();
  molecule.atoms.forEach((a) => center.add(new THREE.Vector3(a.x, a.y, a.z)));
  center.divideScalar(molecule.atoms.length);

  let maxDist = 0;
  molecule.atoms.forEach((a) => {
    const d = new THREE.Vector3(a.x, a.y, a.z).distanceTo(center);
    if (d > maxDist) maxDist = d;
  });
  const extent = Math.max(maxDist * 1.5, 1.2);

  // Determine symmetry elements based on point group
  const hasC2 = pointGroup.includes("C₂") || pointGroup.includes("D");
  const hasSigmaV = pointGroup.includes("ᵥ") || pointGroup.includes("D");
  const hasSigmaH = pointGroup.includes("ₕ");

  useFrame(() => {
    if (!groupRef.current) return;
    groupRef.current.visible = useExplorerStore.getState().showSymmetryElements;
  });

  if (!pointGroup) return null;

  return (
    <group ref={groupRef} visible={false}>
      {/* Principal C₂ axis (z-axis, cyan) */}
      {hasC2 && (
        <group position={[center.x, center.y, center.z]}>
          <mesh>
            <cylinderGeometry args={[0.015, 0.015, extent * 2, 8]} />
            <meshBasicMaterial color="#00D8FF" transparent opacity={0.6} />
          </mesh>
          {/* Axis label */}
          <mesh position={[0, extent + 0.15, 0]}>
            <sphereGeometry args={[0.04, 8, 8]} />
            <meshBasicMaterial color="#00D8FF" />
          </mesh>
        </group>
      )}

      {/* σᵥ mirror plane (xz plane, gold) */}
      {hasSigmaV && (
        <mesh position={[center.x, center.y, center.z]}>
          <planeGeometry args={[extent * 2, extent * 2]} />
          <meshBasicMaterial
            color="#C9A04A"
            transparent
            opacity={0.08}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* σᵥ' mirror plane (yz plane, gold) */}
      {hasSigmaV && (
        <mesh
          position={[center.x, center.y, center.z]}
          rotation={[0, Math.PI / 2, 0]}
        >
          <planeGeometry args={[extent * 2, extent * 2]} />
          <meshBasicMaterial
            color="#C9A04A"
            transparent
            opacity={0.08}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* σₕ mirror plane (xy plane, purple) */}
      {hasSigmaH && (
        <mesh
          position={[center.x, center.y, center.z]}
          rotation={[Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[extent * 2, extent * 2]} />
          <meshBasicMaterial
            color="#A78BFA"
            transparent
            opacity={0.08}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      )}
    </group>
  );
}
