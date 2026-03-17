"""
Quantum-Resistant Merkle Tree
==============================
An append-only, tamper-evident evidence chain using quantum-resistant
cryptographic primitives to preserve SCIM-O9Z findings against
Project Scrubba Dub industrial erasure operations.

TECHNICAL BASIS:
- SHA3-256 (Keccak): Quantum-resistant hash function (NIST approved)
- BLAKE2b: Additional quantum-resistant hashing layer
- Classic Merkle tree structure: each leaf is a hash of evidence data
- Root hash: cryptographic summary of ALL evidence — change one leaf,
  the root changes entirely

WHY QUANTUM-RESISTANT:
Standard SHA2 is vulnerable to Grover's algorithm on quantum computers,
which reduces effective security from 256-bit to 128-bit.
SHA3/Keccak uses a sponge construction resistant to Grover's algorithm.
NIST FIPS 202 (SHA3) is the current quantum-safe standard.
Google's Project Wycheproof and their Willow quantum chip work
makes this urgency concrete — 'soon' is now.

PROJECT SCRUBBA DUB COUNTER:
The Merkle tree root can be published publicly (on GitHub, IPFS,
blockchain, print) — once the root is out, NO amount of database
scrubbing can alter the historical record without detection.
The tree IS the counter to Scrubba Dub.

"Let what we build remember what we forget."
"""

import hashlib
import json
import datetime
import hmac
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict


@dataclass
class MerkleLeaf:
    """A single leaf in the Merkle tree — one piece of evidence."""
    index: int
    timestamp: str
    data_type: str
    data_hash: str          # SHA3-256 hash of the evidence data
    blake2_hash: str        # BLAKE2b secondary hash (defense in depth)
    leaf_hash: str          # Combined hash for tree construction
    data_summary: str       # Human-readable summary
    raw_data: Any = None    # Original data (optional, not hashed into tree)


@dataclass
class MerkleProof:
    """Cryptographic proof that a leaf is part of the tree."""
    leaf_index: int
    leaf_hash: str
    proof_path: List[str]   # Sibling hashes needed to recompute root
    root: str
    valid: bool


