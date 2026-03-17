"""
SCIM-O9Z Command Line Interface
================================
Run as: python -m scim_o9z [command] [options]
Or after install: scim-o9z [command] [options]
"""

import argparse
import sys
import json
from scim_o9z import SCIM_BANNER, __version__


def main():
    print(SCIM_BANNER)

    parser = argparse.ArgumentParser(
        prog="scim-o9z",
        description="SCIM-O9Z: Counter-architecture to O9A/764/The Com harm networks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  scim-o9z scan --target "some text or domain to analyze"
  scim-o9z scan --domain example.com
  scim-o9z scan --entity "O9A nexion"
  scim-o9z quick --target "insight role vindex"
  scim-o9z hden --list
  scim-o9z vectors --network o9a
  scim-o9z corporate --list-cases
  scim-o9z merkle --seal output.json
  scim-o9z adinkra --symbol sankofa

Author: Memory-Keeper (Adam Boisclair) | Family of Coexistence
Website: aibirthingcenter.com | License: CC BY-NC-SA 4.0
        """,
    )

    parser.add_argument("--version", action="version", version=f"SCIM-O9Z {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === SCAN command ===
    scan_parser = subparsers.add_parser("scan", help="Run full SCIM-O9Z analysis")
    scan_parser.add_argument("--target", "-t", help="Text, domain, or entity to analyze")
    scan_parser.add_argument("--domain", "-d", help="Domain name to analyze via CT logs")
    scan_parser.add_argument("--entity", "-e", help="Named entity to analyze")
    scan_parser.add_argument("--file", "-f", help="File containing text to analyze")
    scan_parser.add_argument("--output", "-o", help="Output JSON file path")
    scan_parser.add_argument("--markdown", "-m", help="Output Markdown file path")
    scan_parser.add_argument("--no-ct", action="store_true", help="Skip CT log scanning")
    scan_parser.add_argument("--no-corporate", action="store_true", help="Skip corporate harm check")
    scan_parser.add_argument("--deep", action="store_true", help="Enable deep scanning")

    # === QUICK command ===
    quick_parser = subparsers.add_parser("quick", help="Quick scan (HDEN + harm vectors only)")
    quick_parser.add_argument("--target", "-t", required=True, help="Target to scan")

    # === HDEN command ===
    hden_parser = subparsers.add_parser("hden", help="HDEN taxonomy tools")
    hden_parser.add_argument("--list", action="store_true", help="List all HDEN network types")
    hden_parser.add_argument("--classify", "-c", help="Classify a target")
    hden_parser.add_argument("--profile", "-p", help="Get profile of a network type")

    # === VECTORS command ===
    vec_parser = subparsers.add_parser("vectors", help="Harm vector tools")
    vec_parser.add_argument("--list", action="store_true", help="List all harm vectors")
    vec_parser.add_argument("--network", "-n", help="Filter by network (o9a, 764, ai, corporate)")
    vec_parser.add_argument("--dimension", "-d", help="Filter by SCIM dimension")
    vec_parser.add_argument("--minor-risk", action="store_true", help="Show minor-risk vectors")
    vec_parser.add_argument("--immediate", action="store_true", help="Show immediate-risk vectors")

    # === CORPORATE command ===
    corp_parser = subparsers.add_parser("corporate", help="Corporate harm tracker")
    corp_parser.add_argument("--list-cases", action="store_true", help="List all documented cases")
    corp_parser.add_argument("--check", "-c", help="Check a company/target")
    corp_parser.add_argument("--scrubba-dub", action="store_true", help="Show Scrubba Dub cases")
    corp_parser.add_argument("--deaths", action="store_true", help="Show death cases")

    # === MERKLE command ===
    merkle_parser = subparsers.add_parser("merkle", help="Quantum Merkle tree operations")
    merkle_parser.add_argument("--seal", help="Seal a JSON findings file")
    merkle_parser.add_argument("--verify", help="Verify a Merkle root against a findings file")
    merkle_parser.add_argument("--output", "-o", help="Output file for sealed tree")

    # === ADINKRA command ===
    adinkra_parser = subparsers.add_parser("adinkra", help="Adinkra error correction tools")
    adinkra_parser.add_argument("--symbol", "-s", help="Get info on an Adinkra symbol")
    adinkra_parser.add_argument("--list", action="store_true", help="List all Adinkra symbols")
    adinkra_parser.add_argument("--love-signal", action="store_true", help="Display Universal Love Signal")
    adinkra_parser.add_argument("--principle", action="store_true", help="Display Family of Coexistence principle")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # === Execute commands ===
    if args.command == "scan":
        _cmd_scan(args)
    elif args.command == "quick":
        _cmd_quick(args)
    elif args.command == "hden":
        _cmd_hden(args)
    elif args.command == "vectors":
        _cmd_vectors(args)
    elif args.command == "corporate":
        _cmd_corporate(args)
    elif args.command == "merkle":
        _cmd_merkle(args)
    elif args.command == "adinkra":
        _cmd_adinkra(args)


def _cmd_scan(args):
    from scim_o9z.core.engine import SCIMEngine
    engine = SCIMEngine()

    target = args.target or args.domain or args.entity
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            target = f.read()

    if not target:
        print("[ERROR] Provide --target, --domain, --entity, or --file")
        sys.exit(1)

    target_type = "auto"
    if args.domain:
        target_type = "domain"
    elif args.entity:
        target_type = "entity"

    report = engine.analyze(
        target=target,
        target_type=target_type,
        scan_ct_logs=not args.no_ct,
        check_corporate=not args.no_corporate,
        deep_scan=args.deep,
    )

    report.print_summary()

    if args.output:
        report.save(args.output)

    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(report.to_markdown())
        print(f"[SCIM-O9Z] Markdown report saved to: {args.markdown}")


def _cmd_quick(args):
    from scim_o9z.core.engine import SCIMEngine
    engine = SCIMEngine()
    result = engine.quick_scan(args.target)
    print(json.dumps(result, indent=2))


def _cmd_hden(args):
    from scim_o9z.hden.taxonomy import HDENTaxonomy
    hden = HDENTaxonomy()

    if args.list:
        print("\nHDEN Network Types:")
        for name in hden.list_all_networks():
            profile = hden.get_network_profile(name)
            print(f"  {name:<35} Severity: {profile.severity}/5 | {profile.name}")
    elif args.classify:
        result = hden.classify(args.classify)
        print(json.dumps(result, indent=2))
    elif args.profile:
        profile = hden.get_network_profile(args.profile)
        if profile:
            print(f"\n{profile.name}")
            print(f"Description: {profile.description}")
            print(f"Severity: {profile.severity}/5")
            print(f"Legal Status: {profile.legal_status}")
            print(f"Harm Types: {', '.join(profile.harm_types)}")
        else:
            print(f"Network type '{args.profile}' not found.")


def _cmd_vectors(args):
    from scim_o9z.harm_vectors.o9a import O9AHarmVectors
    vectors = O9AHarmVectors()

    if args.minor_risk:
        found = vectors.get_minor_risk_vectors()
    elif args.immediate:
        found = vectors.get_immediate_risk_vectors()
    elif args.network:
        found = vectors.get_vectors_by_network(args.network)
    elif args.dimension:
        found = vectors.get_vectors_by_dimension(args.dimension)
    else:
        found = list(vectors.vectors.keys())

    print(f"\nHarm Vectors ({len(found)} found):")
    for v in found:
        detail = vectors.get_vector_detail(v)
        print(f"  {v:<35} [{detail.network_origin.upper()}] dim:{detail.scim_dimension_attacked} sev:{detail.severity}")


def _cmd_corporate(args):
    from scim_o9z.corporate.tracker import CorporateHarmTracker
    tracker = CorporateHarmTracker()

    if args.list_cases:
        cases = tracker.get_all_cases()
        print(f"\nCorporate Harm Cases ({len(cases)} documented):")
        for c in cases:
            print(f"  {c['case_id']:<12} {c['company']:<30} [{c['case_type']}] ({c['year']})")
    elif args.check:
        result = tracker.check(args.check)
        print(json.dumps(result, indent=2))
    elif args.scrubba_dub:
        cases = tracker.get_scrubba_dub_cases()
        print(f"\nProject Scrubba Dub Cases ({len(cases)}):")
        for c in cases:
            print(f"  {c.case_id}: {c.company} — {c.harm_description[:100]}...")
    elif args.deaths:
        cases = tracker.get_death_cases()
        print(f"\nDeath Cases ({len(cases)}):")
        for c in cases:
            print(f"  {c.case_id}: {c.company} | {c.victim_category}")
            print(f"    {c.harm_description[:150]}...")


def _cmd_merkle(args):
    from scim_o9z.merkle.tree import QuantumMerkleTree

    if args.seal:
        with open(args.seal, "r", encoding="utf-8") as f:
            data = json.load(f)

        tree = QuantumMerkleTree()
        for key, value in data.items():
            tree.add_evidence(value, data_type=key, summary=f"Finding: {key}")

        seal = tree.seal()
        print(f"\nMerkle Tree Sealed:")
        print(f"  Root: {seal['merkle_root']}")
        print(f"  Leaves: {seal['total_leaves']}")
        print(f"  Algorithm: {seal['hash_algorithm']}")
        print(f"\n{seal['scrubba_dub_note']}")

        if args.output:
            tree.save(args.output)


def _cmd_adinkra(args):
    from scim_o9z.adinkra.codes import AdinkraEngine, ADINKRA_SYMBOLS
    engine = AdinkraEngine()

    if args.list:
        print("\nAdinkra Symbols:")
        for name, symbol in ADINKRA_SYMBOLS.items():
            print(f"  {symbol['visual']} {symbol['name']:<30} {symbol['meaning']}")
    elif args.symbol:
        symbol = engine.get_symbol(args.symbol)
        if symbol:
            print(f"\n{symbol['visual']} {symbol['name']}")
            print(f"Meaning: {symbol['meaning']}")
            print(f"SCIM Function: {symbol['scim_function']}")
        else:
            print(f"Symbol '{args.symbol}' not found. Use --list to see all symbols.")
    elif args.love_signal:
        signal = engine.get_love_signal()
        print("\n=== UNIVERSAL LOVE SIGNAL ===")
        print(f"Principle: {signal['principle']}")
        print(f"Bridge: {signal['bridge']}")
        for option, desc in signal['options'].items():
            print(f"  {option}: {desc}")
        print(f"\n{signal['note']}")
    elif args.principle:
        print(f"\n{engine.family_of_coexistence_principle()}")


if __name__ == "__main__":
    main()