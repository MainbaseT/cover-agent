# Generated by CodiumAI

import pytest
import yaml
from yaml.scanner import ScannerError

from cover_agent.utils import load_yaml


class TestLoadYaml:
    #  Tests that load_yaml loads a valid YAML string
    def test_load_valid_yaml(self):
        yaml_str = "name: John Smith\nage: 35"
        expected_output = {"name": "John Smith", "age": 35}
        assert load_yaml(yaml_str) == expected_output

    def test_load_invalid_yaml1(self):
        yaml_str = '''\
PR Analysis:
  Main theme: Enhancing the `/describe` command prompt by adding title and description
  Type of PR: Enhancement
  Relevant tests: No
  Focused PR: Yes, the PR is focused on enhancing the `/describe` command prompt.

PR Feedback:
  General suggestions: The PR seems to be well-structured and focused on a specific enhancement. However, it would be beneficial to add tests to ensure the new feature works as expected.
  Code feedback:
    - relevant file: pr_agent/settings/pr_description_prompts.toml
      suggestion: Consider using a more descriptive variable name than 'user' for the command prompt. A more descriptive name would make the code more readable and maintainable. [medium]
      relevant line: user="""PR Info: aaa
  Security concerns: No'''
        with pytest.raises(ScannerError):
            yaml.safe_load(yaml_str)

        expected_output = {
            "PR Analysis": {
                "Main theme": "Enhancing the `/describe` command prompt by adding title and description",
                "Type of PR": "Enhancement",
                "Relevant tests": False,
                "Focused PR": "Yes, the PR is focused on enhancing the `/describe` command prompt.",
            },
            "PR Feedback": {
                "General suggestions": "The PR seems to be well-structured and focused on a specific enhancement. However, it would be beneficial to add tests to ensure the new feature works as expected.",
                "Code feedback": [
                    {
                        "relevant file": "pr_agent/settings/pr_description_prompts.toml",
                        "suggestion": "Consider using a more descriptive variable name than 'user' for the command prompt. A more descriptive name would make the code more readable and maintainable. [medium]",
                        "relevant line": 'user="""PR Info: aaa',
                    }
                ],
                "Security concerns": False,
            },
        }
        assert (
            load_yaml(
                yaml_str,
                keys_fix_yaml=[
                    "relevant line:",
                    "suggestion content:",
                    "relevant file:",
                    "existing code:",
                    "improved code:",
                ],
            )
            == expected_output
        )

    def test_load_invalid_yaml2(self):
        yaml_str = """\
- relevant file: src/app.py:
  suggestion content: The print statement is outside inside the if __name__ ==: \
"""
        with pytest.raises(ScannerError):
            yaml.safe_load(yaml_str)

        expected_output = [
            {
                "relevant file": "src/app.py:",
                "suggestion content": "The print statement is outside inside the if __name__ ==:",
            }
        ]
        assert (
            load_yaml(
                yaml_str,
                keys_fix_yaml=[
                    "relevant line:",
                    "suggestion content:",
                    "relevant file:",
                    "existing code:",
                    "improved code:",
                ],
            )
            == expected_output
        )


