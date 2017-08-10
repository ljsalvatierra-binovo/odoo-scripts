# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Python script to apply commit/s to selected branch/es
#
# Use: python git_update_branches -p /path/to/repository -b b1,b2 --cherry-pick-sha XXXXXXXXXXXXX
#      python git_update_branches -p /path/to/repository --exclude-branches master --cherry-pick-sha XXXXXXXXXXXXX
#
# Copyright (C) 2017 Binovo IT Human Project S.L.
#
# Author: Luis J. Salvatierra
import subprocess
from subprocess import STDOUT, CalledProcessError
import git
import os
import argparse


class GitCherryPick:

    def __init__(self, repo, branches):
        self.repo = repo
        self.branches = branches

    def apply_commit(self, sha):
        for branch in self.branches:
            branch.checkout()
            print("Switched to branch '%s'" % branch.name)
            res = subprocess.check_output("git cherry-pick %s" % sha, cwd=repo_path, shell=True, stderr=STDOUT)
            print(res)
        return True

    def apply_multiple_commits(self, sha_from, sha_to):
        commit_range = sha_from + '^..' + sha_to
        for branch in self.branches:
            branch.checkout()
            print("Switched to branch '%s'" % branch.name)
            res = subprocess.check_output("git cherry-pick %s" % commit_range, cwd=repo_path, shell=True, stderr=STDOUT)
            print(res)
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default=os.getcwd(), help='Git repository path')
    parser.add_argument('-b', '--branches', type=str, default=None, help='Branches to apply the update')
    parser.add_argument('--exclude-branches', type=str, default=None, help='Branches to NOT apply the update')
    parser.add_argument('--cherry-pick-sha', type=str, default=None, help='Cherry pick SHA1 to apply')
    parser.add_argument('--cherry-pick-sha-from', type=str, default=None, help='Cherry pick SHA1 commit to apply FROM (included)')
    parser.add_argument('--cherry-pick-sha-to', type=str, default=None, help='Cherry pick SHA1 commit to apply TO (included)')
    args = parser.parse_args()
    try:
        if args.path:
            repo_path = args.path
        else:
            repo_path = os.getcwd()
        repo = git.Repo(repo_path)
        if repo.bare:
            print(repo_path)
            print('Please specify a GIT repository path!')
            exit(1)
        repo_branches = {}
        branches = []
        for branch in repo.heads:
            repo_branches[branch.name] = branch
        if args.branches and args.exclude_branches:
            print('Please, select branches or exclude branches, not both!')
            exit(1)
        if args.branches and 0 < len(args.branches.split(',')):
            for branch_name in args.branches.split(','):
                if branch_name not in repo_branches:
                    print('The branch %s does not exist!')
                    exit(1)
                else:
                    branches.append(repo_branches[branch_name])
        elif args.exclude_branches and 0 < len(args.exclude_branches.split(',')):
            branches = repo.heads
            exclude_branches = args.exclude_branches.split(',')
            for branch in branches:
                if branch.name in exclude_branches:
                    branches.remove(branch)
        else:
            branches = repo.heads
        git_cherry_pick = GitCherryPick(repo, branches)
        print('The following branches will be updated:')
        print(', '.join([branch.name for branch in branches]))
        key = raw_input('Do you wish to continue? [Y/n] ')
        if 'Y' == key.upper():
            if args.cherry_pick_sha is not None:
                res = git_cherry_pick.apply_commit(args.cherry_pick_sha)
            elif args.cherry_pick_sha_from is not None and args.cherry_pick_sha_to is not None:
                res = git_cherry_pick.apply_multiple_commits(args.cherry_pick_sha_from, args.cherry_pick_sha_to)
        elif 'N' == key.upper():
            print('Bye!')
            exit(1)
        else:
            print('Key "%s" not recognised.' % key)
    except CalledProcessError, cpe:
        print(cpe.output)
        subprocess.check_output("git cherry-pick --abort", cwd=repo_path, shell=True, stderr=STDOUT)
    except Exception, e:
        print(e.message)
