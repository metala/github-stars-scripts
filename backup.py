#!/usr/bin/env python3
# Description: download Github starred repositories for a user
# Outputs a JSON file containing name, description, url, homepage, language, number of open issues/stars for each starred repository
# A Personal Access Token must be available in the GITHUB_ACCESS_TOKEN environment variable

__copyright__ = """

    Copyright 2020 nodiscc <nodiscc@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
__license__ = "MIT"

import os
import sys
import github
import json
import logging

usage = 'USAGE: {} USERNAME OUTPUT_FILE\nGITHUB_ACCESS_TOKEN must be declared in the environment, see https://github.com/settings/tokens'.format(sys.argv[0])

try:
    username = sys.argv[1]
except IndexError:
    logging.error("No username specified")
    print(usage)
    exit(1)

if username == "--help":
    print(usage)
    exit(0)

try:
    outfile = sys.argv[2]
except IndexError:
    logging.error("No output file specified")
    print(usage)
    exit(1)

#############################

g = github.Github(os.environ['GITHUB_ACCESS_TOKEN'])
logging.basicConfig(format='[%(levelname)s]: %(message)s',level=logging.INFO)
stars_backup = {}
index = 1

for starred_repo in g.get_user(username).get_starred():
    logging.info(starred_repo)
    repo = {}

    try:
        repo_data = g.get_repo(starred_repo.full_name)
        repo['name'] = repo_data.full_name
    except github.UnknownObjectException:
        logging.warning('repo {} does not exist anymore'.format(starred_repo))
        continue
    except github.GithubException as e:
        logging.warning('something went wrong. {}'.format(str(e)))
        continue

    repo['description'] = repo_data.description
    repo['url'] = 'https://github.com/{}'.format(repo_data.full_name)
    repo['homepage'] = repo_data.homepage
    repo['language'] = repo_data.language
    repo['open_issues'] = repo_data.open_issues
    repo['stars'] = repo_data.stargazers_count
    stars_backup[repo_data.full_name] = repo
    index += 1
    stars_json = json.dumps(stars_backup,indent=2)

with open(outfile, 'w+') as outfile:
    outfile.write(stars_json)
