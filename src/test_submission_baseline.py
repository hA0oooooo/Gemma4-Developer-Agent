"""Keep the reviewed default configuration identical to the scored baseline."""
import hashlib
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'agent.yaml': '24dca8e255dc52fed7e62555456c77931b675c70254bde4976c76b5bb0cc54d3',
 'configs/sampling.yaml': 'ad0efa7e8a10afa00cd037d3e808eac4bfea3b8eb5d185a4a88081d6b4d69ba9',
 'eval_config.yaml': 'd5d51c6b2597f9a5a256bb7b1fd52b3608a731d76734048872f1ac4fd32b8972',
 'prompts/system.md': 'd8e022e9df86ede0d69d1fdf843a18bbd77be33651c722250d5128dc62170bfc'}


class SubmissionBaselineTests(unittest.TestCase):
    def test_default_has_only_the_four_scored_files(self):
        source = ROOT / "submission"
        actual = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in source.rglob("*") if p.is_file()}
        self.assertEqual(actual, EXPECTED)


if __name__ == "__main__":
    unittest.main()
