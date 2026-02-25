"use client";

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useExplorerStore } from "@/lib/store";
import { BOND_RADIUS, VISUAL_FREQ } from "@/lib/constants";
import type { MoleculeData } from "@/lib/types";

interface Props {
  molecule: MoleculeData;
  modeIndex: number;
}

const UP = new THREE.Vector3(0, 1, 0);

export function Bonds({ molecule, modeIndex }: Props) {
  const groupRef = useRef<THREE.Group>(null);
  const meshRefs = useRef<(THREE.Mesh | null)[]>([]);

  const tmpA = useMemo(() => new THREE.Vector3(), []);
  const tmpB = useMemo(() => new THREE.Vector3(), []);
  const tmpDir = useMemo(() => new THREE.Vector3(), []);
  const tmpQuat = useMemo(() => new THREE.Quaternion(), []);

  useFrame(({ clock }) => {
    if (!molecule.modes.length || !molecule.bonds.length) return;

    const { isPlaying, speed, amplitude } = useExplorerStore.getState();
    const mode = molecule.modes[modeIndex];
    if (!mode) return;

    const t = clock.getElapsedTime();
    const phase = isPlaying ? Math.sin(2 * Math.PI * VISUAL_FREQ * speed * t) : 0;

    molecule.bonds.forEach((bond, bi) => {
      const mesh = meshRefs.current[bi];
      if (!mesh) return;

      const atomA = molecule.atoms[bond.atom1];
      const atomB = molecule.atoms[bond.atom2];
      const dispA = mode.displacements[bond.atom1];
      const dispB = mode.displacements[bond.atom2];

      tmpA.set(
        atomA.x + amplitude * dispA[0] * phase,
        atomA.y + amplitude * dispA[1] * phase,
        atomA.z + amplitude * dispA[2] * phase,
      );
      tmpB.set(
        atomB.x + amplitude * dispB[0] * phase,
        atomB.y + amplitude * dispB[1] * phase,
        atomB.z + amplitude * dispB[2] * phase,
      );

      mesh.position.lerpVectors(tmpA, tmpB, 0.5);

      tmpDir.subVectors(tmpB, tmpA);
      const length = tmpDir.length();
      tmpDir.normalize();
      tmpQuat.setFromUnitVectors(UP, tmpDir);
      mesh.quaternion.copy(tmpQuat);
      mesh.scale.set(1, length, 1);
    });
  });

  return (
    <group ref={groupRef}>
      {molecule.bonds.map((_, i) => (
        <mesh
          key={i}
          ref={(el) => {
            meshRefs.current[i] = el;
          }}
        >
          <cylinderGeometry args={[BOND_RADIUS, BOND_RADIUS, 1, 8]} />
          <meshStandardMaterial color="#555555" roughness={0.5} metalness={0.1} />
        </mesh>
      ))}
    </group>
  );
}
