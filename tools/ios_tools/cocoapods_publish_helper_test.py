#!/usr/bin/env python3
# Copyright 2026 The Lynx Authors. All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree.

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cocoapods_publish_helper as helper


class CocoapodsPublishHelperTest(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.cwd)
        self.temp_dir.cleanup()

    def write_podspec_json(self, component, content):
        with open(f'{component}.podspec.json', 'w', encoding='utf8') as f:
            json.dump(content, f)

    def read_podspec_json(self, component):
        with open(f'{component}.podspec.json', 'r', encoding='utf8') as f:
            return json.load(f)

    def test_use_local_pod_source_keeps_http_source_format(self):
        self.write_podspec_json('Lynx', {
            'version': '1.2.3',
            'source': {'git': 'https://example.com/old.git'},
        })

        helper.use_local_pod_source('Lynx')

        content = self.read_podspec_json('Lynx')
        self.assertEqual(
            content['source'],
            {'http': f'file:{os.getcwd()}/Lynx-1.2.3.zip'},
        )

    def test_use_git_pod_source_writes_commit_source_and_preserves_prepare_command(self):
        self.write_podspec_json('Lynx', {
            'version': '1.2.3',
            'source': {'http': 'https://example.com/Lynx.zip'},
            'prepare_command': 'python3 tools/js_tools/build.py --platform ios',
        })

        helper.use_git_pod_source(
            'Lynx',
            'https://github.com/lynx-family/lynx.git',
            'commit',
            'abcdef123456',
        )

        content = self.read_podspec_json('Lynx')
        self.assertEqual(content['source'], {
            'git': 'https://github.com/lynx-family/lynx.git',
            'commit': 'abcdef123456',
        })
        self.assertEqual(
            content['prepare_command'],
            'python3 tools/js_tools/build.py --platform ios',
        )

    def test_missing_git_source_ref_fails_with_clear_error(self):
        with self.assertRaisesRegex(ValueError, '--git-source-ref is required'):
            helper.validate_git_source_options('commit', '')

    def test_zip_source_type_accepts_empty_git_options(self):
        helper.validate_source_type_options('zip', '', '', '')

    def test_missing_git_source_url_fails_with_clear_error(self):
        with self.assertRaisesRegex(ValueError, '--git-source-url is required'):
            helper.validate_source_type_options('git', None, 'commit', 'abcdef123456')

    def test_missing_git_source_ref_type_fails_with_clear_error(self):
        with self.assertRaisesRegex(ValueError, '--git-source-ref-type is required'):
            helper.validate_source_type_options(
                'git',
                'https://github.com/lynx-family/lynx.git',
                None,
                'abcdef123456',
            )


if __name__ == '__main__':
    unittest.main()