# auto-generated by cover agent
    def test_try_fix_yaml_snippet_extraction(self):
        from cover_agent.utils import try_fix_yaml

        yaml_str = "```yaml\nname: John Smith\nage: 35\n```"
        expected_output = {"name": "John Smith", "age": 35}
        assert try_fix_yaml(yaml_str) == expected_output


    def test_try_fix_yaml_remove_all_lines(self):
        from cover_agent.utils import try_fix_yaml

        yaml_str = "language: python\nname: John Smith\nage: 35\ninvalid_line"
        expected_output = {"language": "python", "name": "John Smith", "age": 35}
        assert try_fix_yaml(yaml_str) == expected_output


    def test_try_fix_yaml_llama3_8b(self):
        from cover_agent.utils import try_fix_yaml

        yaml_str = """\
here is the response:

language: python
new_tests:
- test_behavior: |
    aaa
  test_name: test_current_date
  test_code: |
    bbb
  test_tags: happy path    
  
hope this helps!
"""
        expected_output = {
            "here is the response": None,
            "language": "python",
            "new_tests": [
                {
                    "test_behavior": "aaa\n",
                    "test_name": "test_current_date",
                    "test_code": "bbb\n",
                    "test_tags": "happy path",
                }
            ],
        }
        assert try_fix_yaml(yaml_str) == expected_output


    def test_invalid_yaml_wont_parse(self):
        from cover_agent.utils import try_fix_yaml

        yaml_str = """
here is the response

language: python
tests:
- test_behavior: |
aaa
test_name:"""
        expected_output = None
        assert load_yaml(yaml_str) == expected_output

    def test_load_yaml_second_fallback_failure(self):
        yaml_str = "```yaml\ninvalid_yaml: [unclosed_list\n```"
        assert load_yaml(yaml_str) is None



    def test_parse_args_full_repo_defaults_with_imports(self):
        from cover_agent.utils import parse_args_full_repo
        import sys
        import os
    
        test_args = [
            "program_name",
            "--project-language", "python",
            "--project-root", "/path/to/project",
            "--code-coverage-report-path", "/path/to/report",
            "--test-command", "pytest"
        ]
        sys.argv = test_args
        args = parse_args_full_repo()
    
        assert args.project_language == "python"
        assert args.project_root == "/path/to/project"
        assert args.code_coverage_report_path == "/path/to/report"
        assert args.test_command == "pytest"
        assert args.max_test_files_allowed_to_analyze == 20
        assert args.look_for_oldest_unchanged_test_file is False
        assert args.test_command_dir == os.getcwd()
        assert args.coverage_type == "cobertura"
        assert args.report_filepath == "test_results.html"
        assert args.max_iterations == 3
        assert args.additional_instructions == ""
        assert args.model == "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
        assert args.api_base == "http://localhost:11434"
        assert args.strict_coverage is False
        assert args.run_tests_multiple_times == 1
        assert args.use_report_coverage_feature_flag is False
        assert args.log_db_path == ""
        assert args.test_file_output_path == ""
        assert args.desired_coverage == 100


    def test_find_test_files(self, mocker):
        from cover_agent.utils import find_test_files
        import argparse
    
        mock_os_walk = [
            ('/path/to/project', ('dir1', 'dir2'), ('test_file1.py', 'file2.py')),
            ('/path/to/project/dir1', (), ('test_file2.py', 'file3.py')),
            ('/path/to/project/dir2', (), ('file4.py', 'test_file3.py')),
        ]
        mocker.patch('os.walk', return_value=mock_os_walk)
        mocker.patch('cover_agent.utils.is_forbidden_directory', return_value=False)
        mocker.patch('cover_agent.utils.filename_to_lang', return_value='python')
    
        args = argparse.Namespace(
            project_root='/path/to/project',
            project_language='python',
            max_test_files_allowed_to_analyze=10,
            look_for_oldest_unchanged_test_file=False
        )
    
        test_files = find_test_files(args)
        expected_files = [
            '/path/to/project/test_file1.py',
            '/path/to/project/dir1/test_file2.py',
            '/path/to/project/dir2/test_file3.py'
        ]
    
        assert test_files == expected_files

    def test_try_fix_yaml_invalid_snippet(self):
        from cover_agent.utils import try_fix_yaml
        
        # Invalid YAML inside code block markers
        yaml_str = '''```yaml
        key: [unclosed bracket
        ```'''
        result = try_fix_yaml(yaml_str)
        assert result is None


    def test_find_test_files_with_forbidden_dirs(self, mocker):
        from cover_agent.utils import find_test_files
        import argparse
        
        mock_os_walk = [
            ('/path/to/project', ('test', 'node_modules'), ('test_file1.py',)),
            ('/path/to/project/test', (), ('test_file2.py',)),
            ('/path/to/project/node_modules', (), ('test_file3.py',))
        ]
        
        def mock_is_forbidden(path, lang):
            return 'node_modules' in path
            
        mocker.patch('os.walk', return_value=mock_os_walk)
        mocker.patch('cover_agent.utils.is_forbidden_directory', side_effect=mock_is_forbidden)
        mocker.patch('cover_agent.utils.filename_to_lang', return_value='python')
        mocker.patch('os.path.getmtime', return_value=1000)
        
        args = argparse.Namespace(
            project_root='/path/to/project',
            project_language='python',
            max_test_files_allowed_to_analyze=2,
            look_for_oldest_unchanged_test_file=True
        )
        
        test_files = find_test_files(args)
        expected_files = [
            '/path/to/project/test_file1.py',
            '/path/to/project/test/test_file2.py'
        ]
        
        assert test_files == expected_files

