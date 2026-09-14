# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_connector_contains_no_dynamic_execution_primitive():
    tree = ast.parse((ROOT / "sumologic_connector.py").read_text())
    forbidden = {"exec", "eval", "compile"}

    calls = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}

    assert calls.isdisjoint(forbidden)


def test_manifest_does_not_accept_custom_message_parser():
    manifest = json.loads((ROOT / "sumologic.json").read_text())

    assert "message_parser" not in manifest["configuration"]


def test_connector_rejects_legacy_parser_values():
    source = (ROOT / "sumologic_connector.py").read_text()

    assert 'get("message_parser")' in source
    assert "Custom message parsers are no longer supported" in source
