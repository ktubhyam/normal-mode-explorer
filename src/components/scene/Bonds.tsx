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

// Strain colors: compressed = warm, stretched = cool
const STRAIN_COMPRESSED = new THREE.Color("#FF4444");
const STRAIN_NEUTRAL = new THREE.Color("#555555");
const STRAIN_STRETCHED = new THREE.Color("#4488FF");
const tmpStrainColor = new THREE.Color();

export function Bonds({ molecule, modeIndex }: Props) {
  const groupRef = useRef<THREE.Group>(null);
  const meshRefs = useRef<(THREE.Mesh | null)[]>([]);
  const matRefs = useRef<(THREE.MeshStandardMaterial | null)[]>([]);

  const tmpA = useMemo(() => new THREE.Vector3(), []);
  const tmpB = useMemo(() => new THREE.Vector3(), []);
  const tmpDir = useMemo(() => new THREE.Vector3(), []);
  const tmpQuat = useMemo(() => new THREE.Quaternion(), []);

  // Precompute rest lengths for strain coloring
  const restLengths = useMemo(() => {
    return molecule.bonds.map((bond) => {
      const a = molecule.atoms[bond.atom1];
      const b = molecule.atoms[bond.atom2];
      return Math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2);
    });
  }, [molecule]);

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

      // Strain coloring: compare current length to rest length
      const mat = matRefs.current[bi];
      if (mat && restLengths[bi]) {
        const strain = (length - restLengths[bi]) / restLengths[bi]; // negative = compressed, positive = stretched
        const clampedStrain = Math.max(-1, Math.min(1, strain * 8)); // amplify for visibility

        if (clampedStrain < 0) {
          tmpStrainColor.copy(STRAIN_NEUTRAL).lerp(STRAIN_COMPRESSED, -clampedStrain);
        } else {
          tmpStrainColor.copy(STRAIN_NEUTRAL).lerp(STRAIN_STRETCHED, clampedStrain);
        }
        mat.color.copy(tmpStrainColor);
        mat.emissive.copy(tmpStrainColor);
        mat.emissiveIntensity = Math.abs(clampedStrain) * 0.2;
      }
    });
  });

  return (
    <group ref={groupRef}>
      {molecule.bonds.map((_, i) => (
        <mesh
          key={i}
          ref={(el) => { meshRefs.current[i] = el; }}
        >
          <cylinderGeometry args={[BOND_RADIUS, BOND_RADIUS, 1, 8]} />
          <meshStandardMaterial
            ref={(el) => { matRefs.current[i] = el; }}
            color="#555555"
            roughness={0.4}
            metalness={0.1}
          />
        </mesh>
      ))}
    </group>
  );
}
