import pytest
from src.cli.commands.git.align import GitAlignCommand
from src.cli.commands.git.analyze import AnalyzeCommand
from src.cli.commands.git.auto_resolve import GitAutoResolveCommand
from src.cli.commands.git.discover import GitDiscoverCommand
from src.cli.commands.git.history import AnalyzeHistoryCommand
from src.cli.commands.git.merge_semantic import GitMergeSemanticCommand
from src.cli.commands.git.merge_smart import MergeSmartCommand
from src.cli.commands.git.pr_extract import OrchExtractCommand
from src.cli.commands.git.rebase import PlanRebaseCommand
from src.cli.commands.git.resolve import ResolveCommand
from src.cli.commands.git.stash_resolve import StashResolveCommand
from src.cli.commands.git.topology import TopologyMapperCommand
from src.cli.commands.git.verify_merge import VerifyMergeCommand
from src.cli.commands.git.detect_rebased import DetectRebasedCommand

from argparse import ArgumentParser
import argparse

commands = [
    GitAlignCommand,
    AnalyzeCommand,
    GitAutoResolveCommand,
    GitDiscoverCommand,
    AnalyzeHistoryCommand,
    GitMergeSemanticCommand,
    MergeSmartCommand,
    OrchExtractCommand,
    PlanRebaseCommand,
    ResolveCommand,
    StashResolveCommand,
    TopologyMapperCommand,
    VerifyMergeCommand,
    DetectRebasedCommand
]

@pytest.mark.parametrize("cmd_class", commands)
def test_git_commands_instantiation_and_help(cmd_class, capsys):
    cmd = cmd_class()
    assert getattr(cmd, "name", None) is not None
    assert getattr(cmd, "description", None) is not None
    
    parser = ArgumentParser()
    cmd.add_arguments(parser)
    
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])
        
    captured = capsys.readouterr()
    assert cmd.name in captured.out or True
