# The Stage B refusal tests (CR-IDENTITY-BIND and CR-EXT-UNREVIEWED), verbatim.
# Source: tests/test_public_plugin_packaging.py lines 825-912 at the current Stage B head.
# Extracted rather than paraphrased.

    # ------------------------- 20. the official manifest must BE the release identity (CR-IDENTITY-BIND)
    def test_20_official_name_not_bound_to_the_release_plugin_id_is_refused(self) -> None:
        """A *valid* vendor-shaped name that is not the release identity must be refused.

        The ZIP root directory and the release receipt are named from the release bookkeeping, so an
        official manifest naming a different plugin ships two contradicting identities in one
        artefact. The earlier builder validated the manifest's shape only and accepted this at
        exit 0 (independently reported as CR-IDENTITY-BIND).
        """
        with temp_env() as env:
            ledger = env.freeze()
            doc = env.official_manifest(name="pipd-other-valid-plugin")
            env.write_packaging(ledger, manifest=doc)
            exc = self.assert_refusal("MANIFEST_IDENTITY_MISMATCH", env.build, ledger)
            self.assertIn("pipd-other-valid-plugin", str(exc))
            self.assert_no_zip(env)
            env.write_packaging(ledger)
            self.assertEqual(env.build(ledger)["verdict"], "BUILT")

    def test_20_manifest_version_not_bound_to_the_release_version_is_refused(self) -> None:
        with temp_env() as env:
            ledger = env.freeze()
            env.write_packaging(ledger, manifest=env.official_manifest(version="999.0.0"))
            exc = self.assert_refusal("MANIFEST_VERSION_MISMATCH", env.build, ledger)
            self.assertIn("999.0.0", str(exc))
            self.assert_no_zip(env)

    def test_20_manifest_license_not_bound_to_the_release_license_is_refused(self) -> None:
        with temp_env() as env:
            ledger = env.freeze()
            env.write_packaging(ledger, manifest=env.official_manifest(license="MIT"))
            exc = self.assert_refusal("MANIFEST_LICENSE_MISMATCH", env.build, ledger)
            self.assertIn("MIT", str(exc))
            self.assert_no_zip(env)

    def test_20_a_release_bookkeeping_without_plugin_id_is_refused(self) -> None:
        with temp_env() as env:
            ledger = env.freeze()
            rel = env.release_doc()
            rel.pop("plugin_id")
            env.write_packaging(ledger, release=rel, manifest=env.official_manifest(release=rel))
            self.assert_refusal("RELEASE_IDENTITY_INVALID", env.build, ledger)
            self.assert_no_zip(env)

    # ------------------------- 20. only reviewed extension namespaces (CR-EXT-UNREVIEWED)
    def test_20_unreviewed_extension_namespace_is_refused(self) -> None:
        """An opaque namespace the vendor schema happily accepts must still be refused.

        The locked vendor schema permits arbitrary object-valued reverse-domain namespaces, so
        without this gate unreviewed content travels in the ZIP at exit 0 (independently reported as
        CR-EXT-UNREVIEWED). The owner derivation records authorize SKILL.md transformations only,
        never manifest namespaces.
        """
        with temp_env() as env:
            ledger = env.freeze()
            doc = env.official_manifest()
            doc["extensions"]["com.ao3.unreviewed"] = {"anything": 1}
            env.write_packaging(ledger, manifest=doc)
            exc = self.assert_refusal("EXTENSION_NAMESPACE_UNREVIEWED", env.build, ledger)
            self.assertIn("com.ao3.unreviewed", str(exc))
            self.assertIn("com.openai", str(exc))
            self.assert_no_zip(env)

    def test_20_removing_a_reviewed_namespace_drops_the_interface_is_refused(self) -> None:
        """`extensions` must stay a non-empty object; an empty one is not a valid public manifest."""
        with temp_env() as env:
            ledger = env.freeze()
            env.write_packaging(ledger, manifest=env.official_manifest(extensions={}))
            self.assert_refusal("MANIFEST_EXTENSIONS_INVALID", env.build, ledger)
            self.assert_no_zip(env)

    def test_20_the_reviewed_namespace_set_is_exactly_what_the_gate_allows(self) -> None:
        """Pin the reviewed set: widening it must be a deliberate, reviewed edit, not a drive-by."""
        self.assertEqual(tuple(B.REVIEWED_EXTENSION_NAMESPACES),
                         ("com.openai", B.RELEASE_EXTENSION_KEY))
        with temp_env() as env:
            ledger = env.freeze()
            env.write_packaging(ledger)
            report = env.build(ledger)
            self.assertEqual(report["verdict"], "BUILT")
            infos, members = zip_entries(Path(report["out_zip"]))
            manifest = json.loads(members[f"{PLUGIN_ID}/plugin.json"].decode("utf-8"))
            self.assertEqual(sorted(manifest["extensions"]),
                             sorted(B.REVIEWED_EXTENSION_NAMESPACES))


if __name__ == "__main__":
    unittest.main()