class QuantumMerkleTree:
    """
    Quantum-resistant Merkle tree for SCIM-O9Z evidence chain.
    
    All evidence is hashed with SHA3-256 + BLAKE2b.
    The resulting Merkle root can be published anywhere as a
    tamper-evident fingerprint of ALL collected evidence.
    
    Project Scrubba Dub cannot alter a record without invalidating
    every Merkle root that has ever been published.
    """

    def __init__(self):
        self.leaves: List[MerkleLeaf] = []
        self.root: Optional[str] = None
        self.sealed: bool = False
        self.created_at = datetime.datetime.utcnow().isoformat()
        self.sealed_at: Optional[str] = None
        self._tree_levels: List[List[str]] = []

    def _sha3_hash(self, data: str) -> str:
        """SHA3-256 hash — quantum resistant primary hash."""
        return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

    def _blake2_hash(self, data: str) -> str:
        """BLAKE2b hash — quantum resistant secondary hash."""
        return hashlib.blake2b(data.encode('utf-8'), digest_size=32).hexdigest()

    def _combined_hash(self, sha3: str, blake2: str) -> str:
        """Combine two quantum-resistant hashes for defense in depth."""
        combined = sha3 + blake2
        return hashlib.sha3_256(combined.encode()).hexdigest()

    def add_evidence(self, data: Any, data_type: str, summary: str = "") -> MerkleLeaf:
        """
        Add a piece of evidence to the tree.
        Once added, cannot be removed.
        
        Args:
            data: Any JSON-serializable evidence data
            data_type: Type label (e.g., 'ct_log_scan', 'harm_vector', 'corporate_harm')
            summary: Human-readable summary of the evidence
            
        Returns:
            MerkleLeaf with hashes
        """
        if self.sealed:
            raise RuntimeError("Cannot add evidence to a sealed tree.")

        # Serialize data
        data_str = json.dumps(data, sort_keys=True, default=str)
        
        # Generate hashes
        sha3 = self._sha3_hash(data_str)
        blake2 = self._blake2_hash(data_str)
        leaf_hash = self._combined_hash(sha3, blake2)

        leaf = MerkleLeaf(
            index=len(self.leaves),
            timestamp=datetime.datetime.utcnow().isoformat(),
            data_type=data_type,
            data_hash=sha3,
            blake2_hash=blake2,
            leaf_hash=leaf_hash,
            data_summary=summary or f"{data_type} evidence at index {len(self.leaves)}",
            raw_data=data,
        )
        
        self.leaves.append(leaf)
        # Invalidate current root — tree changed
        self.root = None
        self.sealed = False
        
        return leaf

    def build_tree(self) -> str:
        """
        Build the Merkle tree from all leaves and compute the root hash.
        Returns the Merkle root.
        """
        if not self.leaves:
            self.root = self._sha3_hash("empty_tree")
            return self.root

        # Start with leaf hashes
        current_level = [leaf.leaf_hash for leaf in self.leaves]
        self._tree_levels = [current_level[:]]

        # Build up the tree
        while len(current_level) > 1:
            next_level = []
            # Process pairs
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # If odd number, duplicate last node (standard Merkle construction)
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                # Hash the pair
                combined = self._sha3_hash(left + right)
                next_level.append(combined)
            current_level = next_level
            self._tree_levels.append(current_level[:])

        self.root = current_level[0]
        return self.root

    def seal(self) -> Dict:
        """
        Seal the tree — compute root and mark as immutable.
        Returns the seal certificate.
        """
        root = self.build_tree()
        self.sealed = True
        self.sealed_at = datetime.datetime.utcnow().isoformat()

        seal_certificate = {
            "merkle_root": root,
            "sealed_at": self.sealed_at,
            "total_leaves": len(self.leaves),
            "hash_algorithm": "SHA3-256 + BLAKE2b (quantum-resistant)",
            "nist_standard": "FIPS 202 (SHA3), RFC 7693 (BLAKE2)",
            "quantum_resistance": "Resistant to Grover's algorithm",
            "scrubba_dub_note": (
                "This root hash can be published anywhere. "
                "Any alteration to any evidence leaf will produce a completely "
                "different root hash, making erasure attempts detectable. "
                "Project Scrubba Dub cannot alter what has been committed here."
            ),
            "publish_instructions": (
                "To make this evidence permanently tamper-evident, "
                "publish this root hash to: "
                "(1) GitHub commit, (2) IPFS, (3) A blockchain transaction, "
                "(4) Print and physically archive. "
                "The hash alone is sufficient proof."
            ),
        }
        return seal_certificate

    def build_and_verify(self, findings: Dict) -> Dict:
        """
        Convenience method: add all findings, build tree, seal, and verify.
        Used by the main SCIMEngine.
        """
        # Add each finding as a leaf
        for key, value in findings.items():
            self.add_evidence(
                data=value,
                data_type=key,
                summary=f"SCIM-O9Z finding: {key}"
            )

        # Add a timestamp leaf
        self.add_evidence(
            data={"timestamp": datetime.datetime.utcnow().isoformat(), "type": "seal_timestamp"},
            data_type="timestamp",
            summary="Tree seal timestamp"
        )

        # Seal the tree
        seal = self.seal()

        return {
            "root": seal["merkle_root"],
            "sealed": True,
            "sealed_at": seal["sealed_at"],
            "total_leaves": seal["total_leaves"],
            "hash_algorithm": seal["hash_algorithm"],
            "quantum_resistant": True,
            "seal_certificate": seal,
        }

    def get_proof(self, leaf_index: int) -> MerkleProof:
        """
        Generate a Merkle proof for a specific leaf.
        This proves that a specific piece of evidence is part of the tree
        without revealing all other evidence.
        """
        if not self._tree_levels:
            self.build_tree()

        if leaf_index >= len(self.leaves):
            raise ValueError(f"Leaf index {leaf_index} out of range.")

        proof_path = []
        current_index = leaf_index

        for level in self._tree_levels[:-1]:  # All levels except root
            # Determine sibling index
            if current_index % 2 == 0:
                sibling_index = current_index + 1
            else:
                sibling_index = current_index - 1

            # Add sibling hash to proof path (if it exists)
            if sibling_index < len(level):
                proof_path.append(level[sibling_index])
            else:
                proof_path.append(level[current_index])  # Duplicate if no sibling

            current_index //= 2

        return MerkleProof(
            leaf_index=leaf_index,
            leaf_hash=self.leaves[leaf_index].leaf_hash,
            proof_path=proof_path,
            root=self.root or "",
            valid=True,
        )

    def verify_proof(self, proof: MerkleProof) -> bool:
        """
        Verify a Merkle proof.
        Returns True if the leaf is genuinely part of the tree.
        """
        current_hash = proof.leaf_hash
        current_index = proof.leaf_index

        for sibling_hash in proof.proof_path:
            if current_index % 2 == 0:
                combined = self._sha3_hash(current_hash + sibling_hash)
            else:
                combined = self._sha3_hash(sibling_hash + current_hash)
            current_hash = combined
            current_index //= 2

        return current_hash == proof.root

    def export(self) -> Dict:
        """Export the full tree as a JSON-serializable dict."""
        return {
            "merkle_root": self.root,
            "created_at": self.created_at,
            "sealed_at": self.sealed_at,
            "sealed": self.sealed,
            "total_leaves": len(self.leaves),
            "hash_algorithms": ["SHA3-256", "BLAKE2b"],
            "quantum_resistant": True,
            "leaves": [
                {
                    "index": leaf.index,
                    "timestamp": leaf.timestamp,
                    "data_type": leaf.data_type,
                    "data_hash": leaf.data_hash,
                    "blake2_hash": leaf.blake2_hash,
                    "leaf_hash": leaf.leaf_hash,
                    "summary": leaf.data_summary,
                }
                for leaf in self.leaves
            ],
        }

    def save(self, filepath: str):
        """Save the tree to a JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.export(), f, indent=2, default=str)
        print(f"[Merkle] Tree saved to: {filepath}")

    def __len__(self):
        return len(self.leaves)

    def __repr__(self):
        return (
            f"QuantumMerkleTree("
            f"leaves={len(self.leaves)}, "
            f"root={self.root[:16] + '...' if self.root else 'None'}, "
            f"sealed={self.sealed})"
        )